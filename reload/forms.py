from django import forms

from django.forms import EmailField
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import powder
from .models import bullet
from .models import caliber
from .models import loads
from .models import comment
from .models import test

class LoadForm(forms.ModelForm):
    class Meta:
        model = loads
        fields = '__all__'
        exclude = ['votes','user']


class CommentForm(forms.ModelForm):
    class Meta:
        model = comment
        fields = '__all__'
        exclude = ['load','user']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4, 'cols': 19}),
        }


class TestForm(forms.ModelForm):
    class Meta:
        model = test
        fields = '__all__'
        exclude = ['load','user']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4, 'cols': 19}),
        }


class PowderForm(forms.ModelForm):
    class Meta:
        model = powder
        fields = '__all__'
        exclude = ['user']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4, 'cols': 19}),
        }


class BulletForm(forms.ModelForm):
    class Meta:
        model = bullet
        fields = '__all__'
        exclude = ['user']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4, 'cols': 19}),
        }


class CaliberForm(forms.ModelForm):
    class Meta:
        model = caliber
        fields = '__all__'
        exclude = ['user']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4, 'cols': 19}),
        }

class UserCreationForm(UserCreationForm):
    email = EmailField(label=_("Email adres"), required=True, help_text=_("Wymagane do odzyskania hasla."))

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user