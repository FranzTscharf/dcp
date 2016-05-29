# -*- coding: utf-8 -*-
from django.views.generic import View
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.http import urlencode
from django.contrib.auth.decorators import login_required
from dcpcontainer import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Message
from .forms import sendMessage
from django.core.urlresolvers import reverse,reverse_lazy
from django.db import IntegrityError
# The authentification for the login of the user
# Beispiel-View. Bitte beim Erstellen einer Seite selbstständig hinzufügen!  
#   
#class Login(View):
#    template = 'dcp/login.html'
#   
#    def get(self, request):
#        params = {}
#        return render(request, self.template, params)
#   
#   def post ist analog

def getPageAuthenticated(request, template, params={}):
    if request.user.is_authenticated():
        return render(request, template, params)
    else:
        return HttpResponseRedirect("login/")

class Register(View):
    def post(self, request):
        if not request.user.is_authenticated():
            if request.method == "POST":
                username = request.POST['username']
                password = request.POST['password']
                email = request.POST['email']
                obj = User.objects.filter(username=username)
                if obj:
                    return HttpResponse('User already exists') # Wie kann man das schön darstellen?
                user = User.objects.create_user(username, email, password)
                user.save()
                return HttpResponseRedirect("/login/")

class Login(View):
   template = 'dcp/content/spezial/login.html'
   
   def get(self, request):
        params = {}
        return render(request, self.template, params)   
        
   def post(self, request):
       if request.method == "POST":
           username = request.POST['username']
           password = request.POST['password']
           valid = bool(False)
           user = authenticate(username=username, password=password)
           if user is not None:
               if user.is_active:
                   login(request, user)
                   return HttpResponseRedirect("/")
               else:
                   return HttpResponse("Inactive user.")
           else:
               return render(request, self.template, {'notVaild': valid})
       return render(request, self.template, {})

class Logout(View):
    def get(self, request):
        if request.user.is_authenticated():
            logout(request)
            return HttpResponseRedirect("../login/")

class Index(View):
    template = 'dcp/index.html'

    def get(self, request):
        return getPageAuthenticated(request, self.template)

    def post(self, request):
        if request.user.is_authenticated():
            params = {}
            return render(request, 'dcp/index.html', params)
        else:
            return HttpResponseRedirect("login/")

class Suchen(View):
    template = 'dcp/content/suchen/suchen.html'

    def get(self, request):
        return getPageAuthenticated(request, self.template)
   
   
class Suchen_Materielles(View):
    template = 'dcp/content/suchen/materielles.html'

    def get(self, request):
        return getPageAuthenticated(request, self.template)

    def post(self, request):
        params = {}
        return render(request, self.template, params)

class Suchen_Immaterielles(View):
    template = 'dcp/content/suchen/immaterielles.html'

    def get(self, request):
        return getPageAuthenticated(request, self.template)


class Suchen_Personen(View):
    template = 'dcp/content/suchen/personen.html'

    def get(self, request):
        return getPageAuthenticated(request, self.template)

class Chat(View):
    form_class = sendMessage
    template = 'dcp/content/chat/chat.html'
    initial = {'Text': 'Bitte Nachricht eingeben'}
    def get(self,request):
        # Hole die "andere" User Id
        otherId = request.GET['userid']
        currentUser = request.user
        otherUser = User.objects.get(id=otherId) #TODO: Exception einbauen!!!!
        # Ok, fremdschlüssel sind da, nun die Liste holen:
        chats = (Message.objects.filter(From=otherUser.id,To=currentUser) | Message.objects.filter(From=currentUser,To=otherUser)).order_by('SendTime') # Filtern und Sortieren
        form = self.form_class(initial=self.initial)
        return render(request,self.template,context={'message_list':chats,'otherUser':otherUser,'currentUser':currentUser,'form':form})
    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            message = form.cleaned_data['Text']
            otherId = request.GET['userid']
            currentUser = request.user
            otherUser = User.objects.get(id=otherId)  # TODO: Exception einbauen!!!!
            Message.objects.create(Text=message,From=currentUser,To=otherUser)
            url = url_with_querystring(reverse('dcp:Chat'),userid=otherUser.id)
            return HttpResponseRedirect(url)
            #Neuer Eintrag in der Datenbank:
def url_with_querystring(path, **kwargs):
    return path + '?' + urlencode(kwargs)