from rest_framework.generics import GenericAPIView
from helpers.permissions import IsAdmin
from farma.config.response import SuccessResponse, ErrorResponse
from medicine.models import Medicine, Bill
from django.utils.dateparse import parse_date
import decimal


class StockAvailabilityAPIView(GenericAPIView):
    permission_classes = [IsAdmin]  # Only admin can access this API

    def get(self, request):
        medicines = Medicine.objects.prefetch_related("packages").filter(
            is_deleted=False
        )
        stock_data = {
            medicine.name: {
                package.package_type: package.stock
                for package in medicine.packages.all()
            }
            for medicine in medicines
        }
        return SuccessResponse(data={"stock": stock_data})


class SalesReportsAPIView(GenericAPIView):
    permission_classes = [IsAdmin]  # Only admin can access this API

    def get(self, request):
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")
        staff = request.query_params.get("staff")

        if not start_date or not end_date:
            return ErrorResponse(
                message="Start date and end date are required"
            )

        start_date = parse_date(start_date)
        end_date = parse_date(end_date)

        if not start_date or not end_date:
            return ErrorResponse(message="Invalid date format. Use YYYY-MM-DD")
        filter_kwargs = {"created_at__date__range": [start_date, end_date]}
        if staff:
            filter_kwargs["staff_id"] = staff

        bills = Bill.objects.filter(**filter_kwargs)

        report_data = {}

        for bill in bills:
            staff_name = bill.staff.username
            if staff_name not in report_data:
                report_data[staff_name] = {
                    "total_sales": 0,
                    "total_revenue": decimal.Decimal(0.0),
                    "bills": [],
                }

            bill_total = bill.total_price or 0.0
            report_data[staff_name]["total_sales"] += 1
            report_data[staff_name]["total_revenue"] += bill_total
            report_data[staff_name]["bills"].append(
                {
                    "bill_id": bill.id,
                    "created_at": bill.created_at,
                    "total_price": bill_total,
                    "customer_mail": bill.customer_mail,
                }
            )

        return SuccessResponse(data=report_data)
