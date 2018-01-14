from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.db.models import Q
from django.core.urlresolvers import reverse

from django.views.generic import ListView, CreateView
from .models import Message
from .form import MessageForm

User=get_user_model()

class MessagesByUserView(CreateView):
    form_class = MessageForm
    template_name = 'message/message_list.html'
    model = Message

    def get_success_url(self):
        return reverse('message',kwargs={'username' :self.kwargs.get('username') })

    def get_form_kwargs(self):
        kwargs = super(MessagesByUserView,self).get_form_kwargs()
        kwargs.update({'user_to': User.objects.filter(username=self.kwargs.get('username')).first()})
        kwargs.update({'user_from': self.request.user})
        #self.success_url = reverse('message',kwargs={'username': self.kwargs.get('username')})
        #kwargs.pop('instance')
        #print(User.objects.filter(username = self.kwargs.get('username')))
        return kwargs


    def get_context_data(self, **kwargs):
        context = super(MessagesByUserView,self).get_context_data(**kwargs)
        context['user_'] = self.kwargs.get('username')
        context['object_list'] = self.get_queryset()
        #print(context,"form - - ")
        return context


    def get_queryset(self):
        user=self.request.user
        user_ = self.kwargs.get('username')

        queryset = Message.objects.filter((Q(user_from=user) & Q(user_to__username=user_) )|
                                          (Q(user_to=user) & Q(user_from__username=user_) )
                                          ).order_by('-pk')
        #print(queryset)
        return queryset