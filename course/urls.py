from django.urls import path
from .views import *

urlpatterns = [
    path('', get_courses, name='get_courses'),
    path('section/', get_section, name='get_section'),
    path('sections/', get_course_sections, name='get_course_sections'),
    path('section/create/', create_section, name='create_section'),
    path('section/update/', update_section, name='create_section'),
]
