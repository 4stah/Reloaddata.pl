import django_filters
from django.contrib.auth.models import User

from .models import *


class LoadFilter(django_filters.FilterSet):
    user = django_filters.ChoiceFilter(choices=loads.objects.order_by('user__username').values_list('user__pk','user__username').distinct())
    class Meta:
        model = loads
        fields = ['caliber', 'powder', 'user']

class BulletFilter(django_filters.FilterSet):
    diameter = django_filters.ChoiceFilter(choices=bullet.objects.order_by('diameter__diameter').values_list('diameter__pk','diameter__diameter').distinct())
    user = django_filters.ChoiceFilter(choices=bullet.objects.order_by('user__username').values_list('user__pk','user__username').distinct())
    vendor = django_filters.ChoiceFilter(choices=bullet.objects.order_by('vendor').values_list('vendor','vendor').distinct())
    #user = django_filters.ModelChoiceFilter(queryset=User.objects.all().order_by('username'))
    #vendor = django_filters.ChoiceFilter(choices=set([(o.vendor,o.vendor) for o in bullet.objects.all()]))

    class Meta:
        model = bullet
        fields = ['vendor', 'diameter', 'user']

class PowderFilter(django_filters.FilterSet):
    user = django_filters.ChoiceFilter(choices=powder.objects.order_by('user__username').values_list('user__pk','user__username').distinct())
    vendor = django_filters.ChoiceFilter(choices=powder.objects.order_by('vendor').values_list('vendor','vendor').distinct())
    # powder = django_filters.ChoiceFilter(choices=powder.objects.order_by('powder').values_list('powder','powder').distinct())

    class Meta:
        model = powder
        fields = ['vendor', 'user']