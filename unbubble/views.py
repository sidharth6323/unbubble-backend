from django.http import JsonResponse
import requests
from requests_oauthlib import OAuth1
import re
from handler.models import e_user,comment,topic,editor_pick
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from handler.serializers import e_userSerializer,commentSerializer,topicSerializer,editor_pickSerializer

url="https://api.twitter.com/oauth/request_token"
auth = OAuth1('DjIa5Ej9dF4v3bVC0RvG24Fus', 'FelsmTj6QQKvNljMTHy06wycnJIEHorMQbgwt7ggB7fayV6OqW','753617411375366144-SiJRtxZ6S2rV8vabVofLoh2oslisVLR','XVQW3pSa0RIxOcuvivuVRiOuUX7HGzzHYjRXPbVnCO8eX')

def login(request):
	r=requests.get(url, auth=auth)
	#print r.json()
	pattern = r'oauth_token=(.*)&oauth_token_secret=(.*)&oauth_callback_confirmed=(.*)'
	response = re.findall(pattern,r.content)
	oauth_token = response[0][0]
	oauth_token_secret = response[0][1]		
	return JsonResponse({"oauth_token":oauth_token});

def verifylogin(request):
	oauth_verifier = request.GET.get("oauth_verifier")
	oauth_token = request.GET.get("oauth_token")
	print oauth_verifier,oauth_token
	url2="https://api.twitter.com/oauth/access_token?oauth_token="+oauth_token+"&oauth_verifier="+oauth_verifier
	response2 = requests.get(url)
	print response2.content

def get_topic_set(request):
	topic_type = request.GET.get("topic_type")
	print topic_type
	if topic_type == "editor":
		f_topics = editor_pick.objects.all()
		serializer = editor_pickSerializer(f_topics, many=True)
	if topic_type == "politics":
		f_topics = topic.objects.filter(topic_type="politics")
		serializer = topicSerializer(f_topics, many=True)
	if topic_type == "tech":
		f_topics = topic.objects.filter(topic_type="tech")
		serializer = topicSerializer(f_topics, many=True)
	if topic_type == "startup":
		f_topics = topic.objects.filter(topic_type="startup")
		serializer = topicSerializer(f_topics, many=True)
	if not topic_type:
		f_topics = topic.objects.all()
		serializer = topicSerializer(f_topics, many=True)
	return JsonResponse(serializer.data, safe=False)

def get_topic(request):
	t_id = request.GET.get("t_id")
	if not t_id:
		return JsonResponse({"error":"t_id not passed"})
	f_topic = topic.objects.get(t_id=t_id)
	serializer = topicSerializer(f_topic)
	return JsonResponse(serializer.data,safe=False)

def get_comments(request):
	t_id = request.GET.get("t_id")
	if not t_id:
		return JsonResponse({"error":"t_id not passed"})
	f_topic = topic.objects.get(t_id=t_id)
	comments = topic.objects.filter(topic=f_topic)
	serializer = commentSerializer(comments,many=True)
	return JsonResponse(serializer.data,safe="False")

def get_analysis(request):
	t_id = request.GET.get("t_id")
	if not t_id:
		return JsonResponse({"error":"t_id not passed"})
	f_topic = topic.objects.get(t_id=t_id)
	male,female,lessthen18,eighteentwo23,twentythreetwo30,greaterthen30 = 0,0,0,0,0,0
	location = {}
	serializer = topicSerializer(f_topic)
	data = dict(serializer.data)
	for i in data["upvotes"]:
		if i["gender"]=="M":
			male+=1
		else:
			female+=1
		if i["age"]<18:
			lessthen18 +=1
		if 18<=i["age"]<=23:
			eighteentwo23 +=1
		if 23<=i["age"]<=30:
			twentythreetwo30 +=1
		if i["age"]>30:
			greaterthen30 +=1
		if i["location"] in location:
			location[i["location"]]+=1
		else:
			location[i["location"]]=1
	return JsonResponse({"gender":{"male":male,"female":female},"location":location,"age":{"lessthen18":lessthen18,"eighteentwo23":eighteentwo23,"twentythreetwo30":twentythreetwo30,"greaterthen30":greaterthen30}})

