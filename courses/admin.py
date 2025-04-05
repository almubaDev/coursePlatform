from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import (
    Course, Module, Section,
    FlashCard, ConceptConnection, Concept,
    MultipleChoiceTest, MultipleChoiceQuestion, MultipleChoiceOption,
    EssayTest, EssayQuestion, EssayAttempt, EssayAnswer, TestCoupon
)


class ModuleInline(admin.StackedInline):
    model = Module
    extra = 1


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'created', 'updated', 'is_published']
    list_filter = ['is_published', 'created', 'updated']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ModuleInline]
    actions = ['publish_courses', 'unpublish_courses']
    
    def publish_courses(self, request, queryset):
        queryset.update(is_published=True)
        self.message_user(request, _('Los cursos seleccionados han sido publicados.'))
    publish_courses.short_description = _('Publicar cursos seleccionados')
    
    def unpublish_courses(self, request, queryset):
        queryset.update(is_published=False)
        self.message_user(request, _('Los cursos seleccionados han sido despublicados.'))
    unpublish_courses.short_description = _('Despublicar cursos seleccionados')


class SectionInline(admin.StackedInline):
    model = Section
    extra = 1


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order', 'created', 'updated']
    list_filter = ['course', 'created', 'updated']
    search_fields = ['title', 'description', 'course__title']
    inlines = [SectionInline]


class FlashCardInline(admin.TabularInline):
    model = FlashCard
    extra = 1


class ConceptInline(admin.TabularInline):
    model = Concept
    extra = 2


class ConceptConnectionInline(admin.StackedInline):
    model = ConceptConnection
    extra = 1


class MultipleChoiceTestInline(admin.StackedInline):
    model = MultipleChoiceTest
    extra = 1


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'module', 'order', 'created', 'updated']
    list_filter = ['module', 'created', 'updated']
    search_fields = ['title', 'content', 'module__title']
    inlines = [FlashCardInline, ConceptConnectionInline, MultipleChoiceTestInline]


class MultipleChoiceOptionInline(admin.TabularInline):
    model = MultipleChoiceOption
    extra = 4


@admin.register(MultipleChoiceQuestion)
class MultipleChoiceQuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'test', 'order']
    list_filter = ['test']
    search_fields = ['question_text', 'explanation']
    inlines = [MultipleChoiceOptionInline]


@admin.register(MultipleChoiceTest)
class MultipleChoiceTestAdmin(admin.ModelAdmin):
    list_display = ['title', 'section', 'order']
    list_filter = ['section']
    search_fields = ['title', 'description']


@admin.register(ConceptConnection)
class ConceptConnectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'section', 'order']
    list_filter = ['section']
    search_fields = ['title', 'description']
    inlines = [ConceptInline]


@admin.register(FlashCard)
class FlashCardAdmin(admin.ModelAdmin):
    list_display = ['question', 'section', 'order']
    list_filter = ['section']
    search_fields = ['question', 'answer']


class EssayQuestionInline(admin.TabularInline):
    model = EssayQuestion
    extra = 5


@admin.register(EssayTest)
class EssayTestAdmin(admin.ModelAdmin):
    list_display = ['title', 'module', 'created', 'updated']
    list_filter = ['created', 'updated']
    search_fields = ['title', 'description']
    inlines = [EssayQuestionInline]


class EssayAnswerInline(admin.StackedInline):
    model = EssayAnswer
    readonly_fields = ['question', 'answer_text', 'ai_feedback']
    extra = 0
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(EssayAttempt)
class EssayAttemptAdmin(admin.ModelAdmin):
    list_display = ['user', 'test', 'date_submitted', 'status', 'score']
    list_filter = ['status', 'date_submitted', 'date_analyzed']
    search_fields = ['user__email', 'test__title']
    readonly_fields = ['user', 'test', 'date_submitted', 'date_analyzed', 'status', 'ai_feedback', 'score']
    inlines = [EssayAnswerInline]
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        # Solo permitir ver, no editar
        return True


@admin.register(TestCoupon)
class TestCouponAdmin(admin.ModelAdmin):
    list_display = ['user', 'test', 'created', 'is_used', 'used_date']
    list_filter = ['is_used', 'created', 'used_date']
    search_fields = ['user__email', 'test__title']
    readonly_fields = ['used_date']
    
    def save_model(self, request, obj, form, change):
        # Si el cupón es marcado como usado y no tenía fecha de uso, establecerla ahora
        if obj.is_used and not obj.used_date:
            from django.utils import timezone
            obj.used_date = timezone.now()
        super().save_model(request, obj, form, change)