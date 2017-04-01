from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.
gender = [("M", "M"),("F","F")]
u_type = [("general","general"),("hunters","hunters"),("premium","premium")]
topic_type = [("politics","politics"),("tech","tech"),("startup","startup")]

class e_user(models.Model):
	u_id = models.CharField(default=str(uuid.uuid1()),editable=False,max_length=100)
	user = models.ForeignKey(User)
	screen_name = models.CharField(max_length=50)
	name = models.CharField(max_length=50)
	pic_url = models.CharField(max_length=500)
	age = models.IntegerField()
	location = models.CharField(max_length=100)
	gender = models.CharField(choices = gender,max_length=10)
	ethnicity = models.CharField(max_length=50)
	u_type = models.CharField(choices= u_type,max_length=50)


class topic(models.Model):
	creator = models.ForeignKey(e_user)
	t_id = models.CharField(default=str(uuid.uuid1()),editable=False,max_length=100,unique=True)
	issue = models.CharField(max_length=1000)
	created_at= models.DateTimeField(auto_now_add=True) 
	hash_tag = models.CharField(max_length=30,blank=True)
	upvotes = models.ManyToManyField(e_user,related_name="t_upvotes",blank=True)
	downvotes = models.ManyToManyField(e_user,related_name="t_downvotes",blank=True)
	comment_permission = models.ManyToManyField(e_user,related_name="comment_permission",blank=True)
	topic_type = models.CharField(choices=topic_type,max_length=30)

class comment(models.Model):
	c_id = models.CharField(default=str(uuid.uuid1()),editable=False,max_length=100,unique=True)
	topic = models.ForeignKey(topic)
	user = models.ForeignKey(e_user)
	body = models.TextField()
	created_at= models.DateTimeField(auto_now_add=True) 
	upvotes = models.ManyToManyField(e_user,blank=True,related_name="c_upvotes")
	shares = models.ManyToManyField(e_user,blank=True,related_name="c_shares")

class editor_pick(models.Model):
	editor_topics = models.ManyToManyField(topic)
	score = models.IntegerField()

	class Meta:
		ordering = ("score",)

