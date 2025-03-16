from rest_framework import serializers
from medicine.models import Bill, BillItem


class BillItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillItem
        exclude = ("bill",)
        read_only_fields = ("total_price",)


class BillSerializer(serializers.ModelSerializer):
    items = BillItemSerializer(many=True, write_only=True)

    class Meta:
        model = Bill
        fields = ("id", "items", "total_price", "customer_mail")
        read_only_fields = ("id", "total_price")

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        # check the quantity of each item
        items = validated_data.get("items")
        self.total_price = 0
        for item in items:
            if item["quantity"] <= 0:
                raise serializers.ValidationError(
                    "Quantity must be greater than 0."
                )
            if item["medicine_package"].stock < item["quantity"]:
                raise serializers.ValidationError("Not enough stock.")
            self.total_price += (
                item["medicine_package"].price * item["quantity"]
            )
        return validated_data

    def create(self, validated_data):
        items = validated_data.pop("items")
        validated_data["total_price"] = self.total_price
        bill = Bill.objects.create(
            staff=self.context.get("request").user, **validated_data
        )
        for item in items:
            BillItem.objects.create(bill=bill, **item)
        # send email to customer
        return bill
