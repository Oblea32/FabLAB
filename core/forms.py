# Importamos los módulos necesarios de Django para manejar formularios.
from django import forms  # Módulo de Django para crear y manejar formularios.
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm  # Formularios estándar de Django para registro y autenticación.
from django.contrib.auth.models import User  # Modelo de usuario predeterminado de Django.


# Formulario personalizado para la creación de un usuario
class CustomUserCreationForm(UserCreationForm):  
    # Campo adicional para capturar el correo electrónico del usuario (requerido).
    email = forms.EmailField(required=True, label="Correo Electrónico")
    # Campo para capturar el nombre del usuario (requerido).
    first_name = forms.CharField(max_length=100, required=True, label="Nombre")
    # Campo para capturar el apellido del usuario (requerido).
    last_name = forms.CharField(max_length=100, required=True, label="Apellido")

    # Campo para seleccionar el tipo de usuario con opciones predefinidas.
    user_type = forms.ChoiceField(
        choices=[
            ('normal', 'Normal'), 
            ('administrador juegos', 'Administrador de Juegos'), 
            ('editor enemigos', 'Editor de Enemigos'), 
            ('editor personajes', 'Editor de Personajes')
        ],  
        widget=forms.RadioSelect,  # Usa botones de opción (radio buttons) para la selección.
        required=True,
        label="Tipo de Usuario",
    )

    class Meta:
        model = User  # Basado en el modelo `User` de Django.
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'user_type']  # Campos incluidos en el formulario.

    # Sobrescribe el método `save` para incluir campos adicionales.
    def save(self, commit=True):  
        user = super().save(commit=False)  # Llama al método `save` de la clase padre, sin guardar aún en la base de datos.
        user.email = self.cleaned_data.get('email')  # Asigna el correo electrónico al usuario.
        user.first_name = self.cleaned_data.get('first_name')  # Asigna el nombre al usuario.
        user.last_name = self.cleaned_data.get('last_name')  # Asigna el apellido al usuario.

        if commit:  # Si `commit` es True, guarda el usuario en la base de datos.
            user.save()

        return user  # Devuelve la instancia de usuario creada.


# Formulario personalizado para el inicio de sesión (autenticación)
class CustomAuthenticationForm(AuthenticationForm):  
    # Personalización del campo de nombre de usuario con etiqueta y longitud máxima.
    username = forms.CharField(label='Nombre de usuario', max_length=150)
    # Personalización del campo de contraseña con etiqueta y widget para ocultar caracteres.
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)

    class Meta:
        model = User  # Basado en el modelo `User` de Django.
        fields = ['username', 'password']  # Campos incluidos en el formulario.


# Formulario para el contacto
class ContactForm(forms.Form):  
    # Campo obligatorio para nombre y apellido, con validación de longitud y diseño con Bootstrap.
    name = forms.CharField(
        label='Nombre y Apellido', 
        required=True,
        min_length=5, 
        max_length=25, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese sus datos'})
    )

    # Campo obligatorio para correo electrónico, con validación y diseño con Bootstrap.
    email = forms.EmailField(
        label="Correo", 
        required=True,
        max_length=50, 
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su E-mail'})
    )

    # Campo obligatorio para el mensaje, con validación de longitud máxima y diseño con Bootstrap.
    message = forms.CharField(
        label="Mensaje", 
        required=True,
        max_length=500, 
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Escriba aquí su mensaje', 'rows': 5})
    )
