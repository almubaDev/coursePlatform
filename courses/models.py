from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class Course(models.Model):
    """Modelo para los cursos."""
    title = models.CharField(_('título'), max_length=200)
    slug = models.SlugField(_('slug'), max_length=200, unique=True)
    description = models.TextField(_('descripción'))
    image = models.ImageField(_('imagen'), upload_to='courses/%Y/%m/%d/', blank=True)
    created = models.DateTimeField(_('fecha de creación'), auto_now_add=True)
    updated = models.DateTimeField(_('fecha de actualización'), auto_now=True)
    is_published = models.BooleanField(_('publicado'), default=False)

    class Meta:
        ordering = ['-created']
        verbose_name = _('curso')
        verbose_name_plural = _('cursos')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('courses:course_detail', args=[self.slug])


class Module(models.Model):
    """Modelo para los módulos que componen un curso."""
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules', verbose_name=_('curso'))
    title = models.CharField(_('título'), max_length=200)
    description = models.TextField(_('descripción'), blank=True)
    order = models.PositiveIntegerField(_('orden'), default=0)
    created = models.DateTimeField(_('fecha de creación'), auto_now_add=True)
    updated = models.DateTimeField(_('fecha de actualización'), auto_now=True)

    class Meta:
        ordering = ['order']
        verbose_name = _('módulo')
        verbose_name_plural = _('módulos')

    def __str__(self):
        return f'{self.title} ({self.course.title})'


class Section(models.Model):
    """Modelo para las secciones de contenido dentro de los módulos."""
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='sections', verbose_name=_('módulo'))
    title = models.CharField(_('título'), max_length=200)
    content = models.TextField(_('contenido en markdown'))
    order = models.PositiveIntegerField(_('orden'), default=0)
    created = models.DateTimeField(_('fecha de creación'), auto_now_add=True)
    updated = models.DateTimeField(_('fecha de actualización'), auto_now=True)

    class Meta:
        ordering = ['order']
        verbose_name = _('sección')
        verbose_name_plural = _('secciones')

    def __str__(self):
        return f'{self.title} ({self.module.title})'


class FlashCard(models.Model):
    """Modelo para las flashcards asociadas a una sección."""
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='flashcards', verbose_name=_('sección'))
    question = models.CharField(_('pregunta'), max_length=500)
    answer = models.TextField(_('respuesta'))
    order = models.PositiveIntegerField(_('orden'), default=0)

    class Meta:
        ordering = ['order']
        verbose_name = _('flashcard')
        verbose_name_plural = _('flashcards')

    def __str__(self):
        return f'Flashcard: {self.question[:50]}...'


class ConceptConnection(models.Model):
    """Modelo para los ejercicios de unir conceptos."""
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='concept_connections', verbose_name=_('sección'))
    title = models.CharField(_('título'), max_length=200)
    description = models.TextField(_('descripción'), blank=True)
    order = models.PositiveIntegerField(_('orden'), default=0)

    class Meta:
        ordering = ['order']
        verbose_name = _('ejercicio de conexión')
        verbose_name_plural = _('ejercicios de conexión')

    def __str__(self):
        return self.title


class Concept(models.Model):
    """Modelo para los conceptos que se conectan en los ejercicios."""
    connection = models.ForeignKey(ConceptConnection, on_delete=models.CASCADE, related_name='concepts', verbose_name=_('ejercicio'))
    term = models.CharField(_('término'), max_length=200)
    definition = models.TextField(_('definición'))
    order = models.PositiveIntegerField(_('orden'), default=0)

    class Meta:
        ordering = ['order']
        verbose_name = _('concepto')
        verbose_name_plural = _('conceptos')

    def __str__(self):
        return f'{self.term} - {self.connection.title}'


class MultipleChoiceTest(models.Model):
    """Modelo para los tests de alternativas múltiples."""
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='multiple_choice_tests', verbose_name=_('sección'))
    title = models.CharField(_('título'), max_length=200)
    description = models.TextField(_('descripción'), blank=True)
    order = models.PositiveIntegerField(_('orden'), default=0)

    class Meta:
        ordering = ['order']
        verbose_name = _('test de alternativas')
        verbose_name_plural = _('tests de alternativas')

    def __str__(self):
        return self.title


class MultipleChoiceQuestion(models.Model):
    """Modelo para las preguntas de alternativas múltiples."""
    test = models.ForeignKey(MultipleChoiceTest, on_delete=models.CASCADE, related_name='questions', verbose_name=_('test'))
    question_text = models.CharField(_('pregunta'), max_length=500)
    explanation = models.TextField(_('explicación'), blank=True, help_text=_('Explicación que se mostrará después de responder'))
    order = models.PositiveIntegerField(_('orden'), default=0)

    class Meta:
        ordering = ['order']
        verbose_name = _('pregunta de alternativas')
        verbose_name_plural = _('preguntas de alternativas')

    def __str__(self):
        return self.question_text[:50]


