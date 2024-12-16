from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from .forms import CustomUserCreationForm, CustomAuthenticationForm, ContactForm  # Formularios personalizados definidos en la aplicación.
from .models import Saga, Personajes, Enemigos  # Modelos definidos en la aplicación.
from django.contrib import messages  # Para manejar mensajes temporales a los usuarios.
from django.urls import reverse  # Para generar URLs a partir de nombres de vistas.
from django.core.mail import EmailMessage  # Para manejar el envío de correos electrónicos.
from django.contrib.auth.models import Group, Permission  # Modelo para manejar grupos y permisos.
from django.contrib.contenttypes.models import ContentType  # Para asignar permisos a los modelos.
from django.core.paginator import Paginator  # Para manejar la paginación de listas.

# Vista para la página de inicio (home)
def index(request):
    return render(request, "core/index.html")  # Renderiza la plantilla "index.html" para la página principal.


# Vista para la página de galería
def galeria(request):
    return render(request, "core/galeria.html")  # Renderiza la plantilla "galeria.html" para la galería de imágenes.


# Vista para la página "Quiénes somos"
def quienes_somos(request):
    return render(request, "core/quienes_somos.html")  # Renderiza la plantilla "quienes_somos.html" para información sobre la organización.


# Vista para la página de noticias
def noticias(request):
    return render(request, "core/noticias.html")  # Renderiza la plantilla "noticias.html" para la sección de noticias.


# Vista para la página de servicios
def servicios(request):
    return render(request, "core/servicios.html")  # Renderiza la plantilla "servicios.html" para mostrar los servicios disponibles.


# Vista para listar todas las sagas
def lista_sagas(request):
    sagas = Saga.objects.all()  # Obtiene todas las sagas desde la base de datos.
    return render(request, 'core/sagas.html', {'sagas': sagas})  # Renderiza la plantilla con la lista de sagas.


# Vista para mostrar información detallada de una saga, personajes y enemigos relacionados.
def informacion(request):
    query = request.GET.get('saga', '')  # Obtiene el nombre de la saga seleccionada desde los parámetros de la URL.
    sagas = Saga.objects.all()  # Obtiene todas las sagas para mostrarlas en un menú desplegable.

    # Filtra personajes y enemigos según la saga seleccionada.
    personajes = Personajes.objects.filter(saga__nombre=query).distinct() if query else None
    enemigos = Enemigos.objects.filter(saga__nombre=query).distinct() if query else None

    return render(request, 'core/informacion.html', {
        'sagas': sagas,
        'personajes': personajes,
        'enemigos': enemigos,
        'query': query,  # Para mantener la saga seleccionada en el desplegable.
    })


# Vista para el registro de un nuevo usuario
def register(request):
    if request.method == 'POST':  # Si se envía el formulario (método POST).
        form = CustomUserCreationForm(request.POST)  # Instancia el formulario con los datos enviados.
        if form.is_valid():  # Valida el formulario.
            user = form.save()  # Guarda el nuevo usuario en la base de datos.
            user.is_staff = True  # Otorga permisos de staff al usuario.
            user.save()  # Guarda los cambios del usuario.

            

            # Función para crear grupos con permisos si no existen.
            def create_group_with_permissions(group_name, model, actions):
                group, created = Group.objects.get_or_create(name=group_name)
                if created:  # Si el grupo fue creado, asignamos permisos.
                    content_type = ContentType.objects.get_for_model(model)
                    for action in actions:
                        perm = Permission.objects.get_or_create(
                            codename=f"{action}_{model._meta.model_name}",
                            content_type=content_type
                        )[0]
                        group.permissions.add(perm)
                return group

            # Asigna el usuario a un grupo según el tipo de usuario seleccionado.
            if user_type == 'admin':
                admin_group = create_group_with_permissions(
                    'Docente',
                    Saga,
                    ['add', 'change', 'delete', 'view']
                )
                user.groups.add(admin_group)
                messages.success(request, "¡Registro exitoso como Docente! Ahora puedes iniciar sesión.")


            elif user_type == 'editor ':
                editor_personajes_group = create_group_with_permissions(
                    'Editor de Personajes',
                    Personajes,
                    ['add', 'change', 'delete', 'view']
                )
                user.groups.add(editor_personajes_group)
                messages.success(request, "¡Registro exitoso como Editor de Personajes! Ahora puedes iniciar sesión.")

            else:  # Para usuarios normales, no asignamos permisos.
                messages.success(request, "¡Registro exitoso! Ahora puedes iniciar sesión.")

            return redirect('login')  # Redirige al inicio de sesión tras el registro.
        else:
            messages.error(request, "Por favor, corrige los errores en el formulario.")  # Muestra mensaje si hay errores.
    else:
        form = CustomUserCreationForm()  # Si no es POST, crea un formulario vacío.

    return render(request, 'registration/register.html', {'form': form})  # Renderiza la plantilla de registro con el formulario.


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





