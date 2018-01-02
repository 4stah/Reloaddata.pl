# -*- coding: utf-8 -*-

from django.conf import settings
from django import forms

from django.forms import EmailField
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template import loader



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
    email = forms.EmailField(label=_("Email:"), required=True, help_text=_(u"Wymagane do odzyskania hasła."))

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class PasswordChangeFormEmail(PasswordChangeForm):
    email = forms.EmailField(label='Email', required=True)

    def __init__(self, user, *args, **kwargs):
        super(PasswordChangeFormEmail,self).__init__(user, *args, **kwargs)  ########### musi byc zawolane najpierw, inaczej NIE DZIAŁA inicjalne załadowanie
        self.fields['email'].initial = user.email

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['new_password1'])
        self.user.email = self.cleaned_data['email']
        if commit:
            self.user.save()
        return self.user


class ContactForm(forms.Form):
    """
    The base contact form class from which all contact form classes
    should inherit.
    """
    name = forms.CharField(max_length=100,label=_(u'Imię / Nickname'))
    email = forms.EmailField(max_length=200,label=_(u'Email'))
    body = forms.CharField(widget=forms.Textarea,label=_(u'Wiadomość'))
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = []
    subject_template_name = "reload/contact_subject.txt"
    message_template_name = "reload/contact_message.txt"

    def __init__(self, data=None, files=None, request=None, recipient_list=None, *args, **kwargs):
        super(ContactForm, self).__init__(data=data, files=files, *args, **kwargs)
        if request is None:
            raise TypeError("Keyword argument 'request' must be supplied")
        if request.user.is_authenticated:
            self.initial['name'] = request.user
            self.initial['email'] = request.user.email
        self.request = request
        if recipient_list is not None:
            self.recipient_list = recipient_list


    def message(self):
        """
        Render the body of the message to a string.
        """
        template_name = self.message_template_name() if callable(self.message_template_name) else self.message_template_name

        return loader.render_to_string(template_name, self.get_context(), request=self.request)

    def subject(self):
        """
        Render the subject of the message to a string.
        """
        template_name = self.subject_template_name() if callable(self.subject_template_name) else self.subject_template_name
        subject = loader.render_to_string(template_name, self.get_context(), request=self.request)
        return ''.join(subject.splitlines())

    def get_context(self):
        """
        Return the context used to render the templates for the email subject and body.
        By default, this context includes:
        * All of the validated values in the form, as variables of the same names as their fields.
        * The current ``Site`` object, as the variable ``site``.
        * Any additional variables added by context processors (this will be a ``RequestContext``).
        """
        if not self.is_valid():
            raise ValueError("Cannot generate Context from invalid contact form")
        return dict(self.cleaned_data, site=get_current_site(self.request))

    def get_message_dict(self):
        """
        Generate the various parts of the message and return them in a
        dictionary, suitable for passing directly as keyword arguments
        to ``django.core.mail.send_mail()``.
        By default, the following values are returned:
        * ``from_email``
        * ``message``
        * ``recipient_list``
        * ``subject``
        """
        if not self.is_valid():
            raise ValueError( "Message cannot be sent from invalid contact form" )
        message_dict = {}
        for message_part in ('from_email', 'message','recipient_list', 'subject'):
            attr = getattr(self, message_part)
            message_dict[message_part] = attr() if callable(attr) else attr

        return message_dict

    def save(self, fail_silently=False):
        """
        Build and send the email message.
        """
        send_mail(fail_silently=fail_silently, **self.get_message_dict())