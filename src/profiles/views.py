from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView, View
from message.models import Message
from django.db.models import Q
from .models import Profile

User=get_user_model()

class ProfileFollowToggle(LoginRequiredMixin, View):
    def post(selfself,request,*args,**kwargs):

        user_to_toggle = request.POST.get("username")
        profile_ = Profile.objects.toggle_follow(request.user,user_to_toggle)

        return redirect("/u/"+user_to_toggle+"/")




class ProfileDetailView(DetailView):

    def get_object(self, queryset=None):
        username = self.kwargs.get("username")
        if username is None:
            raise Http404
        return get_object_or_404(User, username__iexact=username, is_active=True)

    def get_context_data(self, **kwargs):
        context=super(ProfileDetailView,self).get_context_data(**kwargs)

        #print(context, self.request.user)
        if self.request.user.is_authenticated:
            if self.request.user == context.get('user'):
                #print('admin')
                user = self.request.user
                is_following_user_ids = [x.user.id for x in user.is_following.all()]

                qs = Profile.objects.filter(user__id__in=is_following_user_ids).order_by("-updated")

                nqs = Message.objects.filter(user_to=user)
                queryset=set([])

                for x in qs:
                    queryset.add(x.user)

                #print(queryset,nqs)

                for x in nqs:
                    queryset.add(x.user_from)

                #print(queryset)

                if qs.exists():
                    context['users'] = queryset

        return context
