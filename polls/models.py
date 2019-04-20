from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Poll(models.Model):
	owner = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
	text = models.CharField(max_length=255)
	description = models.CharField(max_length=5000,default='Recipe')
	pub_date = models.DateField()
	# list_display=['text','description']

	def __str__(self):
		return self.text

	# def recipe(self):
	# 	return self.description
		# return self.description
	def user_can_vote(self,user):
		"""
		Returns False if user has already vote,else True
		"""
		user_votes = user.vote_set.all()
		qs = user_votes.filter(recipe=self)
		if qs.exists():
			return False
		return True

	@property
	def num_votes(self):
		return self.vote_set.count()

	def get_result_dict(self):
		res = []
		for comment in self.comment_set.all():
			d = {}
			d['text'] = comment.comment_text
			d['num_votes'] = comment.num_votes
			if not self.num_votes:
				d['percentage'] = 0
			else:
				d['percentage'] = comment.num_votes / self.num_votes * 100
			res.append(d)
		return res


class Comment(models.Model):
	comment = models.ForeignKey(Poll,on_delete=models.CASCADE)
	comment_text = models.CharField(max_length = 400)
	# votes = models.IntegerField(default = 0)

	def __str__(self):
		return "{} - {}".format(self.comment.text[:30],self.comment_text[:30])

	@property
	def num_votes(self):
		return self.vote_set.count()


class Vote(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	recipe = models.ForeignKey(Poll,on_delete=models.CASCADE)
	comment = models.ForeignKey(Comment,on_delete=models.CASCADE)