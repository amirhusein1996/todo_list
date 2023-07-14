from django import forms
from .models import ContactUsMessage

class ContactUsModelForm(forms.ModelForm):
    # subject = forms.CharField(max_length=100)
    class Meta:
        model = ContactUsMessage
        fields = ['subject' , 'message']

        widgets = {
            'subject':forms.TextInput(attrs={'class': 'form-control'}),
            'message':forms.Textarea(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        """ added user attribute to check if user is not logged in,
         dynamically Email field will be included"""
        super(ContactUsModelForm, self).__init__(*args, **kwargs)
        if not user or not user.is_authenticated:
            self.fields['email'] = forms.EmailField(required=True,
                                                    widget=forms.EmailInput(
                                                        attrs={
                                                            'class': 'form-control'
                                                            }
                                                        )
                                                    )

