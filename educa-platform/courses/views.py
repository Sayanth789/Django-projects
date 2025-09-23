from braces.views import CsrfExemptMixin, JsonRequestResponseMixin
from django.views.generic.base import TemplateResponseMixin, View
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.apps import apps
from django.forms.models import modelform_factory
from django.views.generic.detail import DetailView
from .models import Module, Content, Course, Subject
from .forms import ModuleFormSet
from students.forms import CourseEnrollForm
from django.http import Http404
from django.core.cache import cache
from django.db.models import Count
from . forms import ModuleFormSet

# ------------------------------
# Content Create/Update View
# ------------------------------
class ContentCreateUpdateView(TemplateResponseMixin, View):
    """
    Handles creation and update of course content objects (Text, Video, Image, File).
    Uses TemplateResponseMixin to render templates and provide a context.
    """

    module = None  # Current module instance
    model = None   # Content model class (Text, Video, Image, File)
    obj = None     # Instance of content object (for update)
    template_name = 'course/manage/content/form.html'

    def get_model(self, model_name):
        """
        Returns the model class for the given model_name.
        Raises 404 if model_name is invalid.
        """
        if model_name not in ['text', 'video', 'image', 'file']:
            raise Http404("Invalid content type")
        return apps.get_model(app_label='courses', model_name=model_name)

    def get_form(self, model, *args, **kwargs):
        """
        Creates a ModelForm dynamically using modelform_factory.
        Excludes fields: owner, order, created, updated (these are set automatically).
        """
        Form = modelform_factory(
            model, exclude=['owner', 'order', 'created', 'updated']
        )
        return Form(*args, **kwargs)

    def dispatch(self, request, module_id, model_name, id=None, *args, **kwargs):
        """
        Overridden dispatch method.
        Sets self.module, self.model, and self.obj (if updating) before handling GET/POST.
        """
        # Get module owned by current user
        self.module = get_object_or_404(
            Module, id=module_id, course__owner=request.user
        )
        # Get model class for content type
        self.model = self.get_model(model_name)
        # If updating, get the content object
        if id:
            self.obj = get_object_or_404(
                self.model, id=id, owner=request.user
            )
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, module_id, model_name, id=None):
        """
        Handles GET request.
        Renders the form for creating or updating content.
        """
        form = self.get_form(self.model, instance=self.obj)
        return self.render_to_response({'form': form, 'object': self.obj})

    def post(self, request, module_id, model_name, id=None):
        """
        Handles POST request.
        Saves new or updated content object and associates it with the module.
        Redirects to module content list on success.
        """
        form = self.get_form(
            self.model,
            instance=self.obj,
            data=request.POST,
            files=request.FILES
        )
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            if not id:
                # Create Content linking the new object to the module
                Content.objects.create(module=self.module, item=obj)
            return redirect('module_content_list', self.module.id)
        return self.render_to_response({'form': form, 'object': self.obj})


# ------------------------------
# Course Module Update View
# ------------------------------
class CourseModuleUpdateView(TemplateResponseMixin, View):
    """
    Manages multiple modules of a course using a formset.
    Only accessible to the course owner.
    """
    template_name = 'course/manage/module/formset.html'
    course = None

    def get_formset(self, data=None):
        """Returns a ModuleFormSet bound to the current course."""
        return ModuleFormSet(instance=self.course, data=data)

    def dispatch(self, request, *args, **kwargs):
        """Sets self.course before GET or POST."""
        pk = kwargs.get("pk")
        self.course = get_object_or_404(Course, id=pk, owner=request.user)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """Renders the module formset for editing."""
        formset = self.get_formset()
        return self.render_to_response({'course': self.course, 'formset': formset})

    def post(self, request, *args, **kwargs):
        """Validates and saves the formset, then redirects to course list."""
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('manage_course_list')
        return self.render_to_response({'course': self.course, 'formset': formset})


# ------------------------------
# Mixins for owner-based filtering and editing
# ------------------------------
class OwnerMixin:
    """Filters queryset to include only objects owned by the current user."""
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)


