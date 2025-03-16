from django.db import models
from user.models import User


class MedicineCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Medicine(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(MedicineCategory, on_delete=models.CASCADE)
    stock_quantity = models.PositiveIntegerField(default=0)
    expiry_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name


class MedicinePackage(models.Model):
    SINGLE = "single"
    STRIP = "strip"
    PACK = "pack"
    BOX = "box"
    PACKAGE_CHOICES = (
        (SINGLE, "Single"),
        (STRIP, "Strip"),
        (PACK, "Pack"),
        (BOX, "Box"),
    )
    medicine = models.ForeignKey(
        Medicine, on_delete=models.CASCADE, related_name="packages"
    )
    package_type = models.CharField(max_length=10, choices=PACKAGE_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ("medicine", "package_type")

    def __str__(self):
        return f"{self.medicine.name} - {self.package_type}"

