from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import login,authenticate,logout
from django.urls import reverse
from django.contrib import messages
from .forms import UserRegistrationForm
from django.contrib.auth.models import User
# Create your views here.
def login_user(request):
	if request.method == "POST":
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request,username=username, password=password)
		if user is not None:
			login(request, user)
			redirect_url = request.GET.get('next','home')
			return redirect('home')
		else:
			messages.error(request,'Bad username or password')
	return render(request,'accounts/login.html',{})


def logout_user(request):
	logout(request)
	return redirect('accounts:login')

def user_registration(request):
	form = UserRegistrationForm()
	if request.method == 'POST':
		form = UserRegistrationForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			firstname = form.cleaned_data['firstname']
			lastname = form.cleaned_data['lastname']
			email = form.cleaned_data['email']
			user = User.objects.create_user(username,email=email, password=password)
			user.first_name = firstname
			user.last_name = lastname
			user.save()
			messages.success(request,'Thaks for registering {} .Enjoy unlimited access to our recipes .'.format(user.first_name))
			return redirect('accounts:login')
	else:
		form = UserRegistrationForm()	
	return render(request,'accounts/register.html',{'form': form})