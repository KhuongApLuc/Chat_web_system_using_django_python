from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .models import *
from .forms import *
from django.db.models import Q
from rest_framework.generics import GenericAPIView

@login_required
def chat_view(request, chatroom_name='ncc_chat'):
    chat_group = get_object_or_404(ChatGroup, groupname = chatroom_name)
    chat_messages = chat_group.chat_messages.all()[:30]
    form = ChatmessageCreateForm()

    othe_user = None
    if chat_group.is_private:
        if request.user not in chat_group.members.all():
            raise Http404
        for member in chat_group.members.all():
            if member != request.user:
                othe_user = member
                break

    if chat_group.groupchat_name:
        if request.user not in chat_group.members.all():
            chat_group.members.add(request.user)

    if request.htmx:
        form = ChatmessageCreateForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.author = request.user
            message.group = chat_group
            message.save()

            context = {
                'message': message,
                'user': request.user
            }
            return render(request, 'a_rtchat/partials/chat_message_p.html', context)
    context = {
        'chat_messages': chat_messages, 
        'form': form, 
        'other_user': othe_user, 
        'chatroom_name': chatroom_name,
        'chat_group':chat_group
    }

    return render(request, 'a_rtchat/chat.html', context)

# @login_required
# def chat_view(request,chatroom_name='ncc_chat'):
#     chat_group = get_object_or_404(ChatGroup, groupname=chatroom_name)
#     chat_messages=chat_group.chat_messages.all()[:30]
#     participants = Participants.objects.filter(chatgroup=chat_group, active=True)
    
#     # Tạo danh sách các thành viên trong nhóm
#     mem_in_group = participants.values_list('user', flat=True)
    
#     # Xác định những người không thể đọc tin nhắn
#     blocked_users = Blocks.objects.filter(blocker=request.user).values_list('blocked', flat=True)
#     blockers = Blocks.objects.filter(blocked=request.user).values_list('blocker', flat=True)

#     # Kết hợp hai danh sách lại thành một tập hợp
#     can_not_read = set(blocked_users) | set(blockers)
    
#     # Lọc người dùng có thể nhận tin nhắn
#     receivable_users = set(mem_in_group) - set(can_not_read)

#     # Tạo tin nhắn và lưu vào bảng Receiption cho các người dùng có thể nhận
#     if request.htmx:
#         form = ChatmessageCreateForm(request.POST)
#         if form.is_valid():
#             message = form.save(commit=False)
#             message.author = request.user
#             message.group = chat_group
#             message.save()

#             # Xác định các người dùng nhận được tin nhắn
#             for user_id in receivable_users:
#                 Receiption.objects.create(
#                     user_id=user_id,
#                     message=message,
#                     chatgroup=chat_group,
#                     content=message.content
#                 )

#             context = {
#                 'message': message,
#                 'user': request.user
#             }
#             return render(request, 'a_rtchat/partials/chat_message_p.html', context)

#     # Lấy các tin nhắn cho người dùng hiện tại
#     #chat_messages=chat_group.chat_messages.filter(receiption__user=request.user).all()[:30]

#     form = ChatmessageCreateForm()

#     return render(request, 'a_rtchat/chat.html', {'chat_messages': chat_messages, 'form': form, 'groupname':chat_group.groupname})

def get_or_create_chatroom(request, username):
    if request.user.username == username:
        return redirect('home')

    other_user = User.objects.get(username = username)
    my_chatrooms = request.user.chat_groups.filter(is_private=True)

    if my_chatrooms.exists():
        for chatroom in my_chatrooms:
            if other_user in chatroom.members.all():
                chatroom = chatroom
                break
            else:
                chatroom = ChatGroup.objects.create(is_private = True)
                chatroom.members.add(other_user, request.user)
    else:
        chatroom = ChatGroup.objects.create(is_private = True)
        chatroom.members.add(other_user, request.user)

    return redirect('chatroom', chatroom.groupname)

@login_required
def create_groupchat(request):
    form = NewGroupForm()

    if request.method == 'POST':
        form = NewGroupForm(request.POST)
        if form.is_valid():
            new_groupchat=form.save(commit=False)
            new_groupchat.admin = request.user
            new_groupchat.save()
            new_groupchat.members.add(request.user)
            return redirect('chatroom', new_groupchat.groupname)

    context = {
        'form' : form
    }
    return render(request, 'a_rtchat/create_groupchat.html',context)


