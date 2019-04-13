from django.shortcuts import get_object_or_404,render
from django.http import HttpResponse
from .models import Poll,Comment
# Create your views here.
def polls_list(request):
	recipes = Poll.objects.all()
	context = {'recipes': recipes}
	return render(request,'polls/recipes.html', context)

def recipes_detail(request,recipes_id):
	# return HttpResponse('Youre looking for recipe id:{}'.format(recipes_id))
	
	# recipes = Poll.objects.get(id=recipes_id)
	recipes = get_object_or_404(Poll, id=recipes_id)

	if request.method == "POST":
		print(request.POST)
		print("You Posted!!!!")

	if request.method == "GET":
		print(request.GET)
		print("You Get Me")

	context = {'recipes': recipes}
	return render(request,'polls/recipes_detail.html',context)


def recipes_vote(request,recipes_id):
	comment_id = request.POST['comment']
	comment = Comment.objects.get(id=comment_id)
	comment.votes += 1
	comment.save()
	return HttpResponse('Recipe Id: {}'.format(recipes_id))

