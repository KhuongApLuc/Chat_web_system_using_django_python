from django.contrib import admin
from .models import *

admin.site.register(ChatGroup)
admin.site.register(GroupMessage)
admin.site.register(Participants)
admin.site.register(Blocks)
admin.site.register(Receiption)