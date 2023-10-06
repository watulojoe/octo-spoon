from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.data, name="data"),
    path("create/", views.create_contact, name="create")
    # path("add", views.add, name="add"),

]
