from django.urls import path
from django.contrib.admin.views.decorators import staff_member_required

from . import views

app_name = 'courses'

urlpatterns = [
    # Rutas para la administración de cursos (solo superusuarios)
    path('admin/', staff_member_required(views.CourseListView.as_view()), name='admin_course_list'),
    path('admin/course/create/', staff_member_required(views.CourseCreateView.as_view()), name='admin_course_create'),
    path('admin/course/<slug:slug>/', staff_member_required(views.CourseUpdateView.as_view()), name='admin_course_update'),
    path('admin/course/<slug:slug>/delete/', staff_member_required(views.CourseDeleteView.as_view()), name='admin_course_delete'),
    
    # Módulos
    path('admin/course/<slug:course_slug>/modules/', staff_member_required(views.ModuleListView.as_view()), name='admin_module_list'),
    path('admin/course/<slug:course_slug>/module/create/', staff_member_required(views.ModuleCreateView.as_view()), name='admin_module_create'),
    path('admin/module/<int:module_id>/', staff_member_required(views.ModuleUpdateView.as_view()), name='admin_module_update'),
    path('admin/module/<int:module_id>/delete/', staff_member_required(views.ModuleDeleteView.as_view()), name='admin_module_delete'),
    
    # Secciones
    path('admin/module/<int:module_id>/sections/', staff_member_required(views.SectionListView.as_view()), name='admin_section_list'),
    path('admin/module/<int:module_id>/section/create/', staff_member_required(views.SectionCreateView.as_view()), name='admin_section_create'),
    path('admin/section/<int:section_id>/', staff_member_required(views.SectionUpdateView.as_view()), name='admin_section_update'),
    path('admin/section/<int:section_id>/delete/', staff_member_required(views.SectionDeleteView.as_view()), name='admin_section_delete'),
    
    # Actividades
    path('admin/section/<int:section_id>/activities/', staff_member_required(views.ActivityListView.as_view()), name='admin_activity_list'),
    
    # Flashcards
    path('admin/section/<int:section_id>/flashcard/create/', staff_member_required(views.FlashcardCreateView.as_view()), name='admin_flashcard_create'),
    path('admin/flashcard/<int:flashcard_id>/', staff_member_required(views.FlashcardUpdateView.as_view()), name='admin_flashcard_update'),
    path('admin/flashcard/<int:flashcard_id>/delete/', staff_member_required(views.FlashcardDeleteView.as_view()), name='admin_flashcard_delete'),
    
    # Conexiones de conceptos
    path('admin/section/<int:section_id>/concept-connection/create/', staff_member_required(views.ConceptConnectionCreateView.as_view()), name='admin_concept_connection_create'),
    path('admin/concept-connection/<int:connection_id>/', staff_member_required(views.ConceptConnectionUpdateView.as_view()), name='admin_concept_connection_update'),
    path('admin/concept-connection/<int:connection_id>/delete/', staff_member_required(views.ConceptConnectionDeleteView.as_view()), name='admin_concept_connection_delete'),
    
    # API para conceptos (AJAX)
    path('admin/api/concept-connection/<int:connection_id>/save-concept/', views.save_concept, name='admin_save_concept'),
    path('admin/api/concept/<int:concept_id>/delete/', views.delete_concept, name='admin_delete_concept'),
    
    # Test de alternativas múltiples
    path('admin/section/<int:section_id>/multiple-choice/create/', staff_member_required(views.MultipleChoiceTestCreateView.as_view()), name='admin_multiple_choice_create'),
    path('admin/multiple-choice/<int:test_id>/', staff_member_required(views.MultipleChoiceTestUpdateView.as_view()), name='admin_multiple_choice_update'),
    path('admin/multiple-choice/<int:test_id>/delete/', staff_member_required(views.MultipleChoiceTestDeleteView.as_view()), name='admin_multiple_choice_delete'),
    
    # Preguntas de tests de alternativas múltiples
    path('admin/multiple-choice/<int:test_id>/question/create/', staff_member_required(views.MultipleChoiceQuestionCreateView.as_view()), name='admin_multiple_choice_question_create'),
    path('admin/multiple-choice-question/<int:question_id>/', staff_member_required(views.MultipleChoiceQuestionUpdateView.as_view()), name='admin_multiple_choice_question_update'),
    path('admin/multiple-choice-question/<int:question_id>/delete/', staff_member_required(views.MultipleChoiceQuestionDeleteView.as_view()), name='admin_multiple_choice_question_delete'),
    
    # API para opciones de preguntas (AJAX)
    path('admin/api/question/<int:question_id>/save-option/', views.save_option, name='admin_save_option'),
    path('admin/api/option/<int:option_id>/delete/', views.delete_option, name='admin_delete_option'),
    
    # Tests de desarrollo
    path('admin/module/<int:module_id>/essay-test/create/', staff_member_required(views.EssayTestCreateView.as_view()), name='admin_essay_test_create'),
    path('admin/essay-test/<int:test_id>/', staff_member_required(views.EssayTestUpdateView.as_view()), name='admin_essay_test_update'),
    path('admin/essay-test/<int:test_id>/delete/', staff_member_required(views.EssayTestDeleteView.as_view()), name='admin_essay_test_delete'),
    
    # Preguntas de desarrollo
    path('admin/essay-test/<int:test_id>/question/create/', staff_member_required(views.EssayQuestionCreateView.as_view()), name='admin_essay_question_create'),
    path('admin/essay-question/<int:question_id>/', staff_member_required(views.EssayQuestionUpdateView.as_view()), name='admin_essay_question_update'),
    path('admin/essay-question/<int:question_id>/delete/', staff_member_required(views.EssayQuestionDeleteView.as_view()), name='admin_essay_question_delete'),
    
    # Gestión de intentos de tests de desarrollo
    path('admin/essay-attempts/', staff_member_required(views.EssayAttemptListView.as_view()), name='admin_essay_attempt_list'),
    path('admin/essay-attempt/<int:attempt_id>/', staff_member_required(views.EssayAttemptDetailView.as_view()), name='admin_essay_attempt_detail'),
    
    # Gestión de cupones
    path('admin/coupons/', staff_member_required(views.TestCouponListView.as_view()), name='admin_coupon_list'),
    path('admin/coupon/create/', staff_member_required(views.TestCouponCreateView.as_view()), name='admin_coupon_create'),
    
    # URLs para estudiantes
    path('courses/', views.CourseListView.as_view(), name='course_list'),
    path('course/<slug:slug>/', views.CourseDetailView.as_view(), name='course_detail'),
    path('module/<int:module_id>/', views.ModuleDetailView.as_view(), name='module_detail'),
    path('section/<int:section_id>/', views.SectionDetailView.as_view(), name='section_detail'),
    
    # Actividades para estudiantes
    path('section/<int:section_id>/flashcards/', views.FlashcardListView.as_view(), name='flashcard_list'),
    path('concept-connection/<int:connection_id>/', views.ConceptConnectionDetailView.as_view(), name='concept_connection_detail'),
    path('multiple-choice/<int:test_id>/', views.MultipleChoiceTestDetailView.as_view(), name='multiple_choice_test'),
    
    # Tests de desarrollo para estudiantes
    path('essay-test/<int:test_id>/start/', views.EssayTestAttemptView.as_view(), name='essay_test_start'),
    path('essay-test/attempt/<int:attempt_id>/', views.EssayTestTakeView.as_view(), name='essay_test_take'),
    path('essay-test/result/<int:attempt_id>/', views.EssayAttemptResultView.as_view(), name='essay_attempt_result'),
]