class OwnerEditMixin:
    """Automatically assigns current user as owner before saving a form."""
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class OwnerCourseMixin(OwnerMixin, LoginRequiredMixin, PermissionRequiredMixin):
    """
    Base mixin for course-related views.
    Sets model, fields, success URL.
    """
    model = Course
    fields = ['subject', 'slug', 'overview']
    success_url = reverse_lazy('manage_course_list')


class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    """Mixin for creating/updating courses with a template specified."""
    template_name = 'course/manage/course/form.html'


# ------------------------------
# Course Views
# ------------------------------
class ManageCourseListView(OwnerCourseMixin, ListView):
    """Lists courses owned by the current user."""
    template_name = 'course/manage/course/list.html'
    permission_required = 'course.view_course'


class CourseCreateView(OwnerCourseEditMixin, CreateView):
    """View for creating a new course."""
    permission_required = 'course.add_course'


class CourseUpdateView(OwnerCourseEditMixin, UpdateView):
    """View for editing an existing course."""
    permission_required = 'course.change_course'


class CourseListView(TemplateResponseMixin, View):
    model = Course
    template_name = 'courses/course/list.html'

    def get(self, request, subject=None):
        subjects = cache.get('all_subjects')
        if not subjects:
            subjects = Subject.objects.annotate(
                total_courses=Count('course')
            )
            cache.set('all_subjects', subjects)
        all_courses = Course.objects.annotate(
            num_modules=Count('modules')
        )
        if subject:
            subject = get_object_or_404(Subject, slug=subject)
            key = f'subject_{subject.id}_courses'
            courses = cache.get(key)
            if not courses:
                courses = all_courses.filter(subject=subject)
                cache.set(key, courses)
        else:
            courses = cache.get('all_courses')
            if not courses:
                courses = all_courses
                cache.set('all_courses', courses)
        return self.render_to_response(
            {
                'subjects': subjects,
                'subject': subject,
                'courses': courses,
            }
        )

class CourseDeleteView(OwnerCourseMixin, DeleteView):
    """View for deleting a course."""
    template_name = 'course/manage/course/delete.html'
    permission_required = 'course.delete_course'
    success_url = reverse_lazy('manage_course_list')

class CourseDetailView(DetailView):
    """
    Shows detailed information for a single course.
    """
    model = Course
    template_name = 'course/course/detail.html'  # Update path to your template

    # Optionally, filter by owner if needed
    def get_queryset(self):
        qs = super().get_queryset()
        return qs  # or: qs.filter(owner=self.request.user) if you want owner restriction

# ------------------------------
# Content Delete View
# ------------------------------
class ContentDeleteView(View):
    """
    Deletes a content object along with its associated item (Text, Video, Image, File).
    Redirects to module content list after deletion.
    """
    def post(self, request, id):
        content = get_object_or_404(Content, id=id, module__course__owner=request.user)
        module = content.module
        content.item.delete()
        content.delete()
        return redirect('module_content_list', module.id)


# ------------------------------
# Module Content List View
# ------------------------------
class ModuleContentListView(TemplateResponseMixin, View):
    """
    Lists all content objects for a module.
    Only accessible to the module's course owner.
    """
    template_name = 'course/manage/module/content_list.html'

    def get(self, request, module_id):
        module = get_object_or_404(Module, id=module_id, course__owner=request.user)
        return self.render_to_response({'module': module})


# ------------------------------
# Module and Content Ordering Views (AJAX)
# ------------------------------
class ModuleOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):
    """Updates the order of modules in a course via AJAX."""
    def post(self, request):
        for id, order in self.request_json.items():
            Module.objects.filter(id=id, course__owner=request.user).update(order=order)
        return self.render_json_response({'saved': 'OK'})


class ContentOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):
    """Updates the order of content objects in a module via AJAX."""
    def post(self, request):
        for id, order in self.request_json.items():
            Content.objects.filter(id=id, module__course__owner=request.user).update(order=order)
        return self.render_json_response({'saved': 'OK'})
