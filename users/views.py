from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, TemplateView
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView, PasswordChangeView,
    PasswordChangeDoneView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

from .models import CustomUser
from .forms import (
    CustomUserCreationForm, ProfileUpdateForm, CustomAuthenticationForm,
    CustomPasswordResetForm, CustomSetPasswordForm, CustomPasswordChangeForm
)


class SignUpView(CreateView):
    """Vista para registrar un nuevo usuario."""
    form_class = CustomUserCreationForm
    template_name = 'users/signup.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, _('¡Registro exitoso! Ahora puedes iniciar sesión.'))
        return response


class CustomLoginView(LoginView):
    """Vista personalizada para iniciar sesión."""
    form_class = CustomAuthenticationForm
    template_name = 'users/login.html'

    def form_valid(self, form):
        remember_me = self.request.POST.get('remember_me', False)
        if not remember_me:
            # La sesión expirará cuando el usuario cierre el navegador
            self.request.session.set_expiry(0)
        
        messages.success(self.request, _(f'Bienvenido, {form.get_user().get_short_name()}'))
        return super().form_valid(form)


class CustomLogoutView(LogoutView):
    """Vista personalizada para cerrar sesión."""
    template_name = 'users/logout.html'
    http_method_names = ['get', 'post']
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, _('Has cerrado sesión correctamente.'))
        return super().dispatch(request, *args, **kwargs)


class CustomPasswordResetView(PasswordResetView):
    """Vista para restablecer la contraseña."""
    form_class = CustomPasswordResetForm
    template_name = 'users/password_reset_form.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject.txt'
    success_url = reverse_lazy('users:password_reset_done')


class CustomPasswordResetDoneView(PasswordResetDoneView):
    """Vista que se muestra después de que se envía un correo para restablecer la contraseña."""
    template_name = 'users/password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    """Vista para confirmar el restablecimiento de la contraseña."""
    form_class = CustomSetPasswordForm
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('users:password_reset_complete')


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    """Vista que se muestra después de que se ha restablecido la contraseña."""
    template_name = 'users/password_reset_complete.html'


class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    """Vista para cambiar la contraseña."""
    form_class = CustomPasswordChangeForm
    template_name = 'users/password_change_form.html'
    success_url = reverse_lazy('users:password_change_done')


class CustomPasswordChangeDoneView(LoginRequiredMixin, PasswordChangeDoneView):
    """Vista que se muestra después de que se ha cambiado la contraseña."""
    template_name = 'users/password_change_done.html'


class ProfileView(LoginRequiredMixin, DetailView):
    """Vista para visualizar el perfil del usuario."""
    model = CustomUser
    template_name = 'users/profile.html'
    context_object_name = 'user'

    def get_object(self):
        return self.request.user


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Vista para actualizar el perfil del usuario."""
    model = CustomUser
    form_class = ProfileUpdateForm
    template_name = 'users/profile_update.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, _('Tu perfil ha sido actualizado correctamente.'))
        return super().form_valid(form)


class DashboardView(LoginRequiredMixin, TemplateView):
    """Vista del panel de control del usuario."""
    template_name = 'users/dashboard.html'