from celery import shared_task
from medicine.models import Medicine, Alert
from django.utils import timezone


@shared_task(name="check_medicine_expiry")
def check_medicine_expiry():
    medicines = Medicine.objects.filter(
        expiry_date__lte=timezone.now(), is_deleted=False
    )
    for medicine in medicines:
        if Alert.objects.filter(
            medicine=medicine, alert_type=Alert.EXPIRY
        ).exists():
            continue
        Alert.objects.create(medicine=medicine, alert_type=Alert.EXPIRY)
    return True 