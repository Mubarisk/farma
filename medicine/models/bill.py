from django.db import models
from .medicine import MedicinePackage, Alert
from user.models import User
from django.db import transaction


class Bill(models.Model):
    staff = models.ForeignKey(
        User, on_delete=models.CASCADE, limit_choices_to={"role": "staff"}
    )
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    customer_mail = models.EmailField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Bill {self.id} - {self.staff.username}"


# Bill Items
class BillItem(models.Model):
    bill = models.ForeignKey(
        Bill, on_delete=models.CASCADE, related_name="items"
    )
    medicine_package = models.ForeignKey(
        MedicinePackage, on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )

    def save(self, *args, **kwargs):
        with transaction.atomic():

            # Lock stock row to prevent race conditions
            medicine_package = MedicinePackage.objects.select_for_update().get(
                id=self.medicine_package.id
            )
            if medicine_package.stock < self.quantity:
                raise ValueError("Insufficient stock")

            # Deduct stock
            medicine_package.stock -= self.quantity
            medicine_package.save()
            medicine_package.medicine.stock_quantity -= (
                self.quantity * medicine_package.conversion_factor
            )
            medicine_package.medicine.save()
            if (
                medicine_package.medicine.stock_quantity
                <= medicine_package.medicine.alert_threshold
            ):
                Alert.objects.create(
                    medicine=medicine_package.medicine,
                    alert_type=Alert.LOW_STOCK,
                )
            # Calculate price
            self.total_price = self.medicine_package.price * self.quantity

            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.bill.id} - {self.medicine_package.medicine.name} ({self.medicine_package.package_type})"
