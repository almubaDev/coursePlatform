from django import forms
from django.utils.translation import gettext_lazy as _

from .models import (
    Course, Module, Section,
    FlashCard, ConceptConnection, Concept,
    MultipleChoiceTest, MultipleChoiceQuestion, MultipleChoiceOption,
    EssayTest, EssayQuestion, TestCoupon, EssayAttempt, EssayAnswer
)


class CourseForm(forms.ModelForm):
    """Formulario para crear y editar cursos."""
    
    class Meta:
        model = Course
        fields = ['title', 'slug', 'description', 'image', 'is_published']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        help_texts = {
            'slug': _('Un nombre corto único para el curso. Solo letras, números, guiones y guiones bajos.'),
            'is_published': _('Marcar para hacer el curso visible a los estudiantes.'),
        }


class ModuleForm(forms.ModelForm):
    """Formulario para crear y editar módulos."""
    
    class Meta:
        model = Module
        fields = ['title', 'description', 'order', 'course']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'course': forms.HiddenInput(),
        }
        help_texts = {
            'order': _('Orden de aparición del módulo en el curso.'),
        }


class SectionForm(forms.ModelForm):
    """Formulario para crear y editar secciones."""
    
    class Meta:
        model = Section
        fields = ['title', 'content', 'order', 'module']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10, 'id': 'markdown-editor'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'module': forms.HiddenInput(),
        }
        help_texts = {
            'content': _('Utiliza formato Markdown para dar estilo al contenido.'),
            'order': _('Orden de aparición de la sección en el módulo.'),
        }


class FlashCardForm(forms.ModelForm):
    """Formulario para crear y editar flashcards."""
    
    class Meta:
        model = FlashCard
        fields = ['question', 'answer', 'order', 'section']
        widgets = {
            'question': forms.TextInput(attrs={'class': 'form-control'}),
            'answer': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'section': forms.HiddenInput(),
        }


class ConceptConnectionForm(forms.ModelForm):
    """Formulario para crear y editar ejercicios de conexión de conceptos."""
    
    class Meta:
        model = ConceptConnection
        fields = ['title', 'description', 'order', 'section']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'section': forms.HiddenInput(),
        }


class ConceptForm(forms.ModelForm):
    """Formulario para crear y editar conceptos."""
    
    class Meta:
        model = Concept
        fields = ['term', 'definition', 'order', 'connection']
        widgets = {
            'term': forms.TextInput(attrs={'class': 'form-control'}),
            'definition': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'connection': forms.HiddenInput(),
        }


class MultipleChoiceTestForm(forms.ModelForm):
    """Formulario para crear y editar tests de opción múltiple."""
    
    class Meta:
        model = MultipleChoiceTest
        fields = ['title', 'description', 'order', 'section']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'section': forms.HiddenInput(),
        }


class MultipleChoiceQuestionForm(forms.ModelForm):
    """Formulario para crear y editar preguntas de opción múltiple."""
    
    class Meta:
        model = MultipleChoiceQuestion
        fields = ['question_text', 'explanation', 'order', 'test']
        widgets = {
            'question_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'explanation': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'test': forms.HiddenInput(),
        }
        help_texts = {
            'explanation': _('Explicación que se mostrará después de que el estudiante responda.'),
        }


class MultipleChoiceOptionForm(forms.ModelForm):
    """Formulario para crear y editar opciones de preguntas de opción múltiple."""
    
    class Meta:
        model = MultipleChoiceOption
        fields = ['option_text', 'is_correct', 'order', 'question']
        widgets = {
            'option_text': forms.TextInput(attrs={'class': 'form-control'}),
            'is_correct': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'question': forms.HiddenInput(),
        }


class EssayTestForm(forms.ModelForm):
    """Formulario para crear y editar tests de desarrollo."""
    
    class Meta:
        model = EssayTest
        fields = ['title', 'description', 'module']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'module': forms.HiddenInput(),
        }
        help_texts = {
            'description': _('Instrucciones para el estudiante sobre cómo completar el test.'),
        }


class EssayQuestionForm(forms.ModelForm):
    """Formulario para crear y editar preguntas de desarrollo."""
    
    class Meta:
        model = EssayQuestion
        fields = ['question_text', 'question_type', 'order', 'test']
        widgets = {
            'question_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'question_type': forms.Select(attrs={'class': 'form-select'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'test': forms.HiddenInput(),
        }
        help_texts = {
            'question_type': _('Selecciona si es una pregunta regular o un estudio de caso.'),
        }


class TestCouponForm(forms.ModelForm):
    """Formulario para crear cupones de test."""
    
    class Meta:
        model = TestCoupon
        fields = ['user', 'test', 'is_used']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-select'}),
            'test': forms.Select(attrs={'class': 'form-select'}),
            'is_used': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ordenar los tests por curso y título para facilitar la selección
        self.fields['test'].queryset = EssayTest.objects.select_related('module__course').order_by(
            'module__course__title', 'title'
        )
        # Añadimos el nombre del curso al título del test para mejor identificación
        self.fields['test'].label_from_instance = lambda obj: f"{obj.title} ({obj.module.course.title})"


class EssayAnswerForm(forms.ModelForm):
    """Formulario para que los estudiantes respondan preguntas de desarrollo."""
    
    class Meta:
        model = EssayAnswer
        fields = ['answer_text', 'question', 'attempt']
        widgets = {
            'answer_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 6}),
            'question': forms.HiddenInput(),
            'attempt': forms.HiddenInput(),
        }


class EssayTestAttemptForm(forms.Form):
    """Formulario para iniciar un intento de test de desarrollo."""
    
    test_id = forms.IntegerField(widget=forms.HiddenInput())
    
    def clean_test_id(self):
        test_id = self.cleaned_data['test_id']
        user = self.initial.get('user')
        
        if not user:
            raise forms.ValidationError(_("Usuario no identificado."))
        
        try:
            test = EssayTest.objects.get(pk=test_id)
        except EssayTest.DoesNotExist:
            raise forms.ValidationError(_("El test seleccionado no existe."))
        
        # Verificar si el usuario ya ha realizado este test
        if EssayAttempt.objects.filter(user=user, test=test).exists():
            # Verificar si tiene un cupón disponible
            if not TestCoupon.objects.filter(user=user, test=test, is_used=False).exists():
                raise forms.ValidationError(_("Ya has completado este test y no tienes cupones disponibles para otro intento."))
        
        return test_id