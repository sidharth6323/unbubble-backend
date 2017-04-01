from rest_framework import serializers
from models import e_user,comment,topic,editor_pick
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		exclude = ("password",)

class e_userSerializer(serializers.ModelSerializer):
	user = UserSerializer(read_only=True)
	class Meta:
		model = e_user
		fields = ('u_id', 'user', 'screen_name', 'name','location', 'pic_url', 'age','gender','ethnicity','u_type')

class commentSerializer(serializers.ModelSerializer):
	upvotes = e_userSerializer(many=True, read_only=True)
	shares = e_userSerializer(many=True, read_only=True)
	user = e_userSerializer(read_only=True)
	class Meta:
		model = comment
		fields = ('c_id','user', 'body', 'upvotes','created_at', 'shares')

class topicSerializer(serializers.ModelSerializer):
	creator = e_userSerializer(read_only=True)
	upvotes = e_userSerializer(many=True, read_only=True)
	downvotes = e_userSerializer(many=True, read_only=True)
	comment_permission = e_userSerializer(many=True, read_only=True)
	class Meta:
		model = topic
		fields = ('t_id', 'creator','created_at', 'issue', 'hash_tag', 'upvotes', 'downvotes','comment_permission','topic_type')

class editor_pickSerializer(serializers.ModelSerializer):
	editor_topics = topicSerializer(many=True, read_only=True)
	class Meta:
		model = editor_pick
		fields = ('editor_topics','score')