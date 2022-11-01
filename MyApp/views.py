from django.shortcuts import redirect, render
from .models import *
from django.db.models import Q
from django.contrib import messages

# Create your views here.

# Search 
def index(request): 
    urunler = Urun.objects.all()
    kategoriler = Kategori.objects.all()
    search = ''
    if request.GET.get('search'):
        search = request.GET.get('search')
        urunler = Urun.objects.filter(
            Q(urun_adi__icontains=search) |
            Q(kategori__isim__icontains=search) 
        )
    context = {
        'urunler':urunler,
        'search':search,
        'kategoriler':kategoriler,

    }

    return render(request, 'index.html',context) 

def cart(request): 
    return render(request, 'cart.html') 

def checkout(request): 
    return render(request, 'checkout.html') 

def contact(request): 
    return render(request, 'contact.html')

def shop(request): 
    return render(request, 'shop.html') 

def detail(request): 
    return render(request, 'detail.html')

def pay(request): 
    return render(request, 'pay.html')



# End


def detay(request,id):
    urun = Urun.objects.get(id=id)
    if request.user.is_authenticated:
        if request.method == 'POST':
                print('içerik test')
                urun = request.POST['sepet'] #favori yerine sepet koyabilirsiniz model de böyle olmalı
                if Sepet.objects.filter(user = request.user).exists(): #eğer böyle bir kullanıcı varsa
                    sepet = Sepet.objects.get(user = request.user) #kullanıcıyı al
                    if Sepet.objects.filter(urunler = urun, user = request.user).exists():
                        messages.error(request, 'Bu içerik zaten Sepetinize eklenmiş.')
                        return redirect('index') #yönlendirme
                    sepet.urunler.add(urun) # en sonda eğer eklenmemişse favoriye (sepete) ekler
                    sepet.save()
                    messages.success(request, 'İçerik Sepete  eklendi.')
                    return redirect('index')
                else:
                    sepet = Sepet.objects.create(user = request.user) #eğer sepet hiç oluşmamışsa sepet nesnesi üretilir
                    sepet.urunler.add(urun) #direk olarak sepete ekler
                    sepet.save()#sepeti kaydeder
                    messages.success(request, 'İçerik Sepetinize eklendi.')
                    return redirect('index')
                
        else:
                if request.method == 'POST':
                    messages.error(request, 'İçeriği favorilerinize eklemek için lütfen giriş yapınız veya kaydolunuz.')
                    return redirect('login')
            
    context = {
        'urun':urun,
    }
    return render(request,'cart.html',context)                    