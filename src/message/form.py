from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields=['message']

    def __init__(self,*args,**kwargs):
        self.user_from = kwargs.pop('user_from')
        self.user_to = kwargs.pop('user_to')
        print(f'from {self.user_from} to  {self.user_to}')
        super(MessageForm,self).__init__(*args, **kwargs)



    def save(self, commit=True):
        message = Message()
        message.message = self.cleaned_data['message']
        message.user_from=self.user_from
        message.user_to=self.user_to
        #print(f'from {message.user_from} to  {message.user_to}')
        message.save()
