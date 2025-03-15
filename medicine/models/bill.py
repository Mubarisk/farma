from django.db import models
from .medicine import MedicinePackage
from user.models import User


class Bill(models.Model):
    staff = models.ForeignKey(
        User, on_delete=models.CASCADE, limit_choices_to={"role": "staff"}
    )
    created_at = models.DateTimeField(auto_now_add=True)

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
        self.total_price = self.medicine_package.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.bill.id} - {self.medicine_package.medicine.name} ({self.medicine_package.package_type})"
