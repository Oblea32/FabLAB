# Importamos los módulos necesarios de Django para manejar formularios.
from django import forms  # Módulo de Django para crear y manejar formularios.
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm  # Formularios estándar de Django para registro y autenticación.
from django.contrib.auth.models import User  # Modelo de usuario predeterminado de Django.
from .models import CustomUser
from django.contrib.auth import get_user_model
CustomUser = get_user_model()
from .models import Curso
from django.contrib.auth import authenticate


class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ['nombre', 'descripcion', 'docente']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'docente': forms.Select(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar solo docentes en el campo docente
        self.fields['docente'].queryset = CustomUser.objects.filter(user_type='docente')

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'estudiante'  # Solo estudiantes pueden registrarse
        if commit:
            user.save()
        return user

class DocenteCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'docente'
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user



# Formulario personalizado para el inicio de sesión (autenticación)
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Nombre de usuario', max_length=150)
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        
        if username and password:
            self.user_cache = authenticate(
                self.request, username=username, password=password
            )
            if self.user_cache is None:
                raise forms.ValidationError(
                    'Usuario o contraseña incorrectos.'
                )
            else:
                if not self.user_cache.is_active:
                    raise forms.ValidationError('Esta cuenta está inactiva.')
        
        return cleaned_data

    class Meta:
        model = User
        fields = ['username', 'password']


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