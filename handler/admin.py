from django.contrib import admin
from models import e_user,comment,topic,editor_pick
# Register your models here.

@admin.register(e_user)
class e_userAdmin(admin.ModelAdmin):
	pass

@admin.register(comment)
class commentAdmin(admin.ModelAdmin):
	pass

@admin.register(topic)
class topicAdmin(admin.ModelAdmin):
	pass

@admin.register(editor_pick)
class editor_pickAdmin(admin.ModelAdmin):
	pass
