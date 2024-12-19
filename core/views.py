from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, authenticate, login
from .forms import CustomUserCreationForm, CustomAuthenticationForm, ContactForm  # Formularios personalizados definidos en la aplicación.
from django.contrib import messages  # Para manejar mensajes temporales a los usuarios.
from django.urls import reverse  # Para generar URLs a partir de nombres de vistas.
from django.core.mail import EmailMessage  # Para manejar el envío de correos electrónicos.
from django.contrib.auth.models import Group, Permission  # Modelo para manejar grupos y permisos.
from django.contrib.contenttypes.models import ContentType  # Para asignar permisos a los modelos.
from django.core.paginator import Paginator  # Para manejar la paginación de listas.
from django.contrib.auth.decorators import user_passes_test, login_required
from .forms import CustomUserCreationForm, DocenteCreationForm
from .models import Curso, CustomUser
from .forms import CursoForm

# Vista para la página de inicio (home)
def index(request):
    return render(request, "core/index.html")  # Renderiza la plantilla "index.html" para la página principal.


# Vista para la página de galería
def galeria(request):
    return render(request, "core/galeria.html")  # Renderiza la plantilla "galeria.html" para la galería de imágenes.


# Vista para la página "Quiénes somos"
def quienes_somos(request):
    return render(request, "core/quienes_somos.html")  # Renderiza la plantilla "quienes_somos.html" para información sobre la organización.



# Vista para la página de servicios
def servicios(request):
    return render(request, "core/servicios.html")  # Renderiza la plantilla "servicios.html" para mostrar los servicios disponibles.




def is_admin(user):
    return user.is_authenticated and user.user_type == 'admin'

def is_docente(user):
    return user.is_authenticated and user.user_type == 'docente'

def is_estudiante(user):
    return user.is_authenticated and user.user_type == 'estudiante'

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@user_passes_test(is_admin)
def crear_docente(request):
    if request.method == 'POST':
        form = DocenteCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_docentes')
    else:
        form = DocenteCreationForm()
    return render(request, 'crear_docente.html', {'form': form})

@user_passes_test(is_estudiante)
def inscribir_curso(request, curso_id):
    curso = Curso.objects.get(id=curso_id)
    curso.estudiantes.add(request.user)
    return redirect('mis_cursos')

@user_passes_test(is_estudiante)
def mis_cursos(request):
    cursos = request.user.cursos_inscritos.all()
    return render(request, 'mis_cursos.html', {'cursos': cursos})

@user_passes_test(is_docente)
def gestionar_curso(request, curso_id):
    curso = Curso.objects.get(id=curso_id)
    # Lógica para editar curso
    return render(request, 'gestionar_curso.html', {'curso': curso})


# Vista para la autenticación de usuarios (inicio de sesión)
def login_view(request):
    if request.method == 'POST':  # Si se envía el formulario de inicio de sesión (método POST).
        form = CustomAuthenticationForm(request, data=request.POST)  # Instancia el formulario con los datos enviados.
        if form.is_valid():  # Valida el formulario.
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)  # Autentica las credenciales del usuario.
            if user is not None:  # Si las credenciales son correctas.
                login(request, user)  # Inicia sesión para el usuario.
                messages.success(request, f"¡Bienvenido, {user.username}! Has iniciado sesión correctamente.")
                return redirect('index')  # Redirige a la página principal.
            else:
                messages.error(request, "Las credenciales son incorrectas.")  # Muestra un mensaje de error si las credenciales no son válidas.
        else:
            messages.error(request, "Por favor, corrige los errores en el formulario.")  # Mensaje de error si el formulario no es válido.
    else:
        form = CustomAuthenticationForm()  # Si no es POST, crea un formulario vacío.

    return render(request, 'registration/login.html', {'form': form})  # Renderiza la plantilla de inicio de sesión con el formulario.


# Vista para cerrar sesión
def logout_view(request):
    logout(request)  # Finaliza la sesión del usuario actual.
    messages.info(request, "Has cerrado sesión exitosamente.")  # Muestra un mensaje informativo.
    return redirect('index')  # Redirige a la página principal.


