from django.db import models

# Create your models here.
class Poll(models.Model):
    text = models.CharField(max_length=255)
    description = models.CharField(max_length=5000,default='Przepis')
    pub_date = models.DateField()

    def __str__(self):
        return self.text


class Comment(models.Model):
	comment = models.ForeignKey(Poll,on_delete=models.CASCADE)
	comment_text = models.CharField(max_length = 400)
	votes = models.IntegerField(default = 0)

	def __str__(self):
		return "{} - {}".format(self.comment.text[:30],self.comment_text[:30])
