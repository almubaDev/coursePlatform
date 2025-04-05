from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Gestor personalizado de usuarios donde el correo electrónico es el identificador único
    para autenticación en lugar del nombre de usuario.
    """
    def create_user(self, email, password=None, **extra_fields):
        """
        Crea y guarda un usuario con el correo electrónico y contraseña dados.
        """
        if not email:
            raise ValueError(_('El correo electrónico es obligatorio'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Crea y guarda un superusuario con el correo electrónico y contraseña dados.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superusuario debe tener is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superusuario debe tener is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    """
    Modelo de usuario personalizado donde el correo electrónico es el identificador único
    para autenticación en lugar del nombre de usuario.
    """
    username = None
    email = models.EmailField(_('correo electrónico'), unique=True)
    first_name = models.CharField(_('nombre'), max_length=30)
    last_name = models.CharField(_('apellido'), max_length=30)
    date_joined = models.DateTimeField(_('fecha de registro'), auto_now_add=True)
    is_active = models.BooleanField(_('activo'), default=True)
    is_staff = models.BooleanField(_('staff'), default=False)
    
    # Campos adicionales para usuarios
    profile_picture = models.ImageField(
        _('foto de perfil'), 
        upload_to='profile_pics/', 
        null=True, 
        blank=True
    )
    bio = models.TextField(_('biografía'), max_length=500, blank=True)
    
    # Campos adicionales pueden añadirse aquí según sea necesario

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    class Meta:
        verbose_name = _('usuario')
        verbose_name_plural = _('usuarios')

    def __str__(self):
        return self.email

    def get_full_name(self):
        """
        Devuelve el nombre completo del usuario.
        """
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip()

    def get_short_name(self):
        """
        Devuelve el nombre corto del usuario.
        """
        return self.first_name