# Vista para el formulario de contacto
def contacto(request):
    contact_form = ContactForm()  # Crea una instancia vacía del formulario de contacto.

    if request.method == 'POST':  # Si se envía el formulario (método POST).
        contact_form = ContactForm(data=request.POST)  # Instancia el formulario con los datos enviados.

        if contact_form.is_valid():  # Valida el formulario.
            name = request.POST.get('name', '')  # Obtiene el nombre del formulario.
            email = request.POST.get('email', '')  # Obtiene el correo del formulario.
            message = request.POST.get('message', '')  # Obtiene el mensaje del formulario.

            # Configura el correo electrónico.
            email = EmailMessage(
                'Mensaje de contacto recibido',
                'Mensaje enviado por {} <{}>:\n\n{}'.format(name, email, message),
                email,
                ['800e954f00b339@inbox.mailtrap.io'],  # Dirección de destino para pruebas.
                reply_to=[email],
            )

            try:
                email.send()  # Envía el correo electrónico.
                return redirect(reverse('contacto') + '?ok')  # Redirige con un mensaje de éxito si el envío es exitoso.
            except:
                return redirect(reverse('contacto') + '?error')  # Redirige con un mensaje de error si el envío falla.

    return render(request, "core/contacto.html", {'form': contact_form})  # Renderiza la plantilla de contacto con el formulario.

@login_required
def lista_cursos(request):
    cursos = Curso.objects.all()
    return render(request, 'cursos/lista_cursos.html', {'cursos': cursos})

@login_required
@user_passes_test(lambda u: u.user_type == 'estudiante')
def mis_cursos(request):
    cursos = request.user.cursos_inscritos.all()
    return render(request, 'cursos/mis_cursos.html', {'cursos': cursos})

@login_required
@user_passes_test(lambda u: u.user_type == 'docente')
def gestionar_curso(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id, docente=request.user)
    if request.method == 'POST':
        curso.nombre = request.POST.get('nombre')
        curso.descripcion = request.POST.get('descripcion')
        curso.save()
        messages.success(request, 'Curso actualizado exitosamente')
        return redirect('gestionar_curso', curso_id=curso.id)
    return render(request, 'cursos/gestionar_curso.html', {'curso': curso})

@login_required
@user_passes_test(lambda u: u.user_type == 'estudiante')
def inscribir_curso(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    if request.user not in curso.estudiantes.all():
        curso.estudiantes.add(request.user)
        messages.success(request, f'Te has inscrito exitosamente en {curso.nombre}')
    return redirect('mis_cursos')

@login_required
def ambiente(request):
    """Vista que redirige según el tipo de usuario"""
    user_type = request.user.user_type
    if user_type == 'estudiante':
        return redirect('ambiente_estudiante')
    elif user_type == 'docente':
        return redirect('ambiente_docente')
    elif user_type == 'admin':
        return redirect('ambiente_admin')
    else:
        messages.error(request, "Tipo de usuario no válido")
        return redirect('index')

@login_required
def ambiente_estudiante(request):
    """Vista del ambiente del estudiante"""
    cursos_inscritos = request.user.cursos_inscritos.all()
    cursos_disponibles = Curso.objects.exclude(estudiantes=request.user)
    
    context = {
        'cursos_inscritos': cursos_inscritos,
        'cursos_disponibles': cursos_disponibles,
    }
    return render(request, 'core/ambiente_estudiante.html', context)

@login_required
def detalle_curso(request, curso_id):
    """Vista para ver detalles de un curso"""
    curso = get_object_or_404(Curso, id=curso_id)
    context = {
        'curso': curso,
    }
    return render(request, 'core/detalle_curso.html', context)

@login_required
def inscribir_curso(request, curso_id):
    """Vista para inscribirse a un curso"""
    if request.user.user_type != 'estudiante':
        messages.error(request, "Solo los estudiantes pueden inscribirse a cursos")
        return redirect('ambiente')
        
    curso = get_object_or_404(Curso, id=curso_id)
    curso.estudiantes.add(request.user)
    messages.success(request, f"Te has inscrito exitosamente en {curso.nombre}")
    return redirect('ambiente_estudiante')