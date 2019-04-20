from django.urls import path

from . import views

app_name = "aboutus"

urlpatterns = [
    path('aboutus/',views.aboutus,name="aboutus"),
]