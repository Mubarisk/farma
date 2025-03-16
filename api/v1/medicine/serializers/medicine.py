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
        fields = "__all__"

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        packages = validated_data.get("packages")
        if self.instance:
            for package in packages:
                if package.get("modify") == "add":
                    continue
                if not package.get("id"):
                    raise serializers.ValidationError(
                        "Package ID is required for update or delete."
                    )
        return validated_data

    def create(self, validated_data):
        packages = validated_data.pop("packages")
        medicine = Medicine.objects.create(**validated_data)
        packages_list = []
        for package in packages:
            packages_list.append(MedicinePackage(medicine=medicine, **package))
        MedicinePackage.objects.bulk_create(packages_list)
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
        return instance

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["packages"] = MedicinePackageSerializer(
            instance.packages.all(), many=True
        ).data
        return data
