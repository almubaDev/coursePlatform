from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView, FormView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.http import JsonResponse, HttpResponseForbidden
from django.db.models import Q
from django.utils import timezone

from .models import (
    Course, Module, Section,
    FlashCard, ConceptConnection, Concept,
    MultipleChoiceTest, MultipleChoiceQuestion, MultipleChoiceOption,
    EssayTest, EssayQuestion, EssayAttempt, EssayAnswer, TestCoupon
)
from .forms import (
    CourseForm, ModuleForm, SectionForm,
    FlashCardForm, ConceptConnectionForm, ConceptForm,
    MultipleChoiceTestForm, MultipleChoiceQuestionForm, MultipleChoiceOptionForm,
    EssayTestForm, EssayQuestionForm, TestCouponForm, EssayAnswerForm, EssayTestAttemptForm
)


# Mixin para verificar superusuarios
class SuperuserRequiredMixin(UserPassesTestMixin):
    """Mixin que restringe el acceso solo a superusuarios."""
    
    def test_func(self):
        return self.request.user.is_superuser


# Vistas para la administración de cursos
class CourseListView(SuperuserRequiredMixin, ListView):
    """Vista para listar todos los cursos en el panel de administración."""
    model = Course
    template_name = 'courses/admin/course_list.html'
    context_object_name = 'courses'


class CourseCreateView(SuperuserRequiredMixin, CreateView):
    """Vista para crear un nuevo curso."""
    model = Course
    form_class = CourseForm
    template_name = 'courses/admin/course_form.html'
    success_url = reverse_lazy('courses:admin_course_list')
    
    def form_valid(self, form):
        messages.success(self.request, _('Curso creado correctamente.'))
        return super().form_valid(form)


class CourseUpdateView(SuperuserRequiredMixin, UpdateView):
    """Vista para actualizar un curso existente."""
    model = Course
    form_class = CourseForm
    template_name = 'courses/admin/course_form.html'
    success_url = reverse_lazy('courses:admin_course_list')
    
    def form_valid(self, form):
        messages.success(self.request, _('Curso actualizado correctamente.'))
        return super().form_valid(form)


class CourseDeleteView(SuperuserRequiredMixin, DeleteView):
    """Vista para eliminar un curso."""
    model = Course
    template_name = 'courses/admin/course_confirm_delete.html'
    success_url = reverse_lazy('courses:admin_course_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, _('Curso eliminado correctamente.'))
        return super().delete(request, *args, **kwargs)


# Vistas para módulos
class ModuleListView(SuperuserRequiredMixin, ListView):
    """Vista para listar los módulos de un curso."""
    model = Module
    template_name = 'courses/admin/module_list.html'
    context_object_name = 'modules'
    
    def get_queryset(self):
        self.course = get_object_or_404(Course, slug=self.kwargs['course_slug'])
        return Module.objects.filter(course=self.course).order_by('order')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = self.course
        return context


class ModuleCreateView(SuperuserRequiredMixin, CreateView):
    """Vista para crear un nuevo módulo."""
    model = Module
    form_class = ModuleForm
    template_name = 'courses/admin/module_form.html'
    
    def get_initial(self):
        self.course = get_object_or_404(Course, slug=self.kwargs['course_slug'])
        return {'course': self.course}
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = self.course
        return context
    
    def get_success_url(self):
        return reverse('courses:admin_module_list', kwargs={'course_slug': self.course.slug})
    
    def form_valid(self, form):
        messages.success(self.request, _('Módulo creado correctamente.'))
        return super().form_valid(form)


class ModuleUpdateView(SuperuserRequiredMixin, UpdateView):
    """Vista para actualizar un módulo existente."""
    model = Module
    form_class = ModuleForm
    template_name = 'courses/admin/module_form.html'
    pk_url_kwarg = 'module_id'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = self.object.course
        return context
    
    def get_success_url(self):
        return reverse('courses:admin_module_list', kwargs={'course_slug': self.object.course.slug})
    
    def form_valid(self, form):
        messages.success(self.request, _('Módulo actualizado correctamente.'))
        return super().form_valid(form)


class ModuleDeleteView(SuperuserRequiredMixin, DeleteView):
    """Vista para eliminar un módulo."""
    model = Module
    template_name = 'courses/admin/module_confirm_delete.html'
    pk_url_kwarg = 'module_id'
    
    def get_success_url(self):
        return reverse('courses:admin_module_list', kwargs={'course_slug': self.object.course.slug})
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, _('Módulo eliminado correctamente.'))
        return super().delete(request, *args, **kwargs)