def get_topic_by_user(request):
	u_id = request.GET.get("u_id")
	print request.GET
	if not u_id:
		return JsonResponse({"error":"t_id not passed"})
	f_user = e_user.objects.get(u_id=u_id)
	f_topic = topic.objects.filter(creator=f_user)
	serializer = topicSerializer(f_topic,many=True)
	return JsonResponse(serializer.data,safe=False)

def get_premium_topic(request):
	t_id = request.GET.get("t_id")
	if not t_id:
		return JsonResponse({"error":"t_id not passed"})
	f_topic = topic.objects.get(t_id=t_id)
	for_user=[]
	against_user=[]
	serializer = topicSerializer(f_topic)
	data = dict(serializer.data)
	for i in data["upvotes"]:
		if i["u_type"]=="premium":
			for_user.append(i)
	for i in data["downvotes"]:
		if i["u_type"]=="premium":
			against_user.append(i)
	return JsonResponse({"for":for_user,"against":against_user})

@csrf_exempt
def post_topic(request):
	if request.method=="POST":
		u_id = request.POST.get("u_id")
		creator = e_user.objects.get(u_id=u_id)
		issue = request.POST.get("issue")
		hash_tag = request.POST.get("hash_tag")
		topic_type = request.POST.get("topic_type")
		if not u_id or not issue or not topic_type:
			return JsonResponse({"error":"not enough arguments passed"})
		if creator.u_type!="hunters":
			return JsonResponse({"error":"User not authorized to Post"})
		f_topic = topic.objects.create(creator=creator,issue=issue,hash_tag=hash_tag,topic_type=topic_type)
		serializer = topicSerializer(f_topic)
		return JsonResponse(serializer.data,safe="False")

@csrf_exempt
def post_comment(request):
	if request.method=="POST":
		u_id = request.POST.get("u_id")
		t_id = request.POST.get("t_id")
		f_topic = topic.objects.get(t_id=t_id) 
		f_user = e_user.objects.get(u_id=u_id)
		t_user  = f_user.user
		body = request.POST.get("body")
		if not u_id or not t_id or not body:
			return JsonResponse({"error":"not enough arguments passed"})
		if not f_topic.comment_permission.filter(user=t_user).exists():
			return JsonResponse({"error":"User not authorized to comment"})
		f_comment = comment.objects.create(user=f_user,topic=f_topic,body=body)
		serializer = commentSerializer(f_comment)
		return JsonResponse(serializer.data,safe="False")

@csrf_exempt
def topic_upvote(request):
	if request.method=="POST":
		u_id = request.POST.get("u_id")
		t_id = request.POST.get("t_id")
		f_topic = topic.objects.get(t_id=t_id) 
		f_user = e_user.objects.get(u_id=u_id)
		t_user = f_user.user
		if f_topic.upvotes.filter(user=t_user).exists():
				f_topic.upvotes.remove(f_user)
		else:
				f_topic.upvotes.add(f_user)
		f_topic.save()
		serializer = topicSerializer(f_topic)
		return JsonResponse(serializer.data)

def topic_downvote(request):
	if request.method=="POST":
		u_id = request.POST.get("u_id")
		t_id = request.POST.get("t_id")
		f_topic = topic.objects.get(t_id=t_id) 
		f_user = e_user.objects.get(u_id=u_id)
		t_user = f_user.users
		if f_topic.downvotes.filter(user=t_user).exists():
				f_topic.downvotes.remove(f_user)
		else:
				f_topic.downvotes.add(f_user)
		f_topic.save()
		serializer = topicSerializer(f_topic)
		return JsonResponse(serializer.data)
