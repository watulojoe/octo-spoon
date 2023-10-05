from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import ContactInfo
from .forms import ContactInfoForm
from django.db.models import Q


# from django.db import connection, reset_queries
# from .models import ContactInfo
# from .extractor import *

# def add(request):
#     for lists in data2:
#         ContactInfo(facility_id=lists[0], facility_name=str(lists[1]), phone_no=str(lists[2]), partner_name=str(lists[3])).save()
#     return HttpResponse("done")


def home(request):
    if request.method == "POST":
        query = request.POST['query_search']
        # the_data = ContactInfo.objects.filter(facility_name__contains=query)    #  or search multiple field:
        multiple_query = Q(Q(facility_name__contains=query) | Q(partner_name__contains=query))    #  or search multiple field:
        the_data = ContactInfo.objects.filter(multiple_query)
        context = {'the_data':the_data}
        return render(request, "data.html", context)
    else:
        the_data = ContactInfo.objects.order_by("facility_name")
        context = {'the_data':the_data}
        return render(request, "data.html", context)


def create_contact(request):
    if request.method == "POST":
        form = ContactInfoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
        else:
            return render(request, "create_contact.html", {"error":"bad data"})
    else:
        context = {"form": ContactInfoForm()}
        return render(request, "create_contact.html", context)

