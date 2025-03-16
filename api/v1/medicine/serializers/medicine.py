from rest_framework import serializers
from medicine.models import Medicine, MedicineCategory, MedicinePackage


class MedicineCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicineCategory
        fields = "__all__"


class MedicinePackageSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    modify = serializers.ChoiceField(
        choices=["add", "remove", "update"], required=False
    )

    class Meta:
        model = MedicinePackage
        exclude = ("medicine",)


class MedicineSerializer(serializers.ModelSerializer):
    packages = MedicinePackageSerializer(many=True, write_only=True)

    class Meta:
        model = Medicine
        exclude = ("is_deleted", "deleted_at")
        read_only_fields = ("stock_quantity",)

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        packages = validated_data.get("packages")
        is_base_unit = False
        if self.instance:
            for package in packages:
                if package.get("modify") == "add":
                    continue
                if not package.get("id"):
                    raise serializers.ValidationError(
                        "Package ID is required for update or delete."
                    )
                if package.get("is_base_unit"):
                    if not is_base_unit:
                        is_base_unit = True
                    else:
                        raise serializers.ValidationError(
                            "Only one package should be base unit."
                        )

        else:
            for package in packages:
                if package.get("is_base_unit"):
                    if not is_base_unit:
                        is_base_unit = True
                    else:
                        raise serializers.ValidationError(
                            "Only one package should be base unit."
                        )

        if not is_base_unit:
            raise serializers.ValidationError(
                "At least one package should be base unit."
            )
        return validated_data

    def create(self, validated_data):
        packages = validated_data.pop("packages")
        medicine = Medicine.objects.create(**validated_data)
        packages_list = []
        total_stock = 0
        for package in packages:
            packages_list.append(MedicinePackage(medicine=medicine, **package))
        MedicinePackage.objects.bulk_create(packages_list)
        total_stock = 0

        for package in packages_list:
            if package.is_base_unit:
                total_stock += package.stock
            else:
                total_stock += package.stock * package.conversion_factor
        medicine.stock_quantity = total_stock
        medicine.save(update_fields=["stock_quantity"])
        return medicine

    def update(self, instance, validated_data):
        packages = validated_data.pop("packages")
        instance = super().update(instance, validated_data)
        for package in packages:
            modify = package.pop("modify")
            if modify == "add":
                MedicinePackage.objects.create(medicine=instance, **package)
            elif modify == "remove":
                MedicinePackage.objects.filter(
                    medicine=instance, id=package["id"]
                ).delete()
            elif modify == "update":
                MedicinePackage.objects.filter(
                    medicine=instance, id=package["id"]
                ).update(**package)
        packages_list = MedicinePackage.objects.filter(medicine=instance)
        total_stock = 0
        for package in packages_list:
            if package.is_base_unit:
                total_stock += package.stock
            else:
                total_stock += package.stock * package.conversion_factor

        instance.stock_quantity = total_stock
        instance.save(update_fields=["stock_quantity"])
        return instance

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["packages"] = MedicinePackageSerializer(
            instance.packages.all(), many=True
        ).data
        return data
