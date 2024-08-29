from django.db import models
from django.contrib.auth.models import User
import shortuuid

class ChatGroup(models.Model):
    id = models.AutoField(unique=True,primary_key=True)
    groupname = models.CharField(max_length=50, unique=True, default=shortuuid.uuid)
    groupchat_name=models.CharField(max_length=50, null=True, blank=True)
    admin=models.ForeignKey(User, related_name='groupchats', blank=True, null=True, on_delete=models.SET_NULL)
    creat_at = models.DateTimeField(auto_now_add=True)
    users_online = models.ManyToManyField(User, related_name='online_in_groups', blank=True)
    members = models.ManyToManyField(User, related_name='chat_groups', blank=True)
    is_private = models.BooleanField(default=False)

    def __str__(self):
        return self.groupname
    
class GroupMessage(models.Model):
    id = models.AutoField(unique=True, primary_key=True)
    group = models.ForeignKey(ChatGroup, related_name='chat_messages', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author.username} : {self.content}'

    class Meta:
        ordering = ['-created']

class Participants(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chatgroup = models.ForeignKey(ChatGroup, on_delete=models.CASCADE)
    join_at = models.DateTimeField(auto_now_add=True)
    role = models.CharField(max_length=50)
    active = models.BooleanField(default=True)

class Blocks(models.Model):
    id = models.AutoField(unique=True, primary_key=True)
    blocker = models.ForeignKey(User, related_name='blocked_user', on_delete=models.CASCADE)
    blocked = models.ForeignKey(User, related_name='blocked_by', on_delete=models.CASCADE)
    blocked_at = models.DateTimeField(auto_now_add=True)

class Receiption(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.ForeignKey(GroupMessage, on_delete=models.CASCADE)
    chatgroup = models.ForeignKey(ChatGroup, on_delete=models.CASCADE)
    content = models.TextField()

    def save(self, *args, **kwargs):
        if not self.chatgroup:
            self.chatgroup = self.message.group
        if not self.content:
            self.content = self.message.content
        super(Receiption, self).save(*args, **kwargs)
