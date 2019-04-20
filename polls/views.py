from django.shortcuts import get_object_or_404,render, redirect
from django.http import HttpResponse , HttpResponseRedirect
from .models import Poll,Comment,Vote
from django.contrib import messages
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .forms import RecipeForm,EditRecipeForm,RatingForm
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Count
import datetime
# Create your views here.
@login_required
def polls_list(request):
	
	# if not request.user.is_authenticated:
	# 	return redirect('{}?next={}'.format(settings.LOGIN_URL, request.path))
	recipes = Poll.objects.all()
	search_term = ''

	if 'title' in request.GET:
		recipes = recipes.order_by('text')

	if 'pub_date' in request.GET:
		recipes = recipes.order_by('-pub_date')

	if 'num_votes' in request.GET:
		# recipes = recipes.order_by('num_votes')
		recipes = recipes.annotate(Count('vote')).order_by('vote__count')

	if 'search' in request.GET:
		search_term = request.GET['search']
		recipes = recipes.filter(text__icontains=search_term)
		"""
		Description 
		"""

	paginator = Paginator(recipes,10)
	

	page = request.GET.get('page')
	recipes = paginator.get_page(page)

	get_dict_copy = request.GET.copy()
	params = get_dict_copy.pop('page',True) and get_dict_copy.urlencode()

	context = {'recipes': recipes,'params':params,'search_term':search_term}
	return render(request,'polls/recipes.html', context)

@login_required
def add_recipe(request):
	if request.method =="POST":
		form = RecipeForm(request.POST)
		if form.is_valid():
			new_poll=form.save(commit=False)
			new_poll.pub_date = datetime.datetime.now()
			new_poll.owner = request.user
			new_poll.save()
			new_rating = Comment(
					comment = new_poll,
					comment_text=form.cleaned_data['rating']

				).save()
			new_rating2 = Comment(
					comment = new_poll,
					comment_text=form.cleaned_data['rating2']

				).save()
			messages.success(
				request,
				'Good Job . You added your great recipe ',
				'alert alert-success alert-dismissible'
				)
			return redirect('makefood:recipes')
	else:
		form = RecipeForm()
	context={'form':form}
	return render(request,'polls/add_recipe.html',context)

@login_required
def edit_recipe(request,recipes_id):
	recipes = get_object_or_404(Poll,id=recipes_id)
	if request.user != recipes.owner:
		return redirect('/')

	if request.method == 'POST':
		form = EditRecipeForm(request.POST, instance=recipes)
		if form.is_valid():
			form.save()
			messages.success(
					request,
					'Recipe Was Edit',
					extra_tags='alert alert-success alert-dismissible fade show'
				)
			return redirect('makefood:recipes')
	else:
		form = EditRecipeForm(instance=recipes)

	return render(request,'polls/edit_recipe.html', {'form':form ,'recipes':recipes})



@login_required
def add_comment(request,recipes_id):
	recipes = get_object_or_404(Poll,id=recipes_id)
	if request.user != recipes.owner:
		return redirect('/')

	if request.method =='POST':
		form = RatingForm(request.POST)
		if form.is_valid():
			new_comment = form.save(commit=False)
			new_comment.comment = recipes
			new_comment.save() 
			messages.success(
					request,
					'Comment Add Successfully',
					extra_tags='alert alert-success alert-dismissible fade show'
				)
			return redirect('makefood:recipes')
	else:
		form = RatingForm()
	return render(request,'polls/add_comment.html',{'form':form})

@login_required
def delete_recipe(request,recipes_id):
    recipes = get_object_or_404(Poll, id=recipes_id)
    if request.user != recipes.owner:
        return redirect('/')

    if request.method == "POST":
        recipes.delete()
        messages.success(
                        request,
                        'Recipe Deleted Successfully',
                        extra_tags='alert alert-success alert-dismissible fade show'
                        )
        return redirect('makefood:recipes')

    return render(request, 'polls/delete_recipe_confirm.html', {'recipes': recipes})


@login_required
def edit_comment(request,comment_id):
	comment = get_object_or_404(Comment,id=comment_id)
	recipes = get_object_or_404(Poll,id=comment.comment.id)
	if request.user != recipes.owner:
		return redirect('/')

	if request.method =='POST':
		form = RatingForm(request.POST,instance=comment)
		if form.is_valid():
			form.save()
			messages.success(
					request,
					'Comment Edited Successfully',
					extra_tags='alert alert-success alert-dismissible fade show'
				)
			return redirect('makefood:recipes')
	else:
		form = RatingForm(instance=comment)
	return render(request,'polls/add_comment.html',{'form':form,'edit_mode':True,'comment':comment})

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    recipes = get_object_or_404(Poll, id=comment.comment.id)
    if request.user != recipes.owner:
        return redirect('/')

    if request.method == "POST":
        comment.delete()
        messages.success(
                        request,
                        'Comment Deleted Successfully',
                        extra_tags='alert alert-success alert-dismissible fade show'
                        )
        return redirect('makefood:recipes')

    return render(request, 'polls/delete_comment_confirm.html', {'comment':comment})

@login_required
def recipes_detail(request,recipes_id):
	# return HttpResponse('Youre looking for recipe id:{}'.format(recipes_id))
	
	# recipes = Poll.objects.get(id=recipes_id)
	recipes = get_object_or_404(Poll, id=recipes_id)
	user_can_vote = recipes.user_can_vote(request.user)
	results = recipes.get_result_dict()
	context = {'recipes': recipes, 'user_can_vote':user_can_vote, 'results':results}
	return render(request,'polls/recipes_detail.html',context)

@login_required
def recipes_vote(request,recipes_id):
	recipes = get_object_or_404(Poll, id=recipes_id)
	if not recipes.user_can_vote(request.user):
		messages.error(request,'You have already voted.')
		return HttpResponseRedirect(reverse("makefood:detail",args=(recipes_id,)))

	comment_id = request.POST.get('comment')
	if comment_id:
		comment = Comment.objects.get(id=comment_id) 
		new_comment = Vote(user=request.user,recipe=recipes,comment=comment)
		new_comment.save()
		# comment.votes += 1
		# comment.save()
	else:
		messages.error(request,'No Choice Was Found')
		return redirect('makefood:detail', recipes_id=recipes_id)
	return redirect('makefood:detail', recipes_id=recipes_id)
	# return render(request,'polls/recipes_results.html',{'error': True})	

#polls = makefood
#poll = recipes