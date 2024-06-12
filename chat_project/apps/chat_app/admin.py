from django.contrib import admin
from .models import ChatModel, GroupModel

@admin.register(ChatModel)
class ChatAdmin(admin.ModelAdmin):
    '''Admin View for Chat'''

    list_display = ('id','content','timestamp','group')

@admin.register(GroupModel)
class GroupAdmin(admin.ModelAdmin):
    '''Admin View for Group'''

    list_display = ('id','name')