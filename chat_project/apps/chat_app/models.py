from django.db import models

class GroupModel(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'chat_app'

class ChatModel(models.Model):
    content = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now=True)
    group = models.ForeignKey(GroupModel, on_delete=models.CASCADE)

    class Meta:
        app_label = 'chat_app'