# Vistas para secciones
class SectionListView(SuperuserRequiredMixin, ListView):
    """Vista para listar las secciones de un módulo."""
    model = Section
    template_name = 'courses/admin/section_list.html'
    context_object_name = 'sections'
    
    def get_queryset(self):
        self.module = get_object_or_404(Module, id=self.kwargs['module_id'])
        return Section.objects.filter(module=self.module).order_by('order')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module'] = self.module
        context['course'] = self.module.course
        return context


class SectionCreateView(SuperuserRequiredMixin, CreateView):
    """Vista para crear una nueva sección."""
    model = Section
    form_class = SectionForm
    template_name = 'courses/admin/section_form.html'
    
    def get_initial(self):
        self.module = get_object_or_404(Module, id=self.kwargs['module_id'])
        return {'module': self.module}
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module'] = self.module
        context['course'] = self.module.course
        return context
    
    def get_success_url(self):
        return reverse('courses:admin_section_list', kwargs={'module_id': self.module.id})
    
    def form_valid(self, form):
        messages.success(self.request, _('Sección creada correctamente.'))
        return super().form_valid(form)


class SectionUpdateView(SuperuserRequiredMixin, UpdateView):
    """Vista para actualizar una sección existente."""
    model = Section
    form_class = SectionForm
    template_name = 'courses/admin/section_form.html'
    pk_url_kwarg = 'section_id'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module'] = self.object.module
        context['course'] = self.object.module.course
        return context
    
    def get_success_url(self):
        return reverse('courses:admin_section_list', kwargs={'module_id': self.object.module.id})
    
    def form_valid(self, form):
        messages.success(self.request, _('Sección actualizada correctamente.'))
        return super().form_valid(form)


class SectionDeleteView(SuperuserRequiredMixin, DeleteView):
    """Vista para eliminar una sección."""
    model = Section
    template_name = 'courses/admin/section_confirm_delete.html'
    pk_url_kwarg = 'section_id'
    
    def get_success_url(self):
        return reverse('courses:admin_section_list', kwargs={'module_id': self.object.module.id})
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, _('Sección eliminada correctamente.'))
        return super().delete(request, *args, **kwargs)


# Vista para listar actividades de una sección
class ActivityListView(SuperuserRequiredMixin, TemplateView):
    """Vista para listar todas las actividades de una sección."""
    template_name = 'courses/admin/activity_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        section_id = self.kwargs.get('section_id')
        section = get_object_or_404(Section, id=section_id)
        
        context['section'] = section
        context['module'] = section.module
        context['course'] = section.module.course
        
        # Obtener todas las actividades de la sección
        context['flashcards'] = FlashCard.objects.filter(section=section).order_by('order')
        context['concept_connections'] = ConceptConnection.objects.filter(section=section).order_by('order')
        context['multiple_choice_tests'] = MultipleChoiceTest.objects.filter(section=section).order_by('order')
        
        return context


# Vistas para Flashcards
class FlashcardCreateView(SuperuserRequiredMixin, CreateView):
    """Vista para crear una nueva flashcard."""
    model = FlashCard
    form_class = FlashCardForm
    template_name = 'courses/admin/flashcard_form.html'
    
    def get_initial(self):
        self.section = get_object_or_404(Section, id=self.kwargs['section_id'])
        return {'section': self.section}
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = self.section
        context['module'] = self.section.module
        context['course'] = self.section.module.course
        return context
    
    def get_success_url(self):
        return reverse('courses:admin_activity_list', kwargs={'section_id': self.section.id})
    
    def form_valid(self, form):
        messages.success(self.request, _('Flashcard creada correctamente.'))
        return super().form_valid(form)


class FlashcardUpdateView(SuperuserRequiredMixin, UpdateView):
    """Vista para actualizar una flashcard existente."""
    model = FlashCard
    form_class = FlashCardForm
    template_name = 'courses/admin/flashcard_form.html'
    pk_url_kwarg = 'flashcard_id'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = self.object.section
        context['module'] = self.object.section.module
        context['course'] = self.object.section.module.course
        return context
    
    def get_success_url(self):
        return reverse('courses:admin_activity_list', kwargs={'section_id': self.object.section.id})
    
    def form_valid(self, form):
        messages.success(self.request, _('Flashcard actualizada correctamente.'))
        return super().form_valid(form)


