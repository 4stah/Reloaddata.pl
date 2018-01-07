# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from auditlog.registry import auditlog
from django.db import models
from django.utils.translation import ugettext_lazy as _


# Create your models here.
class caliber (models.Model):
    caliber = models.CharField(verbose_name=_("Kaliber"),max_length=20)
    comment = models.TextField(verbose_name=_("Komentarz"),max_length=125, blank=True, default='')
    user = models.ForeignKey('auth.User', on_delete=models.PROTECT, verbose_name=_("Właściciel"))
    date = models.DateTimeField(verbose_name=_("Data"),auto_now_add=True)
    datemod = models.DateTimeField(verbose_name=_("Data Mod."),auto_now=True)

    def __unicode__(self):
        return self.caliber
    class Meta:
        ordering = ['caliber']

auditlog.register(caliber)

class diameter (models.Model): #all bullets diameters
    diameter = models.CharField(verbose_name=_("Kalibracja [in]"),max_length=5,unique=True, blank=False)
    comment = models.TextField(verbose_name=_("Komentarz"),max_length=125, blank=True, default='')
    user = models.ForeignKey('auth.User', on_delete=models.PROTECT, verbose_name=_("Właściciel"))
    date = models.DateTimeField(verbose_name=_("Data"),auto_now_add=True)
    datemod = models.DateTimeField(verbose_name=_("Data Mod."),auto_now=True)

    def __unicode__(self):
        return self.diameter
    class Meta:
        ordering = ['diameter']

auditlog.register(diameter)

class powder (models.Model):
    vendor = models.CharField(verbose_name=_("Producent"),max_length=20)
    powder = models.CharField(verbose_name=_("Proch"),max_length=20)
    comment = models.TextField(verbose_name=_("Komentarz"),max_length=125, blank=True, default='')
    user = models.ForeignKey('auth.User', on_delete=models.PROTECT, verbose_name=_("Właściciel"))
    date = models.DateTimeField(verbose_name=_("Data"),auto_now_add=True)
    datemod = models.DateTimeField(verbose_name=_("Data Mod."),auto_now=True)

    def __unicode__(self):
      return self.vendor+' '+self.powder
    class Meta:
        ordering = ['vendor','powder']

auditlog.register(powder)


class bullet (models.Model):
    # caliber = models.ForeignKey(caliber, on_delete=models.CASCADE, verbose_name=_("Kaliber"))
    vendor = models.CharField(verbose_name=_("Producent"), max_length=20)
    bullet = models.CharField(verbose_name=_("Pocisk"),max_length=20)
    weight = models.DecimalField(verbose_name=_("Waga [gr]"),max_digits=3, decimal_places=0)
    diameter = models.ForeignKey(diameter, on_delete=models.PROTECT, verbose_name=_("Kalibracja [in]"))
    # calibration  = models.CharField(verbose_name=_("Kalibracja [in]"),max_length=5)
    length = models.DecimalField(verbose_name=_("Długość [mm]"),max_digits=5, decimal_places=2)
    bc = models.DecimalField(verbose_name=_("BC"),max_digits=5, decimal_places=3, null=True,blank=True)
    comment = models.TextField(verbose_name=_("Komentarz"),max_length=125, blank=True, default='')
    user = models.ForeignKey('auth.User', on_delete=models.PROTECT, verbose_name=_("Właściciel"))
    date = models.DateTimeField(verbose_name=_("Data"),auto_now_add=True)
    datemod = models.DateTimeField(verbose_name=_("Data Mod."),auto_now=True)

    def __unicode__(self):
        return (self.vendor)+' ' +(self.bullet)+' '+str(self.weight)+'gr' #TODO + ' (' + self.diameter + ')'
    class Meta:
        ordering = ['vendor','diameter','weight']

auditlog.register(bullet)

class quality (models.Model):
    quality = models.CharField(verbose_name=_("Przeznaczenie"),max_length=20)
    def __unicode__(self):
        return unicode(_(self.quality))
    class Meta:
        ordering = ['quality']


