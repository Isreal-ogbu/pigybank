import datetime
from dataclasses import dataclass
from _decimal import Decimal
from django.contrib.auth.models import User
from django.db.models import Sum, Count, Avg

from core.models import Transaction, Catagory


@dataclass
class ReportEntry:
    catagory: Catagory
    total: Decimal
    count: int
    avg: Decimal


@dataclass
class ReportParams:
    user: User
    start_date: datetime.datetime
    end_date: datetime.datetime


def transaction_report(params: ReportParams) -> list[ReportEntry]:
    data = []
    queryset = Transaction.objects.filter(
        user=params.user,
        date__gte=params.start_date,
        date__lte=params.end_date
    ).values('catagory').annotate(
        total=Sum('amount'),
        count=Count('id'),
        avg=Avg('amount')
    )
    catagory_index = {}
    for catagory in Catagory.objects.filter(user=params.user):
        catagory_index[catagory.pk] = catagory
    for entry in queryset:
        catagory = catagory_index.get(entry['catagory'])
        report_entry = ReportEntry(catagory, entry['total'], entry['count'], entry['avg'])
        data.append(report_entry)
    return data