class FlashcardDeleteView(SuperuserRequiredMixin, DeleteView):
    """Vista para eliminar una flashcard."""
    model = FlashCard
    template_name = 'courses/admin/flashcard_confirm_delete.html'
    pk_url_kwarg = 'flashcard_id'
    
    def get_success_url(self):
        return reverse('courses:admin_activity_list', kwargs={'section_id': self.object.section.id})
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, _('Flashcard eliminada correctamente.'))
        return super().delete(request, *args, **kwargs)


# Vistas para Conexión de conceptos
class ConceptConnectionCreateView(SuperuserRequiredMixin, CreateView):
    """Vista para crear un nuevo ejercicio de conexión de conceptos."""
    model = ConceptConnection
    form_class = ConceptConnectionForm
    template_name = 'courses/admin/concept_connection_form.html'
    
    def get_initial(self):
        self.section = get_object_or_404(Section, id=self.kwargs['section_id'])
        return {'section': self.section}
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = self.section
        context['module'] = self.section.module
        context['course'] = self.section.module.course
        return context
    
    def get_success_url(self):
        return reverse('courses:admin_activity_list', kwargs={'section_id': self.section.id})
    
    def form_valid(self, form):
        messages.success(self.request, _('Ejercicio de conexión creado correctamente.'))
        return super().form_valid(form)


class ConceptConnectionUpdateView(SuperuserRequiredMixin, UpdateView):
    """Vista para actualizar un ejercicio de conexión de conceptos."""
    model = ConceptConnection
    form_class = ConceptConnectionForm
    template_name = 'courses/admin/concept_connection_form.html'
    pk_url_kwarg = 'connection_id'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = self.object.section
        context['module'] = self.object.section.module
        context['course'] = self.object.section.module.course
        context['concepts'] = Concept.objects.filter(connection=self.object).order_by('order')
        return context
    
    def get_success_url(self):
        return reverse('courses:admin_activity_list', kwargs={'section_id': self.object.section.id})
    
    def form_valid(self, form):
        messages.success(self.request, _('Ejercicio de conexión actualizado correctamente.'))
        return super().form_valid(form)


class ConceptConnectionDeleteView(SuperuserRequiredMixin, DeleteView):
    """Vista para eliminar un ejercicio de conexión de conceptos."""
    model = ConceptConnection
    template_name = 'courses/admin/concept_connection_confirm_delete.html'
    pk_url_kwarg = 'connection_id'
    
    def get_success_url(self):
        return reverse('courses:admin_activity_list', kwargs={'section_id': self.object.section.id})
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, _('Ejercicio de conexión eliminado correctamente.'))
        return super().delete(request, *args, **kwargs)


# Vistas para tests de opción múltiple
class MultipleChoiceTestCreateView(SuperuserRequiredMixin, CreateView):
    """Vista para crear un nuevo test de opción múltiple."""
    model = MultipleChoiceTest
    form_class = MultipleChoiceTestForm
    template_name = 'courses/admin/multiple_choice_test_form.html'
    
    def get_initial(self):
        self.section = get_object_or_404(Section, id=self.kwargs['section_id'])
        return {'section': self.section}
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = self.section
        context['module'] = self.section.module
        context['course'] = self.section.module.course
        return context
    
    def get_success_url(self):
        return reverse('courses:admin_activity_list', kwargs={'section_id': self.section.id})
    
    def form_valid(self, form):
        messages.success(self.request, _('Test de opción múltiple creado correctamente.'))
        return super().form_valid(form)


class MultipleChoiceTestUpdateView(SuperuserRequiredMixin, UpdateView):
    """Vista para actualizar un test de opción múltiple."""
    model = MultipleChoiceTest
    form_class = MultipleChoiceTestForm
    template_name = 'courses/admin/multiple_choice_test_form.html'
    pk_url_kwarg = 'test_id'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = self.object.section
        context['module'] = self.object.section.module
        context['course'] = self.object.section.module.course
        context['questions'] = MultipleChoiceQuestion.objects.filter(test=self.object).order_by('order')
        return context
    
    def get_success_url(self):
        return reverse('courses:admin_activity_list', kwargs={'section_id': self.object.section.id})
    
    def form_valid(self, form):
        messages.success(self.request, _('Test de opción múltiple actualizado correctamente.'))
        return super().form_valid(form)


class MultipleChoiceTestDeleteView(SuperuserRequiredMixin, DeleteView):
    """Vista para eliminar un test de opción múltiple."""
    model = MultipleChoiceTest
    template_name = 'courses/admin/multiple_choice_test_confirm_delete.html'
    pk_url_kwarg = 'test_id'
    
    def get_success_url(self):
        return reverse('courses:admin_activity_list', kwargs={'section_id': self.object.section.id})
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, _('Test de opción múltiple eliminado correctamente.'))
        return super().delete(request, *args, **kwargs)


