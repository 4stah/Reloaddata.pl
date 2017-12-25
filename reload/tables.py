# -*- coding: utf-8 -*-

import django_tables2 as tables
from django_tables2.utils import A
from django.utils.safestring import mark_safe
from .models import *
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse


class LoadTable_templ(tables.Table):
    id = tables.Column(verbose_name='')
    # id = tables.LinkColumn('load_edit', args=[A('pk')])
    date = tables.DateTimeColumn(verbose_name='Data', format='d-M H:i')
    no_comments = tables.Column(verbose_name=_('Komentarze / Testy'),empty_values=(),orderable=False) #empty_values - zeby nie pomijal w render_FOO

    def render_id (self,record):
        return mark_safe('<a href="/load_edit/%s"> <img src="/static/reload/img/icon-changelink.svg"/></a>' % (record.id))

    def render_no_comments (self,record,column):
        count_c = comment.objects.filter(load=record.id).count()
        count_t = test.objects.filter(load=record.id).count()
        if (count_c + count_t) > 0:
            # return mark_safe('<a href="/load_comment_test/%s"> %s/%s &emsp; <img src="/static/reload/img/search.svg"/></a>' % (record.id, count_c,count_t))
            return mark_safe('<a href=' + reverse("load_comment_test", args=[record.id]) + '> %s/%s &emsp; <img src="/static/reload/img/search.svg"/></a>' % (count_c,count_t))
        # return mark_safe('<a href="/load_comment_test/%s"> <img src="/static/reload/img/icon-addlink.svg"/></a>' % (record.id))
        return mark_safe('<a href=' + reverse("load_comment_test", args=[record.id]) + '> <img src="/static/reload/img/icon-addlink.svg"/></a>')

    class Meta:
        model = loads

class LoadTable(LoadTable_templ):
    class Meta:
        order_by = ('id')
        exclude = ('date','datemod','votes')

class LoadTable_w_n(LoadTable_templ):
    class Meta:
        order_by = ('-date')
        exclude = ('votes','datemod',)


class CommentTable(tables.Table):
    id = tables.Column(verbose_name='')
    # id = tables.LinkColumn('comment_edit', args=[A('pk'),A('load')])
    date = tables.DateTimeColumn(verbose_name=_('Data'),format='d-M H:i')
    # load = tables.LinkColumn('load_comment_test', args=[A('load')],verbose_name='Elaboracja')
    comment = tables.Column(verbose_name=_('Komentarz'), attrs={'td' : {'style' : 'max-width:650px; word-wrap:break-word;'}}) #### to CSS? class name?>

    def render_id (self,record):
        return mark_safe('<a href="/comment_edit/%s/%s"> <img src="/static/reload/img/icon-changelink.svg"/></a>' % (record.id,record.load))

    def render_load (self,record):
        return mark_safe('<a href="/load_comment_test/%s"> <img src="/static/reload/img/search.svg"/></a>' % (record.load))

    class Meta:
        model = comment
        order_by = ('-date')
        exclude = ('datemod',)


class TestTable(tables.Table):
    id = tables.Column(verbose_name='')
    # id = tables.LinkColumn('test_edit', args=[A('pk'),A('load')])
    date = tables.DateTimeColumn(verbose_name=_('Data'),format='d-M H:i')
    # load = tables.LinkColumn('load_comment_test', args=[A('load')],verbose_name='Elaboracja')
    comment = tables.Column(verbose_name=_('Komentarz'),attrs={'td' : {'style' : 'max-width:320px; word-wrap:break-word;'}}) #### to CSS? class name?>

    def render_photo (self,record):
        return mark_safe('<a href="%s"> <img src="%s" height="50px"/></a>' % (record.photo.url,record.photo.url))

    def render_id (self,record):
        return mark_safe('<a href="/test_edit/%s/%s"> <img src="/static/reload/img/icon-changelink.svg"/></a>' % (record.id,record.load))

    def render_load(self, record):
        return mark_safe('<a href="/load_comment_test/%s"> <img src="/static/reload/img/search.svg"/></a>' % (record.load))

    class Meta:
        model = test
        order_by = ('-date')
        exclude = ('datemod',)



class PowderTable(tables.Table):
    id = tables.Column(verbose_name='')
    # id = tables.LinkColumn('powder_edit', args=[A('pk')])
    vendor = tables.Column()
    powder = tables.LinkColumn('load_by_powder', args=[A('pk')])
    no_loads = tables.Column(verbose_name=_('Elaboracji'),empty_values=(),orderable=False) #empty_values - zeby nie pomijal w render_FOO

    def render_no_loads (self,record,column):
        count = loads.objects.filter(powder=record).count()
        if count > 0:
            return mark_safe('<a href=' + reverse("load_by_powder", args=[record.id]) + '> %s &emsp; <img src="/static/reload/img/search.svg"/></a>' % (count))
        return mark_safe('—')

    def render_id (self,record):
        return mark_safe('<a href="/powder_edit/%s"> <img src="/static/reload/img/icon-changelink.svg"/></a>' % (record.id))

    class Meta:
        model = powder
        order_by = ('vendor','powder')
        exclude = ('date','datemod',)


class BulletTable(tables.Table):
    id = tables.Column(verbose_name='')
    # id = tables.LinkColumn('bullet_edit', args=[A('pk')])
    caliber = tables.Column()
    vendor = tables.Column()
    bullet = tables.LinkColumn('load_by_bullet', args=[A('pk')])
    weight = tables.Column()
    calibration = tables.Column()
    length = tables.Column()
    bc = tables.Column()
    no_loads = tables.Column(verbose_name=_('Elaboracji'),empty_values=(),orderable=False) #empty_values - zeby nie pomijal w render_FOO

    def render_no_loads (self,record):
        count = loads.objects.filter(bullet=record).count()
        if count > 0:
            return mark_safe('<a href=' + reverse("load_by_bullet", args=[record.id]) + '> %s &emsp; <img src="/static/reload/img/search.svg"/></a>' % (count))
        return mark_safe('—')

    def render_id (self,record):
        return mark_safe('<a href="/bullet_edit/%s"> <img src="/static/reload/img/icon-changelink.svg"/></a>' % (record.id))

    class Meta:
        model = bullet
        order_by = ('caliber','vendor','calibration','weight')
        exclude = ('date','datemod',)


class CaliberTable(tables.Table):
    id = tables.Column(verbose_name='')
    # id = tables.LinkColumn('caliber_edit', args=[A('pk')])
    caliber = tables.LinkColumn('load_by_caliber', args=[A('pk')])
    no_loads = tables.Column(verbose_name=_('Elaboracji'),empty_values=(),orderable=False) #empty_values - zeby nie pomijal w render_FOO

    def render_id (self,record):
        return mark_safe('<a href="/caliber_edit/%s"> <img src="/static/reload/img/icon-changelink.svg"/></a>' % (record.id))

    def render_no_loads (self,record):
        count = loads.objects.filter(caliber=record).count()
        if count > 0:
            return mark_safe('<a href=' + reverse("load_by_caliber", args=[record.id]) + '> %s &emsp; <img src="/static/reload/img/search.svg"/></a>' % (count))

        return mark_safe('—')

    class Meta:
        model = caliber
        order_by = ('caliber')
        exclude = ('date','datemod')

