from django.urls import path

from . import views

app_name = "makefood"

urlpatterns = [
    path('recipes/',views.polls_list,name="recipes"),
	path('detail/<int:recipes_id>/',views.recipes_detail,name='detail'),
	path('detail/<int:recipes_id>/vote/',views.recipes_vote,name='vote')
]