# Vistas para preguntas de tests de opción múltiple
class MultipleChoiceQuestionCreateView(SuperuserRequiredMixin, CreateView):
    """Vista para crear una nueva pregunta de opción múltiple."""
    model = MultipleChoiceQuestion
    form_class = MultipleChoiceQuestionForm
    template_name = 'courses/admin/multiple_choice_question_form.html'
    
    def get_initial(self):
        self.test = get_object_or_404(MultipleChoiceTest, id=self.kwargs['test_id'])
        return {'test': self.test}
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['test'] = self.test
        context['section'] = self.test.section
        context['module'] = self.test.section.module
        context['course'] = self.test.section.module.course
        return context
    
    def get_success_url(self):
        return reverse('courses:admin_multiple_choice_update', kwargs={'test_id': self.test.id})
    
    def form_valid(self, form):
        messages.success(self.request, _('Pregunta creada correctamente.'))
        return super().form_valid(form)


class MultipleChoiceQuestionUpdateView(SuperuserRequiredMixin, UpdateView):
    """Vista para actualizar una pregunta de opción múltiple."""
    model = MultipleChoiceQuestion
    form_class = MultipleChoiceQuestionForm
    template_name = 'courses/admin/multiple_choice_question_form.html'
    pk_url_kwarg = 'question_id'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['test'] = self.object.test
        context['section'] = self.object.test.section
        context['module'] = self.object.test.section.module
        context['course'] = self.object.test.section.module.course
        context['options'] = MultipleChoiceOption.objects.filter(question=self.object).order_by('order')
        return context
    
    def get_success_url(self):
        return reverse('courses:admin_multiple_choice_update', kwargs={'test_id': self.object.test.id})
    
    def form_valid(self, form):
        messages.success(self.request, _('Pregunta actualizada correctamente.'))
        return super().form_valid(form)


class MultipleChoiceQuestionDeleteView(SuperuserRequiredMixin, DeleteView):
    """Vista para eliminar una pregunta de opción múltiple."""
    model = MultipleChoiceQuestion
    template_name = 'courses/admin/multiple_choice_question_confirm_delete.html'
    pk_url_kwarg = 'question_id'
    
    def get_success_url(self):
        return reverse('courses:admin_multiple_choice_update', kwargs={'test_id': self.object.test.id})
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, _('Pregunta eliminada correctamente.'))
        return super().delete(request, *args, **kwargs)


# Vistas para tests de desarrollo
class EssayTestCreateView(SuperuserRequiredMixin, CreateView):
    """Vista para crear un nuevo test de desarrollo."""
    model = EssayTest
    form_class = EssayTestForm
    template_name = 'courses/admin/essay_test_form.html'
    
    def get_initial(self):
        self.module = get_object_or_404(Module, id=self.kwargs['module_id'])
        return {'module': self.module}
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module'] = self.module
        context['course'] = self.module.course
        return context
    
    def get_success_url(self):
        return reverse('courses:admin_module_list', kwargs={'course_slug': self.module.course.slug})
    
    def form_valid(self, form):
        messages.success(self.request, _('Test de desarrollo creado correctamente.'))
        return super().form_valid(form)


class EssayTestUpdateView(SuperuserRequiredMixin, UpdateView):
    """Vista para actualizar un test de desarrollo."""
    model = EssayTest
    form_class = EssayTestForm
    template_name = 'courses/admin/essay_test_form.html'
    pk_url_kwarg = 'test_id'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module'] = self.object.module
        context['course'] = self.object.module.course
        context['questions'] = EssayQuestion.objects.filter(test=self.object).order_by('order')
        return context
    
    def get_success_url(self):
        return reverse('courses:admin_module_list', kwargs={'course_slug': self.object.module.course.slug})
    
    def form_valid(self, form):
        messages.success(self.request, _('Test de desarrollo actualizado correctamente.'))
        return super().form_valid(form)


class EssayTestDeleteView(SuperuserRequiredMixin, DeleteView):
    """Vista para eliminar un test de desarrollo."""
    model = EssayTest
    template_name = 'courses/admin/essay_test_confirm_delete.html'
    pk_url_kwarg = 'test_id'
    
    def get_success_url(self):
        return reverse('courses:admin_module_list', kwargs={'course_slug': self.object.module.course.slug})
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, _('Test de desarrollo eliminado correctamente.'))
        return super().delete(request, *args, **kwargs)