class MultipleChoiceOption(models.Model):
    """Modelo para las opciones de las preguntas de alternativas múltiples."""
    question = models.ForeignKey(MultipleChoiceQuestion, on_delete=models.CASCADE, related_name='options', verbose_name=_('pregunta'))
    option_text = models.CharField(_('opción'), max_length=255)
    is_correct = models.BooleanField(_('es correcta'), default=False)
    order = models.PositiveIntegerField(_('orden'), default=0)

    class Meta:
        ordering = ['order']
        verbose_name = _('opción')
        verbose_name_plural = _('opciones')

    def __str__(self):
        return f'{self.option_text} ({"Correcta" if self.is_correct else "Incorrecta"})'


class EssayTest(models.Model):
    """Modelo para los tests de preguntas de desarrollo al final del módulo."""
    module = models.OneToOneField(Module, on_delete=models.CASCADE, related_name='essay_test', verbose_name=_('módulo'))
    title = models.CharField(_('título'), max_length=200)
    description = models.TextField(_('descripción'), blank=True)
    created = models.DateTimeField(_('fecha de creación'), auto_now_add=True)
    updated = models.DateTimeField(_('fecha de actualización'), auto_now=True)

    class Meta:
        verbose_name = _('test de desarrollo')
        verbose_name_plural = _('tests de desarrollo')

    def __str__(self):
        return f'Test: {self.title}'


class EssayQuestion(models.Model):
    """Modelo para las preguntas de desarrollo."""
    QUESTION_TYPES = (
        ('regular', _('Regular')),
        ('case_study', _('Estudio de caso')),
    )
    
    test = models.ForeignKey(EssayTest, on_delete=models.CASCADE, related_name='questions', verbose_name=_('test'))
    question_text = models.TextField(_('pregunta'))
    question_type = models.CharField(_('tipo de pregunta'), max_length=20, choices=QUESTION_TYPES, default='regular')
    order = models.PositiveIntegerField(_('orden'), default=0)

    class Meta:
        ordering = ['order']
        verbose_name = _('pregunta de desarrollo')
        verbose_name_plural = _('preguntas de desarrollo')

    def __str__(self):
        return f'{self.get_question_type_display()}: {self.question_text[:50]}...'


class EssayAttempt(models.Model):
    """Modelo para los intentos de respuesta al test de desarrollo."""
    STATUS_CHOICES = (
        ('submitted', _('Enviado')),
        ('processing', _('Procesando')),
        ('analyzed', _('Analizado')),
        ('failed', _('Falló análisis')),
    )
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='essay_attempts', verbose_name=_('usuario'))
    test = models.ForeignKey(EssayTest, on_delete=models.CASCADE, related_name='attempts', verbose_name=_('test'))
    date_submitted = models.DateTimeField(_('fecha de envío'), auto_now_add=True)
    date_analyzed = models.DateTimeField(_('fecha de análisis'), null=True, blank=True)
    status = models.CharField(_('estado'), max_length=20, choices=STATUS_CHOICES, default='submitted')
    ai_feedback = models.TextField(_('retroalimentación IA'), blank=True)
    score = models.FloatField(_('puntuación'), null=True, blank=True)

    class Meta:
        ordering = ['-date_submitted']
        verbose_name = _('intento de test')
        verbose_name_plural = _('intentos de test')
        unique_together = [['user', 'test']]  # Un usuario solo puede tener un intento por test

    def __str__(self):
        return f'{self.user.email} - {self.test.title} ({self.date_submitted.strftime("%d/%m/%Y")})'


class EssayAnswer(models.Model):
    """Modelo para las respuestas a las preguntas de desarrollo."""
    attempt = models.ForeignKey(EssayAttempt, on_delete=models.CASCADE, related_name='answers', verbose_name=_('intento'))
    question = models.ForeignKey(EssayQuestion, on_delete=models.CASCADE, related_name='answers', verbose_name=_('pregunta'))
    answer_text = models.TextField(_('respuesta'))
    ai_feedback = models.TextField(_('retroalimentación IA'), blank=True)
    
    class Meta:
        verbose_name = _('respuesta de desarrollo')
        verbose_name_plural = _('respuestas de desarrollo')
        unique_together = [['attempt', 'question']]  # Una respuesta por pregunta por intento

    def __str__(self):
        return f'Respuesta: {self.answer_text[:50]}...'


class TestCoupon(models.Model):
    """Modelo para los cupones que permiten intentos adicionales en los tests de desarrollo."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='test_coupons', verbose_name=_('usuario'))
    test = models.ForeignKey(EssayTest, on_delete=models.CASCADE, related_name='coupons', verbose_name=_('test'))
    created = models.DateTimeField(_('fecha de creación'), auto_now_add=True)
    is_used = models.BooleanField(_('usado'), default=False)
    used_date = models.DateTimeField(_('fecha de uso'), null=True, blank=True)
    
    class Meta:
        verbose_name = _('cupón de test')
        verbose_name_plural = _('cupones de test')

    def __str__(self):
        return f'Cupón: {self.user.email} - {self.test.title} ({"Usado" if self.is_used else "Disponible"})'