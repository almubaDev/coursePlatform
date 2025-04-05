from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, PasswordResetForm, SetPasswordForm, PasswordChangeForm
from django import forms
from django.utils.translation import gettext_lazy as _

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """
    Formulario para crear nuevos usuarios. Incluye todos los campos requeridos,
    más un campo de verificación de contraseña.
    """
    
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aplicar clases de Bootstrap a los campos
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label


class CustomUserChangeForm(UserChangeForm):
    """
    Formulario para actualizar usuarios. Incluye todos los campos de
    CustomUser, pero reemplaza el campo de contraseña con el del widget
    de contraseña del admin.
    """
    
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'profile_picture', 'bio')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aplicar clases de Bootstrap a los campos
        for field_name, field in self.fields.items():
            if field_name != 'profile_picture':
                field.widget.attrs['class'] = 'form-control'
            else:
                field.widget.attrs['class'] = 'form-control-file'


class CustomAuthenticationForm(AuthenticationForm):
    """
    Formulario para iniciar sesión de usuarios.
    """
    username = forms.EmailField(
        label=_("Correo electrónico"),
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'})
    )
    password = forms.CharField(
        label=_("Contraseña"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'})
    )
    
    error_messages = {
        'invalid_login': _(
            "Por favor, introduzca un correo electrónico y contraseña correctos. "
            "Tenga en cuenta que ambos campos pueden ser sensibles a mayúsculas."
        ),
        'inactive': _("Esta cuenta está inactiva."),
    }


class CustomPasswordResetForm(PasswordResetForm):
    """
    Formulario para solicitar un restablecimiento de contraseña.
    """
    email = forms.EmailField(
        label=_("Correo electrónico"),
        max_length=254,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'})
    )


class CustomSetPasswordForm(SetPasswordForm):
    """
    Formulario para establecer una nueva contraseña después de un restablecimiento.
    """
    new_password1 = forms.CharField(
        label=_("Nueva contraseña"),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Nueva contraseña'}),
        strip=False,
    )
    new_password2 = forms.CharField(
        label=_("Confirmar nueva contraseña"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmar nueva contraseña'}),
    )


class CustomPasswordChangeForm(PasswordChangeForm):
    """
    Formulario para cambiar la contraseña de un usuario.
    """
    old_password = forms.CharField(
        label=_("Contraseña actual"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña actual'})
    )
    new_password1 = forms.CharField(
        label=_("Nueva contraseña"),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Nueva contraseña'}),
        strip=False,
    )
    new_password2 = forms.CharField(
        label=_("Confirmar nueva contraseña"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmar nueva contraseña'}),
    )


class ProfileUpdateForm(forms.ModelForm):
    """
    Formulario para actualizar el perfil de usuario.
    """
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'profile_picture', 'bio']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control-file'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }