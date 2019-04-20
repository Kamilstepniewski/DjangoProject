from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class UserRegistrationForm(forms.Form):
	firstname = forms.CharField(
					label='First Name',
					max_length=50,
					widget=forms.TextInput(attrs={'class':'form-control'}))
	lastname = forms.CharField(
					label='Last Name',
					max_length=50,
					widget=forms.TextInput(attrs={'class':'form-control'}))
	username = forms.CharField(
					label='Username',
					max_length=50,
					min_length=5,
					widget=forms.TextInput(attrs={'class':'form-control'}))
	email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control'}))
	password1 = forms.CharField(
					label='Password',
					max_length=50,
					min_length=5,
					widget=forms.PasswordInput(attrs={'class':'form-control'}))
	password2 = forms.CharField(
					label='Confirm Password',
					max_length=50,
					min_length=5,
					widget=forms.PasswordInput(attrs={'class':'form-control'}))


	def clean_email(self):
		email = self.cleaned_data['email']
		qs = User.objects.filter(email=email)
		if qs.exists():
			raise ValidationError('Email is already registerd. ')
		return email


	# def clean_password1(self):
	# 	p1 = self.cleaned_data['password1']
	#  	p2 = self.cleaned_data['password2']
	#  	if p1 != p2:
	#  		raise ValidationError('Passwords does not match')
	#  	return p1



	 # def clean_password2(self):
	 # 	p1 = self.cleaned_data['password1']
	 # 	p2 = self.cleaned_data['password2']
	 # 	if p1 != p2:
	 # 		raise ValidationError('Passwords does not match')
	 # 	return p2
	
	def clean(self):
		cleaned_data = super().clean()
		p1 = cleaned_data.get('password1')
		p2 = cleaned_data.get('password2')


		if p1 and p2:
			if p1 != p2:
				raise ValidationError('Passwords does not match')