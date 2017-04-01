"""unbubble URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from views import login,verifylogin,get_topic_set,get_topic,get_analysis,get_premium_topic,post_topic,post_comment,topic_upvote,topic_downvote,get_topic_by_user

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^auth/', include('rest_framework_social_oauth2.urls')),
    url(r'^api/login', login),
    url(r'^api/verifylogin', verifylogin),
    url(r'^api/get/topic_set', get_topic_set),
    url(r'^api/get/topic', get_topic),
    url(r'^api/get/user_topics', get_topic_by_user),
    #url(r'^api/get/comments/', get_comments),
    url(r'^api/get/analysis', get_analysis),
    url(r'^api/get/trending_tweets', verifylogin),
    url(r'^api/get/trending_news', verifylogin),
    url(r'^api/get/premium_topic', get_premium_topic),
    url(r'^api/post/topic', post_topic),
    url(r'^api/post/comment', post_comment),
    url(r'^api/topic/upvote', topic_upvote),
    url(r'^api/topic/downvote', topic_downvote),
]
