from django.contrib.auth import get_user_model
from django.views.generic import View, CreateView, TemplateView
from django.shortcuts import render
from .forms import RegisterForm


User=get_user_model()

def search_view(request):

    qs = User.objects.filter(username__iexact=query)
    context={'object_list':qs}
    return render(request,'result.html',context)


class HomeView(TemplateView):

    def get_context_data(self, **kwargs):
        query = self.request.GET.get('q')
        context = super(HomeView,self).get_context_data(**kwargs)
        print(query)
        if query:
            qs = User.objects.filter(username__iexact=query)
            context['object_list'] = qs
            self.template_name='result.html'
        else:
            self.template_name='home.html'
        return context



class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = '/login'