# Vistas para preguntas de desarrollo
class EssayQuestionCreateView(SuperuserRequiredMixin, CreateView):
    """Vista para crear una nueva pregunta de desarrollo."""
    model = EssayQuestion
    form_class = EssayQuestionForm
    template_name = 'courses/admin/essay_question_form.html'
    
    def get_initial(self):
        self.test = get_object_or_404(EssayTest, id=self.kwargs['test_id'])
        return {'test': self.test}
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['test'] = self.test
        context['module'] = self.test.module
        context['course'] = self.test.module.course
        return context
    
    def get_success_url(self):
        return reverse('courses:admin_essay_test_update', kwargs={'test_id': self.test.id})
    
    def form_valid(self, form):
        messages.success(self.request, _('Pregunta de desarrollo creada correctamente.'))
        return super().form_valid(form)


class EssayQuestionUpdateView(SuperuserRequiredMixin, UpdateView):
    """Vista para actualizar una pregunta de desarrollo."""
    model = EssayQuestion
    form_class = EssayQuestionForm
    template_name = 'courses/admin/essay_question_form.html'
    pk_url_kwarg = 'question_id'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['test'] = self.object.test
        context['module'] = self.object.test.module
        context['course'] = self.object.test.module.course
        return context
    
    def get_success_url(self):
        return reverse('courses:admin_essay_test_update', kwargs={'test_id': self.object.test.id})
    
    def form_valid(self, form):
        messages.success(self.request, _('Pregunta de desarrollo actualizada correctamente.'))
        return super().form_valid(form)


class EssayQuestionDeleteView(SuperuserRequiredMixin, DeleteView):
    """Vista para eliminar una pregunta de desarrollo."""
    model = EssayQuestion
    template_name = 'courses/admin/essay_question_confirm_delete.html'
    pk_url_kwarg = 'question_id'
    
    def get_success_url(self):
        return reverse('courses:admin_essay_test_update', kwargs={'test_id': self.object.test.id})
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, _('Pregunta de desarrollo eliminada correctamente.'))
        return super().delete(request, *args, **kwargs)


# Vistas para intentos de tests de desarrollo
class EssayAttemptListView(SuperuserRequiredMixin, ListView):
    """Vista para listar todos los intentos de tests de desarrollo."""
    model = EssayAttempt
    template_name = 'courses/admin/essay_attempt_list.html'
    context_object_name = 'attempts'
    
    def get_queryset(self):
        return EssayAttempt.objects.select_related('user', 'test__module__course').order_by('-date_submitted')


class EssayAttemptDetailView(SuperuserRequiredMixin, DetailView):
    """Vista para ver el detalle de un intento de test de desarrollo."""
    model = EssayAttempt
    template_name = 'courses/admin/essay_attempt_detail.html'
    context_object_name = 'attempt'
    pk_url_kwarg = 'attempt_id'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['answers'] = EssayAnswer.objects.filter(attempt=self.object).select_related('question')
        context['test'] = self.object.test
        context['module'] = self.object.test.module
        context['course'] = self.object.test.module.course
        return context


# Vistas para cupones
class TestCouponListView(SuperuserRequiredMixin, ListView):
    """Vista para listar todos los cupones de tests."""
    model = TestCoupon
    template_name = 'courses/admin/test_coupon_list.html'
    context_object_name = 'coupons'
    
    def get_queryset(self):
        return TestCoupon.objects.select_related('user', 'test__module__course').order_by('-created')


class TestCouponCreateView(SuperuserRequiredMixin, CreateView):
    """Vista para crear un nuevo cupón de test."""
    model = TestCoupon
    form_class = TestCouponForm
    template_name = 'courses/admin/test_coupon_form.html'
    success_url = reverse_lazy('courses:admin_coupon_list')
    
    def form_valid(self, form):
        messages.success(self.request, _('Cupón creado correctamente.'))
        return super().form_valid(form)


