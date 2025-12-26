from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Rol, UsuarioRol
from .utils import es_admin, es_socio, obtener_rol_usuario
from django.contrib.auth.hashers import check_password
from appsocios.models import Socio
from appadmincontenido.models import Articulo, Noticia, Reportaje

# usuario admin:claus clave:cfm-1..5

# Create your views here.

def iniciar(request):
    # por el urls.py '' es el primer view que se ejecuta
    #  GET es lo primero que levanta, el formulario de autenticación
    # POST es lo que recibe desde el formulario de iniciar.html method='post' una vez presionado el botón
    if request.method=='GET':
        return render(request,"applogin/iniciar.html",{ 'form': AuthenticationForm() })
    else:
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        
        if not username or not password:
            return render(request, "applogin/iniciar.html",{ 
                'form':AuthenticationForm(), 
                'mensaje':'Por favor completa todos los campos'
            })
        
        # Intenta primero como Admin (Usuario Django)
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        
        # Si falla, intenta como Socio (RUT + contraseña)
        try:
            # Limpiar RUT: remover puntos, guiones y convertir a mayúsculas
            rut_limpio = username.upper().replace('.', '').replace('-', '')
            socio = Socio.objects.get(socio_rut=rut_limpio)
            
            # Verificar contraseña
            if socio.socio_contraseña and check_password(password, socio.socio_contraseña):
                # Crear sesión para el socio
                request.session['socio_id'] = socio.socio_id
                request.session['socio_nombre'] = f"{socio.socio_nombre} {socio.socio_apellido_paterno}"
                request.session['socio_rut'] = socio.socio_rut
                request.session['es_socio_login'] = True
                
                return redirect("appdashboard:home")
            else:
                return render(request, "applogin/iniciar.html",{ 
                    'form':AuthenticationForm(), 
                    'mensaje':'Usuario/RUT o contraseña incorrectos'
                })
        except Socio.DoesNotExist:
            # Si tampoco es socio, mostrar error genérico
            return render(request, "applogin/iniciar.html",{ 
                'form':AuthenticationForm(), 
                'mensaje':'Usuario/RUT o contraseña incorrectos'
            })


def registro(request):  
    if request.method=='GET':        
         return render(request, "applogin/registro.html",{ 'form' : UserCreationForm() })
    else:
        if request.POST["password1"]!=request.POST["password2"]:
            return render(request, "applogin/registro.html",{ 'form' : UserCreationForm(), 'mensaje': "Las contraseñas no coinciden" })
        else:
            name = request.POST["username"]
            password = request.POST["password1"]
            # Validar si el nombre de usuario ya existe
            if User.objects.filter(username=name).exists():
                return render(request, "applogin/registro.html",{ 'form' : UserCreationForm(), 'mensaje': "El nombre de usuario ya está en uso. Elige otro." })
            user = User.objects.create_user(username=name, password=password)
            user.save()
            
            # Asignar rol de administrador por defecto
            rol_admin, _ = Rol.objects.get_or_create(nombre='admin', defaults={'descripcion': 'Administrador'})
            UsuarioRol.objects.create(usuario=user, rol=rol_admin)
            
            return render(request, "applogin/registro.html",{ 'form' : UserCreationForm(), 'mensaje': "Usuario registrado exitosamente. Ya puedes iniciar sesión."})
        
def home(request):
    context = {}
    if request.user.is_authenticated:
        context = {
            'es_admin': es_admin(request.user),
            'es_socio': es_socio(request.user),
            'rol_usuario': obtener_rol_usuario(request.user),
        }
    
    # Obtener contenido reciente (Artículos, Noticias, Reportajes)
    articulos = list(Articulo.objects.all())
    noticias = list(Noticia.objects.all())
    reportajes = list(Reportaje.objects.all())
    
    # Combinar y ordenar por fecha de publicación (más reciente primero)
    contenido_total = articulos + noticias + reportajes
    contenido_total.sort(key=lambda x: x.publicado_en, reverse=True)
    
    # Pasar solo los 3 primeros al template
    context['contenido_destacado'] = contenido_total[:3]
    
    return render(request, "inicio.html", context)        

def salir(request):
    # Limpiar sesión de socio si existe
    if 'es_socio_login' in request.session:
        del request.session['es_socio_login']
    if 'socio_id' in request.session:
        del request.session['socio_id']
    if 'socio_nombre' in request.session:
        del request.session['socio_nombre']
    if 'socio_rut' in request.session:
        del request.session['socio_rut']
    
    # Logout del usuario Django
    logout(request)
    return redirect('home')