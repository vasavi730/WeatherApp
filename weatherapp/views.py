from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from weatherapp.models import userDetails
import json
from urllib.request import urlopen

# Create your views here.



def home(request):
    return render(request, "homepage.html")


@csrf_exempt
def savemail(request):
    first_name = request.POST.get("fname")
    last_name = request.POST.get("lname")
    mail = request.POST.get("email")
    user = userDetails(firstName=first_name, lastName=last_name, email=mail)
    user.save()
    return render(request, "thank.html")


@csrf_exempt
def displayWeather(request):
    city = request.POST.get("city")
    url = 'http://api.openweathermap.org/data/2.5/forecast?q='
    url+= city
    url+='&cnt=7&APPID=b7174ad2b2d6ef9d181c73572502ee83'
    json_url = urlopen(url)
    data = json.loads(json_url.read())
    data1=''
    lst=[]
    for i in data['list']:
        w={
            'temp':str(i['main']['temp']),
            'mn' :str(i['main']['temp_min']),
            'mx':str(i['main']['temp_max']),
            'pressure':str(i['main']['pressure']),
            'hum':str(i['main']['humidity']) ,
            'desc':str(i['weather'][0]['description']),
            'speed':str(i['wind']['speed']),
            'icon':i['weather'][0]['icon'],
            'date':str(i['dt_txt']),
        }
        
        
         
        lst.append(w)

    request.session['l'] = lst

    return render(request,'display.html',context={'lst':lst,'city':city})
        

# This is function for senting mail out - Commenting it out for a CronJOb - siva
@csrf_exempt
def sendmail(request):
    touser = request.POST.get("t")
    sub = 'Weather alert'
    bod = 'Hello sir/ madam,'
    bod+='Here is to inform that you may have rain in the coming two days.'
    bod+='So be alert and stay safe. Thanks for subscribing us!'
    efrom = settings.EMAIL_HOST_USER
    reclist = [
        touser,
    ]
    msg = "Mail Delivered"
    lst = request.session['l']
    for w in lst:
        if w['desc']=='light rain' or w['desc']=='moderate rain':
            send_mail(sub, bod, efrom, reclist)
            msg='Mail Sent!'

    
    
    return render(request,'thank.html')
 