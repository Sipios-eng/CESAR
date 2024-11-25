from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, Rol

class RegistroUsuarioForm(UserCreationForm):
    email = forms.EmailField(required=True)
    telefono = forms.CharField(max_length=20, required=False)
    rol = forms.ModelChoiceField(queryset=Rol.objects.all(), required=True)

    class Meta:
        model = Usuario
        fields = ('username', 'email', 'telefono', 'password1', 'password2', 'rol')
