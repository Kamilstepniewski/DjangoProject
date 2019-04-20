from django.urls import path

from . import views

app_name = "makefood"

urlpatterns = [
    path('recipes/',views.polls_list,name="recipes"),
    path('add/',views.add_recipe,name='add'),
    path('edit/<int:recipes_id>/',views.edit_recipe,name='edit_recipe'),
    
    path('edit/<int:recipes_id>/comment/add/',views.add_comment,name='add_comment'),
	path('delete/comment/<int:comment_id>/', views.delete_comment, name='comment_confirm_delete'),
	path('delete/recipes/<int:recipes_id>',views.delete_recipe,name="recipe_confirm_delete"),
    path('edit/comment/<int:comment_id>/',views.edit_comment,name='edit_comment'),
	path('detail/<int:recipes_id>/',views.recipes_detail,name='detail'),
	path('detail/<int:recipes_id>/vote/',views.recipes_vote,name='vote')
]