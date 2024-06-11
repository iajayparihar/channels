from django.shortcuts import render

def index(request,group_name):
    print('Group name ', group_name)
    return render(request, 'index.html',{'group_name':group_name})
