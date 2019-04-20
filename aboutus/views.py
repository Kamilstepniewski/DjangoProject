from django.shortcuts import render
from django.http import HttpResponse
import datetime
# Create your views here.
def aboutus(request):
	return render(request,'AboutUs.html',{})