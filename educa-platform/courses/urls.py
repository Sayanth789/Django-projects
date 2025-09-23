from django.urls import path
from . import views

urlpatterns = [
    # Course management
    path(
        'mine/',
        views.ManageCourseListView.as_view(),
        name='manage_course_list'
    ),
    path(
        'create/',
        views.CourseCreateView.as_view(),
        name='course_create'
    ),
    path(
        '<int:pk>/edit/',
        views.CourseUpdateView.as_view(),
        name='course_edit'
    ),
    path(
        '<int:pk>/delete/',
        views.CourseDeleteView.as_view(),
        name='course_delete'
    ),
    path(
        '<int:pk>/module/',
        views.CourseModuleUpdateView.as_view(),
        name='course_module_update'
    ),

    # Module content create/update/delete
    path(
        'module/<int:module_id>/content/<model_name>/create/',
        views.ContentCreateUpdateView.as_view(),
        name='module_content_create'
    ),
    path(
        'module/<int:module_id>/content/<model_name>/<int:id>/',
        views.ContentCreateUpdateView.as_view(),
        name='module_content_update'
    ),
    path(
        'content/<int:id>/delete/',
        views.ContentDeleteView.as_view(),
        name='module_content_delete'
    ),

    # Module content list and ordering
    path(
        'module/<int:module_id>/',
        views.ModuleContentListView.as_view(),
        name='module_content_list'
    ),
    path(
        'module/order/',
        views.ModuleOrderView.as_view(),
        name='module_order'
    ),
    path(
        'content/order/',
        views.ContentOrderView.as_view(),
        name='content_order'
    ),

    # Course listing by subject
    path(
        'subject/<slug:subject>/',
        views.CourseListView.as_view(),
        name='course_list_subject'
    ),

    # Course detail (generic slug)
    path(
        '<slug:slug>/',
        views.CourseDetailView.as_view(),
        name='course_detail'
    ),
    path('', views.CourseListView.as_view(), name='course_list'),
]

# Notes:
# <int:pk> refers to the primary key of a Course object
# module_content_create: create a new Text, Video, Image, or File content object for a module
# module_content_update: update an existing content object, includes its id
# More specific URLs are listed first; generic slug URL is last to avoid conflicts
