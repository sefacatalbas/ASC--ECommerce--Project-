from django.db import models
from django.forms import ModelForm
from django.conf import settings
from email.policy import default
from django.db import models
from user.views import *
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.db.models.signals import post_save,m2m_changed
from django.dispatch import receiver
# Create your models here.


class Kategori(models.Model):
    isim = models.CharField(max_length=100)
    def __str__(self):
        return self.isim
class Subcategory(models.Model):
    isim = models.CharField(max_length=100)
    def __str__(self):
        return self.isim
class SeriNo(models.Model):
    no = models.CharField(max_length= 50)
    def __str__(self):
        return self.no
class Urun(models.Model):
    kategori = models.ForeignKey(Kategori,on_delete=models.CASCADE,null = True)
    subcategories = models.ManyToManyField(Subcategory)
    no = models.OneToOneField(SeriNo,on_delete=models.SET_NULL,null = True)
    urun_adi = models.CharField(max_length=100,null = True,blank = True)
    urun_aciklama = models.CharField(max_length=100,null = True,blank = True)
    urun_fiyat = models.IntegerField(null = True,blank = True)
    urun_ekipman = models.CharField(max_length=100,null = True,blank = True)
    urun_marka = models.CharField(max_length=100,null = True,blank = True)
    resim = models.FileField(upload_to='urunler/',null = True,blank = True)
    urun_firma = models.CharField(max_length=100,null = True,blank = True)
    def __str__(self):
        return self.urun_adi


class Sepet(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null = True)
    urunler = models.ManyToManyField(Urun)
    adet = models.IntegerField(null = True,blank = True)
    fiyat = models.IntegerField(null = True,blank = True)
    is_deleted = models.BooleanField(default=False)
    def _str_(self):
        return self.user.username
    @property
    def fiyat(self):
        return (self.urun.urun_fiyat)
    @property
    def tutar(self):
        return (self.adet * self.urun.urun_fiyat)