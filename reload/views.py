# -*- coding: utf-8 -*-

from django.shortcuts import render,redirect

from django_tables2 import RequestConfig, SingleTableMixin
from django_filters.views import FilterView

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from django.contrib.contenttypes.models import ContentType

from django.http import HttpResponseRedirect

from hitcount.models import HitCount
from hitcount.views import HitCountMixin

from django.utils.translation import ugettext_lazy as _

from django.views.generic.edit import FormView


from .models import *
from .forms import *
from .tables import *
from .filters import *


# Class

class LoadFilteredTable(SingleTableMixin, FilterView):
    table_class = LoadTable
    filterset_class = LoadFilter
    template_name = 'reload/view.html'
    table_pagination = {'per_page': 15}
    title = _('Baza elaboracji')
    def dispatch(self, request, *args, **kwargs):
        hit_count, created = HitCount.objects.get_or_create(content_type=ContentType.objects.get_for_model(loads),
                                                            object_pk=0)  # małe oszustwo: ustawiam pk=0 - dla wszystkich pk w loads
        hit_count_response = HitCountMixin.hit_count(request, hit_count)
        return super(LoadFilteredTable, self).dispatch(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super(LoadFilteredTable, self).get_context_data(**kwargs)
        context.update({'title': self.title})
        return context

class BulletFilteredTable(SingleTableMixin, FilterView):
    table_class = BulletTable
    filterset_class = BulletFilter
    template_name = 'reload/view.html'
    table_pagination = {'per_page': 15}
    title = _(u'Baza pocisków')
    def get_context_data(self, **kwargs):
        context = super(BulletFilteredTable, self).get_context_data(**kwargs)
        context.update({'title': self.title})
        return context

class PowderFilteredTable(SingleTableMixin, FilterView):
    table_class = PowderTable
    filterset_class = PowderFilter
    template_name = 'reload/view.html'
    table_pagination = {'per_page': 15}
    title = _('Baza prochu')
    def get_context_data(self, **kwargs):
        context = super(PowderFilteredTable, self).get_context_data(**kwargs)
        context.update({'title': self.title})
        return context

# https://wsvincent.com/django-contact-form/
# https://django-contact-form.readthedocs.io/en/1.4.2/

class ContactFormView(FormView):
    form_class = ContactForm
    recipient_list = ['admin@reloaddata.pl']
    template_name = "reload/contact.html"

    def form_valid(self, form):
        form.save()
        return super(ContactFormView, self).form_valid(form)

    def get_form_kwargs(self):
        # ContactForm instances require instantiation with an
        # HttpRequest.
        kwargs = super(ContactFormView, self).get_form_kwargs()
        kwargs.update({'request': self.request})

        # We may also have been given a recipient list when
        # instantiated.
        if self.recipient_list is not None:
            kwargs.update({'recipient_list': self.recipient_list})
        return kwargs

    def get_success_url(self):
        # This is in a method instead of the success_url attribute
        # because doing it as an attribute would involve a
        # module-level call to reverse(), creating a circular
        # dependency between the URLConf (which imports this module)
        # and this module (which would need to access the URLConf to
        # make the reverse() call).
        return reverse('contact_sent')

##############
# views here #
##############


def index(request):
    user_count = User.objects.all().count()
    loads_count = loads.objects.all().count()
    return render(request, 'reload/index.html',{'user_count':user_count,'loads_count':loads_count})

#---------------------------
def loginuser(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'POST':
            form = AuthenticationForm(data=request.POST)
            if form.is_valid:
                user = request.POST['username']
                password = request.POST['password']
                access = authenticate(request, username=user, password=password)
                if access is not None:
                    login(request, access)
                    if access.is_active:
                        hit_count, created = HitCount.objects.get_or_create(
                            content_type=ContentType.objects.get_for_model(User),
                            object_pk=0)  # małe oszustwo: ustawiam pk=0 - dla wszystkich pk w user
                        hit_count_response = HitCountMixin.hit_count(request, hit_count)
                        hit_count = HitCount.objects.get_for_object(User.objects.get(username=user)) # hit_count dla poszczególnych wierszy (kluczy)
                        hit_count_response = HitCountMixin.hit_count(request, hit_count)

                        next_url = request.GET.get('next')
                        if next_url and not next_url[4:][:10]=='logoutuser':
                            return redirect(next_url)
                        else:
                            return redirect('index')
        else:
            form = AuthenticationForm()
        return render(request, 'reload/login.html',{'form': form})


#---------------------------
def password_change(request):
    if not request.user.is_authenticated:
        return redirect('loginuser')
    if request.method == "POST":
        form = PasswordChangeFormEmail(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect(index)
    else:
        form = PasswordChangeFormEmail(request.user)
    return render(request, 'reload/password_change.html', {'form': form,})


#---------------------------
def create_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            access = authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password1'))
            login(request, access)
            return HttpResponseRedirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'reload/create_user.html', {'title':_('Rejestracja'),'form': form})


############################
#---------------------------
# def loaddata(request):
#     table = LoadTable(loads.objects.all())
#
#     #hit_count = HitCount.objects.get_for_object(loads.objects.get(pk=3)) # hit_count dla poszczególnych wierszy (kluczy)
#     hit_count, created = HitCount.objects.get_or_create(content_type=ContentType.objects.get_for_model(loads),object_pk=0) # małe oszustwo: ustawiam pk=0 - dla wszystkich pk w loads
#     hit_count_response = HitCountMixin.hit_count(request, hit_count)
#
#     RequestConfig(request, paginate={'per_page': 20}).configure(table)  # dodatkowo, żeby reagował na sortowanie
#     return render(request, 'reload/view.html', {'title':'Baza elaboracji','table': table})

#---------------------------
def load_new(request):
    if not request.user.is_authenticated:
        return redirect('loginuser')
    if request.method == 'POST':
        form = LoadForm(request.POST)
        if form.is_valid():
            update_user = form.save(commit=False)
            update_user.user = request.user
            update_user.save()
            return redirect('loads')
    else:
        form = LoadForm()
    return render(request, 'reload/edit.html', {'title':_('Edycja elaboracji'),'editable':True,'form': form})

#---------------------------
def load_edit(request,key):
    if not request.user.is_authenticated:
        return redirect('/loginuser?next=%s' % request.path)
    instance = loads.objects.get(id=key)
    if request.method == 'POST':
        if (not instance.user == request.user) and (not request.user.is_superuser):
            return redirect('loads')
        form = LoadForm(request.POST,instance=instance)
        if form.is_valid():
            form.save()
            return redirect('loads')
    else:
        form = LoadForm(instance=instance)
    return render(request, 'reload/edit.html', {'title':_('Edycja elaboracji'),'editable': ((instance.user == request.user) or (request.user.is_superuser)),'form': form})

#---------------------------
def comment_edit(request,key,id_load):
    if not request.user.is_authenticated:
        return redirect('/loginuser?next=%s' % request.path)
    instance = comment.objects.get(id=key)
    if request.method == 'POST':
        if (not instance.user == request.user) and (not request.user.is_superuser):
            return redirect('load_comment',id_load)
        form = CommentForm(request.POST,instance=instance)
        if form.is_valid():
            form.save()
            return redirect('load_comment_test',id_load)
    else:
        form = CommentForm(instance=instance)
    return render(request, 'reload/edit.html', {'title':_('Edycja komentarza'),'editable': ((instance.user == request.user) or (request.user.is_superuser)),'form': form})

#---------------------------
def load_comment_test (request,key):
    if not request.user.is_authenticated:
        return redirect('/loginuser?next=%s' % request.path)

    table = LoadTable(loads.objects.filter(id=key))
    table_comment = CommentTable(comment.objects.filter(load=key))
    table_comment.exclude = ('load')
    table_test = TestTable(test.objects.filter(load=key))
    table_test.exclude = ('load')

    RequestConfig(request, paginate={'per_page': 10}).configure(table_comment)
    RequestConfig(request, paginate={'per_page': 10}).configure(table_test)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            update = form.save(commit=False)
            update.user = request.user
            update.load = loads.objects.get(id=key)
            update.save()
            return redirect('load_comment_test',key)
    else:
        form = CommentForm()

    tests = test.objects.all()
    return render(request, 'reload/view_comments_test.html',
                  {'title':_(u'Szczegóły elaboracji'), 'key':key, 'table': table,'table_comment': table_comment,'table_test': table_test,
                   'form':form,
                   'tests':tests})

#---------------------------
def test_new(request,key):
    if not request.user.is_authenticated:
        return redirect('/loginuser?next=%s' % request.path)
    if request.method == 'POST':
        form = TestForm(request.POST,request.FILES)
        if form.is_valid():
            update = form.save(commit=False)
            update.user = request.user
            update.load = loads.objects.get(id=key)
            update.save()
            return redirect('load_comment_test',key)
    else:
        form = TestForm()
    return render(request, 'reload/edit.html', {'title':_('Edycja testu'),'editable':True,'form': form})

#---------------------------
def test_edit(request,key,id_load):
    if not request.user.is_authenticated:
        return redirect('/loginuser?next=%s' % request.path)
    instance = test.objects.get(id=key)
    if request.method == 'POST':
        if (not instance.user == request.user) and (not request.user.is_superuser):
            return redirect('load_comment_test',id_load)
        form = TestForm(request.POST,request.FILES,instance=instance)
        if form.is_valid():
            form.save()
            return redirect('load_comment_test',id_load)
    else:
        form = TestForm(instance=instance)
    return render(request, 'reload/edit.html', {'title':_('Edycja testu'),'editable': ((instance.user == request.user) or (request.user.is_superuser)),'form': form})

#---------------------------

def whats_new(request):
    # if not request.user.is_authenticated:
    #     return redirect('/loginuser?next=%s' % request.path)
    table_l = LoadTable_w_n(list(loads.objects.order_by('-date')[:5]))
    table_c = CommentTable(list(comment.objects.order_by('-date')[:5]))
    table_t = TestTable(list(test.objects.order_by('-date')[:5]))

    hit_count, created = HitCount.objects.get_or_create(content_type=ContentType.objects.get_for_model(loads),
                                                        object_pk=0)  # małe oszustwo: ustawiam pk=0 - dla wszystkich pk w loads
    hit_count_response = HitCountMixin.hit_count(request, hit_count)

    return render(request, 'reload/whats_new.html', {'title':_('Co nowego'),'table_l': table_l,'table_c': table_c,'table_t': table_t})


#---------------------------

def load_by_caliber(request,key):
    if not request.user.is_authenticated:
        return redirect('loginuser')
    table = LoadTable(loads.objects.filter(caliber = caliber.objects.get(pk=key)))
    RequestConfig(request, paginate={'per_page': 20}).configure(table)
    return render(request, 'reload/view.html', {'title':_('Kaliber: ')+caliber.objects.get(pk=key).caliber,'table': table})

def load_by_bullet(request,key):
    if not request.user.is_authenticated:
        return redirect('loginuser')
    table = LoadTable(loads.objects.filter(bullet = bullet.objects.get(pk=key)))
    RequestConfig(request, paginate={'per_page': 20}).configure(table)
    return render(request, 'reload/view.html', {'title':_('Pocisk: ')+bullet.objects.get(pk=key).vendor+' '+bullet.objects.get(pk=key).bullet,'table': table})

def load_by_powder(request,key):
    if not request.user.is_authenticated:
        return redirect('loginuser')
    table = LoadTable(loads.objects.filter(powder = powder.objects.get(pk=key)))
    RequestConfig(request, paginate={'per_page': 20}).configure(table)
    return render(request, 'reload/view.html', {'title':_('Proch: ')+powder.objects.get(pk=key).vendor+' '+powder.objects.get(pk=key).powder,'table': table})


############################
#---------------------------
# def powders(request):
#     table = PowderTable(powder.objects.all())
#     RequestConfig(request).configure(table) # żeby reagował na sortowanie
#     return render(request, 'reload/view.html', {'title':'Baza prochów','table': table})

#---------------------------
def powder_new(request):
    if not request.user.is_authenticated:
        return redirect('/loginuser?next=%s' % request.path)
    if request.method == 'POST':
        form = PowderForm(request.POST)
        if form.is_valid():
            update_user = form.save(commit=False)
            update_user.user = request.user
            update_user.save()
            return redirect('powders')
    else:
        form = PowderForm()
    return render(request, 'reload/edit.html', {'title':_('Edycja prochu'),'editable':True,'form': form})

#---------------------------
def powder_edit(request,key):
    if not request.user.is_authenticated:
        return redirect('/loginuser?next=%s' % request.path)
    instance = powder.objects.get(id=key)
    editable = (instance.user == request.user) or (request.user.is_superuser) #rekord użytkownika
    update_disabled = (loads.objects.filter(powder = instance).exclude(user = instance.user).count()>0) and (not request.user.is_superuser)
    # uniemizliwia edytowanie jesli slownik zostal uzyty przez innych

    if request.method == 'POST':
        if (not editable or update_disabled):
            return redirect('powders')
        form = PowderForm(request.POST,instance=instance)
        if form.is_valid():
            form.save()
            return redirect('powders')
    else:
        form = PowderForm(instance=instance)

    return render(request, 'reload/edit.html', {'title':_('Edycja prochu'),'editable': editable,'update_disabled':update_disabled,'form': form})

############################
#---------------------------
# def bullets(request):
#     table = BulletTable(bullet.objects.all())
#     RequestConfig(request).configure(table) # żeby reagował na sortowanie
#     return render(request, 'reload/view.html', {'title':'Baza pocisków','table': table})

#---------------------------
def bullet_new(request):
    if not request.user.is_authenticated:
        return redirect('/loginuser?next=%s' % request.path)
    if request.method == 'POST':
        form = BulletForm(request.POST)
        if form.is_valid():
            update_user = form.save(commit=False)
            update_user.user = request.user
            update_user.save()
            return redirect('bullets')
    else:
        form = BulletForm()
    return render(request, 'reload/edit.html', {'title':_('Edycja pocisku'),'editable':True,'form': form})

#---------------------------
def bullet_edit(request,key):
    if not request.user.is_authenticated:
        return redirect('/loginuser?next=%s' % request.path)
    instance = bullet.objects.get(id=key)
    editable = (instance.user == request.user) or (request.user.is_superuser)  # rekord użytkownika
    update_disabled = (loads.objects.filter(bullet=instance).exclude(user=instance.user).count() > 0) and (not request.user.is_superuser)
    # uniemizliwia edytowanie jesli slownik zostal uzyty przez innych

    if request.method == 'POST':
        if (not editable or update_disabled):
            return redirect('bullets')
        form = BulletForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('bullets')
    else:
        form = BulletForm(instance=instance)

    return render(request, 'reload/edit.html',
                  {'title': _('Edycja pocisku'), 'editable': editable, 'update_disabled': update_disabled, 'form': form})

############################
#---------------------------
def calibers(request):
    table = CaliberTable(caliber.objects.all())
    RequestConfig(request).configure(table) # żeby reagował na sortowanie
    return render(request, 'reload/view.html', {'title':'Baza kalibrów','table': table})

#---------------------------
def caliber_new(request):
    if not request.user.is_authenticated:
        return redirect('/loginuser?next=%s' % request.path)
    if request.method == 'POST':
        form = CaliberForm(request.POST)
        if form.is_valid():
            update_user = form.save(commit=False)
            update_user.user = request.user
            update_user.save()
            return redirect('calibers')
    else:
        form = CaliberForm()
    return render(request, 'reload/edit.html', {'title':_('Edycja kalibru'),'editable':True,'form': form})

#---------------------------
def caliber_edit(request,key):
    if not request.user.is_authenticated:
        return redirect('/loginuser?next=%s' % request.path)
    instance = caliber.objects.get(id=key)
    editable = (instance.user == request.user) or (request.user.is_superuser)  # rekord użytkownika
    update_disabled = (loads.objects.filter(caliber=instance).exclude(user=instance.user).count() > 0) and (not request.user.is_superuser)
    # uniemizliwia edytowanie jesli slownik zostal uzyty przez innych

    if request.method == 'POST':
        if (not editable or update_disabled):
            return redirect('calibers')
        form = CaliberForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('calibers')
    else:
        form = CaliberForm(instance=instance)

    return render(request, 'reload/edit.html',
                  {'title': _('Edycja kalibru'), 'editable': editable, 'update_disabled': update_disabled, 'form': form})


############################
# TESTOWE
############################
#---------------------------
# class LoadsListView(ListView):
#     model = loads
#     list_display = ('ID','caliber','gun','bullet','powder','COL','load','crimp','prime','case','quality','date','user')
#     fields = ('ID','caliber','gun',)
#     context_object_name = 'loads'
#     queryset = loads.objects.all()
#     template_name = 'reload/loads_list.html'

    # def get_context_data(self, **kwargs):
    #     context = super(LoadsListView, self).get_context_data(**kwargs)
    #     return context