# API para guardar conceptos (AJAX)
def save_concept(request, connection_id):
    """API para guardar un concepto mediante AJAX."""
    if not request.user.is_superuser:
        return HttpResponseForbidden("No tienes permiso para realizar esta acción.")
    
    if request.method == 'POST':
        connection = get_object_or_404(ConceptConnection, id=connection_id)
        
        term = request.POST.get('term', '')
        definition = request.POST.get('definition', '')
        order = request.POST.get('order', 0)
        concept_id = request.POST.get('concept_id', None)
        
        if concept_id and concept_id != 'new':
            # Actualizar concepto existente
            concept = get_object_or_404(Concept, id=concept_id)
            concept.term = term
            concept.definition = definition
            concept.order = order
            concept.save()
            message = 'Concepto actualizado correctamente.'
        else:
            # Crear nuevo concepto
            concept = Concept.objects.create(
                connection=connection,
                term=term,
                definition=definition,
                order=order
            )
            message = 'Concepto creado correctamente.'
        
        return JsonResponse({
            'success': True,
            'message': message,
            'concept_id': concept.id
        })
    
    return JsonResponse({'success': False, 'message': 'Método no permitido.'}, status=405)


# API para eliminar concepto (AJAX)
def delete_concept(request, concept_id):
    """API para eliminar un concepto mediante AJAX."""
    if not request.user.is_superuser:
        return HttpResponseForbidden("No tienes permiso para realizar esta acción.")
    
    if request.method == 'POST':
        concept = get_object_or_404(Concept, id=concept_id)
        concept.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Concepto eliminado correctamente.'
        })
    
    return JsonResponse({'success': False, 'message': 'Método no permitido.'}, status=405)


# API para guardar opciones de preguntas de opción múltiple (AJAX)
def save_option(request, question_id):
    """API para guardar una opción de pregunta mediante AJAX."""
    if not request.user.is_superuser:
        return HttpResponseForbidden("No tienes permiso para realizar esta acción.")
    
    if request.method == 'POST':
        question = get_object_or_404(MultipleChoiceQuestion, id=question_id)
        
        option_text = request.POST.get('option_text', '')
        is_correct = request.POST.get('is_correct', '') == 'true'
        order = request.POST.get('order', 0)
        option_id = request.POST.get('option_id', None)
        
        if option_id and option_id != 'new':
            # Actualizar opción existente
            option = get_object_or_404(MultipleChoiceOption, id=option_id)
            option.option_text = option_text
            option.is_correct = is_correct
            option.order = order
            option.save()
            message = 'Opción actualizada correctamente.'
        else:
            # Crear nueva opción
            option = MultipleChoiceOption.objects.create(
                question=question,
                option_text=option_text,
                is_correct=is_correct,
                order=order
            )
            message = 'Opción creada correctamente.'
        
        return JsonResponse({
            'success': True,
            'message': message,
            'option_id': option.id
        })
    
    return JsonResponse({'success': False, 'message': 'Método no permitido.'}, status=405)


# API para eliminar opción (AJAX)
def delete_option(request, option_id):
    """API para eliminar una opción mediante AJAX."""
    if not request.user.is_superuser:
        return HttpResponseForbidden("No tienes permiso para realizar esta acción.")
    
    if request.method == 'POST':
        option = get_object_or_404(MultipleChoiceOption, id=option_id)
        option.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Opción eliminada correctamente.'
        })
    
    return JsonResponse({'success': False, 'message': 'Método no permitido.'}, status=405)


