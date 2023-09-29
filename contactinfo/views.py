from django.http import HttpResponse
from django.shortcuts import render
from .models import ContactInfo


# from django.db import connection, reset_queries
# from .models import ContactInfo
# from .extractor import *

# def add(request):
#     for lists in data2:
#         ContactInfo(facility_id=lists[0], facility_name=str(lists[1]), phone_no=str(lists[2]), partner_name=str(lists[3])).save()
#     return HttpResponse("done")

def home(request):
    the_data = ContactInfo.objects.order_by("facility_name")
    context = {'the_data':the_data}
    return render(request, "data.html", context)

