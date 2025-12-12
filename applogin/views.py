from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# usuario admin:claus clave:cfm-1..5

# Create your views here.

def iniciar(request):
    # por el urls.py '' es el primer view que se ejecuta
    #  GET es lo primero que levanta, el formulario de autenticación
    # POST es lo que recibe desde el formulario de iniciar.html method='post' una vez presionado el botón
    if request.method=='GET':
        return render(request,"applogin/iniciar.html",{ 'form': AuthenticationForm() })
    else:
        name = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=name, password=password)
        if user is None:
            return render(request, "applogin/iniciar.html",{ 'form':AuthenticationForm(), 'mensaje':'Debe ingresar un usuario o clave correcta'})
        else:
            login(request, user)
            return redirect("home")


def registro(request):  
    if request.method=='GET':        
         return render(request, "applogin/registro.html",{ 'form' : UserCreationForm() })
    else:
        if request.POST["password1"]!=request.POST["password2"]:
            return render(request, "applogin/registro.html",{ 'form' : UserCreationForm(), 'mensaje': "Las contraseñas no coinciden" })
        else:
            name = request.POST["username"]
            password = request.POST["password1"]
            user = User.objects.create_user(username=name, password=password)
            user.save()
            return render(request, "applogin/registro.html",{ 'form' : UserCreationForm(), 'mensaje': "Usuario registrado"})
        
@login_required    
def home(request):   
        return render(request, "home.html")    

def salir(request):
    logout(request)
    return redirect('home')