class score (models.Model):
    score = models.CharField(verbose_name=_("Ocena"),max_length=20)
    def __unicode__(self):
        return unicode(_(self.score))

class loads (models.Model):
    date = models.DateTimeField(verbose_name=_("Data"),auto_now_add=True)
    datemod = models.DateTimeField(verbose_name=_("Data Mod."),auto_now=True)
    caliber = models.ForeignKey(caliber, on_delete=models.PROTECT, verbose_name=_("Kaliber"))
    gun = models.CharField(verbose_name=_("Broń"),max_length=30, blank=True, default='')
    bullet = models.ForeignKey(bullet, on_delete=models.PROTECT, verbose_name=_("Pocisk"))
    powder = models.ForeignKey(powder, on_delete=models.PROTECT, verbose_name=_("Proch"))
    COL = models.DecimalField(verbose_name=_("COL [mm]"),max_digits=5, decimal_places=2)
    load = models.DecimalField(verbose_name=_("Naważka [gr]"),max_digits=5, decimal_places=2)
    crimp = models.DecimalField(verbose_name=_("Crimp [mm]"),max_digits=5, decimal_places=2, null=True,blank=True)
    prime = models.CharField(verbose_name=_("Spłonka"),max_length=16, blank=True, default='')
    case = models.CharField(verbose_name=_("Łuska"),max_length=16, blank=True, default='')
    quality = models.ForeignKey(quality, on_delete=models.PROTECT,verbose_name=_("Przeznaczenie"))
    votes = models.IntegerField(verbose_name=_("Głosy"),default=0)
    user = models.ForeignKey('auth.User', on_delete=models.PROTECT, verbose_name=_("Właściciel"))
    def __unicode__(self):
        return str(self.id)

auditlog.register(loads)

class comment (models.Model):
    load = models.ForeignKey(loads, on_delete=models.CASCADE, verbose_name=_("Elaboracja"))
    date = models.DateTimeField(verbose_name=_("Data"),auto_now_add=True)
    datemod = models.DateTimeField(verbose_name=_("Data Mod."),auto_now=True)
    gun = models.CharField(verbose_name=_("Broń"),max_length=50, blank=True, default='')
    comment = models.TextField(verbose_name=_("Komentarz"),max_length=140, blank=False, default='')
    score = models.ForeignKey(score, on_delete=models.PROTECT,verbose_name=_("Ocena"))
    user = models.ForeignKey('auth.User', on_delete=models.PROTECT, verbose_name=_("Właściciel"))
    def __unicode__(self):
        return str(self.load)+' ' + self.comment

auditlog.register(comment)

class test (models.Model):
    load = models.ForeignKey(loads, on_delete=models.CASCADE, verbose_name=_("Elaboracja"))
    date = models.DateTimeField(verbose_name=_("Data"),auto_now_add=True)
    datemod = models.DateTimeField(verbose_name=_("Data Mod."),auto_now=True)
    gun = models.CharField(verbose_name=_("Broń"), max_length=50, blank=True,null=True,default='')
    v0t = models.DecimalField(verbose_name=_("V0 (QL) [m/s]"),blank=True,null=True,max_digits=3, decimal_places=0)
    v0c = models.DecimalField(verbose_name=_("V0 (chrono) [m/s]"),blank=True,null=True,max_digits=3, decimal_places=0)
    temp = models.DecimalField(verbose_name=_("Temp. [C]"), blank=True,null=True,max_digits=3, decimal_places=0)
    moa = models.DecimalField(verbose_name=_("Grupa [MOA]"),max_digits=3, decimal_places=1, blank=True,null=True)
    comment = models.TextField(verbose_name=_("Opis"),max_length=125, blank=True,null=True,default='')
    photo = models.ImageField(verbose_name=_("Zdjęcie"),upload_to="tests/",blank=True,null=True)
    user = models.ForeignKey('auth.User', on_delete=models.PROTECT, verbose_name=_("Właściciel"))
    def __unicode__(self):
        return str(self.id)+' ' + self.comment

auditlog.register(test)
