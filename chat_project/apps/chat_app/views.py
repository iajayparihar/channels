from django.shortcuts import render
from chat_app.models import ChatModel,GroupModel

def index(request,group_name):
    print('Group name ', group_name)
    group = GroupModel.objects.filter(name=group_name).first()
    chats = []
    if group:
        chats = ChatModel.objects.filter(group = group)
    else:
        GroupModel.objects.create(name=group_name).save()

    return render(request, 'index.html',{'group_name':group_name,'chats':chats})
