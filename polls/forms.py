from django import forms
from .models import Poll,Comment

class RecipeForm(forms.ModelForm):

	rating = forms.CharField(
					label='Rating',
					max_length=500,
					min_length=3,
					widget=forms.TextInput(attrs={'class':'form-control'}))

	rating2 = forms.CharField(
					label='Second Rating',
					max_length=50,
					min_length=3,
					widget=forms.TextInput(attrs={'class':'form-control'}))

	class Meta:
		model = Poll
		fields = ['text','description','rating','rating2']
		widgets = {
			'description':forms.Textarea(attrs={"class":"form-control"})
			# 'ingredients':forms.Textarea(attrs={"class":"form-control"})
		}

class EditRecipeForm(forms.ModelForm):

	class Meta:
		model = Poll
		fields = ['text','description']
		widgets = {
			'description':forms.Textarea(attrs={"class":"form-control"})
		
			# 'ingredients':forms.Textarea(attrs={"class":"form-control"})
		}

class RatingForm(forms.ModelForm):

	class Meta:
		model = Comment
		fields = ['comment_text']