# Vistas para estudiantes
class CourseDetailView(LoginRequiredMixin, DetailView):
    """Vista de detalle de un curso para estudiantes."""
    model = Course
    template_name = 'courses/course_detail.html'
    context_object_name = 'course'
    
    def get_queryset(self):
        # Solo mostrar cursos publicados
        return Course.objects.filter(is_published=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obtener módulos ordenados
        modules = Module.objects.filter(course=self.object).order_by('order')
        context['modules'] = modules
        
        return context


class ModuleDetailView(LoginRequiredMixin, DetailView):
    """Vista de detalle de un módulo para estudiantes."""
    model = Module
    template_name = 'courses/module_detail.html'
    context_object_name = 'module'
    pk_url_kwarg = 'module_id'
    
    def get_queryset(self):
        # Solo mostrar módulos de cursos publicados
        return Module.objects.filter(course__is_published=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obtener secciones ordenadas
        sections = Section.objects.filter(module=self.object).order_by('order')
        context['sections'] = sections
        
        # Verificar si existe un test de desarrollo para este módulo
        try:
            essay_test = EssayTest.objects.get(module=self.object)
            context['essay_test'] = essay_test
            
            # Verificar si el usuario ya ha realizado este test
            user_attempt = EssayAttempt.objects.filter(user=self.request.user, test=essay_test).first()
            context['user_attempt'] = user_attempt
            
            # Verificar si tiene cupones disponibles
            available_coupon = TestCoupon.objects.filter(
                user=self.request.user,
                test=essay_test,
                is_used=False
            ).exists()
            context['has_available_coupon'] = available_coupon
            
        except EssayTest.DoesNotExist:
            pass
        
        return context


class SectionDetailView(LoginRequiredMixin, DetailView):
    """Vista de detalle de una sección para estudiantes."""
    model = Section
    template_name = 'courses/section_detail.html'
    context_object_name = 'section'
    pk_url_kwarg = 'section_id'
    
    def get_queryset(self):
        # Solo mostrar secciones de cursos publicados
        return Section.objects.filter(module__course__is_published=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obtener actividades
        context['flashcards'] = FlashCard.objects.filter(section=self.object).order_by('order')
        context['concept_connections'] = ConceptConnection.objects.filter(section=self.object).order_by('order')
        context['multiple_choice_tests'] = MultipleChoiceTest.objects.filter(section=self.object).order_by('order')
        
        return context


class ConceptConnectionDetailView(LoginRequiredMixin, DetailView):
    """Vista de detalle de un ejercicio de conexión de conceptos."""
    model = ConceptConnection
    template_name = 'courses/activities/concept_connection_detail.html'
    context_object_name = 'connection'
    pk_url_kwarg = 'connection_id'
    
    def get_queryset(self):
        # Solo mostrar actividades de cursos publicados
        return ConceptConnection.objects.filter(section__module__course__is_published=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obtener conceptos ordenados
        concepts = Concept.objects.filter(connection=self.object).order_by('order')
        context['concepts'] = concepts
        
        # Obtener información de la sección y el curso
        context['section'] = self.object.section
        context['module'] = self.object.section.module
        context['course'] = self.object.section.module.course
        
        return context


class MultipleChoiceTestDetailView(LoginRequiredMixin, DetailView):
    """Vista de detalle de un test de opciones múltiples."""
    model = MultipleChoiceTest
    template_name = 'courses/activities/multiple_choice_test_detail.html'
    context_object_name = 'test'
    pk_url_kwarg = 'test_id'
    
    def get_queryset(self):
        # Solo mostrar actividades de cursos publicados
        return MultipleChoiceTest.objects.filter(section__module__course__is_published=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obtener preguntas ordenadas
        questions = MultipleChoiceQuestion.objects.filter(test=self.object).order_by('order')
        context['questions'] = []
        
        for question in questions:
            # Opciones para cada pregunta
            options = MultipleChoiceOption.objects.filter(question=question).order_by('order')
            context['questions'].append({
                'question': question,
                'options': options
            })
        
        # Obtener información de la sección y el curso
        context['section'] = self.object.section
        context['module'] = self.object.section.module
        context['course'] = self.object.section.module.course
        
        return context


class FlashcardListView(LoginRequiredMixin, ListView):
    """Vista para mostrar las flashcards de una sección."""
    model = FlashCard
    template_name = 'courses/activities/flashcard_list.html'
    context_object_name = 'flashcards'
    
    def get_queryset(self):
        section_id = self.kwargs.get('section_id')
        self.section = get_object_or_404(
            Section.objects.filter(module__course__is_published=True),
            id=section_id
        )
        return FlashCard.objects.filter(section=self.section).order_by('order')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = self.section
        context['module'] = self.section.module
        context['course'] = self.section.module.course
        return context


class EssayTestAttemptView(LoginRequiredMixin, FormView):
    """Vista para iniciar un intento de test de desarrollo."""
    form_class = EssayTestAttemptForm
    template_name = 'courses/essay_test_confirm.html'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial'] = {'user': self.request.user, 'test_id': self.kwargs.get('test_id')}
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        test_id = self.kwargs.get('test_id')
        self.test = get_object_or_404(
            EssayTest.objects.filter(module__course__is_published=True),
            id=test_id
        )
        
        context['test'] = self.test
        context['module'] = self.test.module
        context['course'] = self.test.module.course
        
        # Verificar si el usuario ya ha realizado este test
        user_attempt = EssayAttempt.objects.filter(user=self.request.user, test=self.test).first()
        context['user_attempt'] = user_attempt
        
        # Verificar si tiene cupones disponibles
        available_coupon = TestCoupon.objects.filter(
            user=self.request.user,
            test=self.test,
            is_used=False
        ).exists()
        context['has_available_coupon'] = available_coupon
        
        return context
    
    def form_valid(self, form):
        test_id = form.cleaned_data['test_id']
        test = get_object_or_404(EssayTest, id=test_id)
        user = self.request.user
        
        # Verificar si ya existe un intento previo
        previous_attempt = EssayAttempt.objects.filter(user=user, test=test).first()
        
        if previous_attempt:
            # Usar un cupón disponible
            coupon = TestCoupon.objects.filter(user=user, test=test, is_used=False).first()
            if coupon:
                coupon.is_used = True
                coupon.used_date = timezone.now()
                coupon.save()
            else:
                # No debería llegar aquí debido a la validación en el formulario
                messages.error(self.request, _('No tienes cupones disponibles para este test.'))
                return redirect('courses:module_detail', module_id=test.module.id)
        
        # Crear nuevo intento
        attempt = EssayAttempt.objects.create(
            user=user,
            test=test,
            status='submitted'
        )
        
        return redirect('courses:essay_test_take', attempt_id=attempt.id)


class EssayTestTakeView(LoginRequiredMixin, DetailView):
    """Vista para responder un test de desarrollo."""
    model = EssayAttempt
    template_name = 'courses/essay_test_take.html'
    context_object_name = 'attempt'
    pk_url_kwarg = 'attempt_id'
    
    def get_queryset(self):
        # Verificar que el intento pertenece al usuario actual
        return EssayAttempt.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obtener detalles del test y las preguntas
        test = self.object.test
        questions = EssayQuestion.objects.filter(test=test).order_by('order')
        
        # Preparar formularios para cada pregunta
        question_forms = []
        
        for question in questions:
            # Verificar si ya existe una respuesta para esta pregunta
            try:
                answer = EssayAnswer.objects.get(attempt=self.object, question=question)
                initial_data = {'answer_text': answer.answer_text}
            except EssayAnswer.DoesNotExist:
                answer = None
                initial_data = {}
            
            # Crear formulario
            form = EssayAnswerForm(
                initial={
                    'answer_text': initial_data.get('answer_text', ''),
                    'question': question.id,
                    'attempt': self.object.id
                },
                prefix=f'question_{question.id}'
            )
            
            question_forms.append({
                'question': question,
                'form': form,
                'answer': answer
            })
        
        context['question_forms'] = question_forms
        context['test'] = test
        context['module'] = test.module
        context['course'] = test.module.course
        
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        
        # Verificar que el intento no ha sido procesado
        if self.object.status != 'submitted':
            messages.error(request, _('Este intento ya ha sido procesado y no puede ser modificado.'))
            return redirect('courses:essay_attempt_result', attempt_id=self.object.id)
        
        # Obtener preguntas del test
        test = self.object.test
        questions = EssayQuestion.objects.filter(test=test)
        
        # Guardar cada respuesta
        for question in questions:
            form = EssayAnswerForm(
                request.POST,
                prefix=f'question_{question.id}'
            )
            
            if form.is_valid():
                answer_text = form.cleaned_data['answer_text']
                
                # Guardar o actualizar respuesta
                answer, created = EssayAnswer.objects.update_or_create(
                    attempt=self.object,
                    question=question,
                    defaults={'answer_text': answer_text}
                )
            else:
                # Si hay errores en el formulario, volver a la página
                context = self.get_context_data(object=self.object)
                return render(request, self.template_name, context)
        
        # Actualizar estado del intento a "processing"
        self.object.status = 'processing'
        self.object.save()
        
        # Aquí se integraría con la API de IA para análisis
        # Por ahora, simulamos que se ha analizado
        
        # TODO: Integrar con API de IA
        
        messages.success(request, _('Tus respuestas han sido enviadas para su análisis.'))
        return redirect('courses:essay_attempt_result', attempt_id=self.object.id)


class EssayAttemptResultView(LoginRequiredMixin, DetailView):
    """Vista para mostrar los resultados de un intento de test de desarrollo."""
    model = EssayAttempt
    template_name = 'courses/essay_attempt_result.html'
    context_object_name = 'attempt'
    pk_url_kwarg = 'attempt_id'
    
    def get_queryset(self):
        # Verificar que el intento pertenece al usuario actual
        return EssayAttempt.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obtener respuestas con sus preguntas
        answers = EssayAnswer.objects.filter(attempt=self.object).select_related('question')
        context['answers'] = answers
        
        # Obtener información adicional
        test = self.object.test
        context['test'] = test
        context['module'] = test.module
        context['course'] = test.module.course
        
        # Verificar si tiene cupones disponibles
        available_coupon = TestCoupon.objects.filter(
            user=self.request.user,
            test=test,
            is_used=False
        ).exists()
        context['has_available_coupon'] = available_coupon
        
        return context