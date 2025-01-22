from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.home_page, name='home'),
    path('patient/signup/', views.patient_signup, name='patient_signup'),
    path('doctor/signup/', views.doctor_signup, name='doctor_signup'),
    path('patient/dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('doctor/dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('create-blog/', views.create_blog, name='create_blog'),
    path('blogs/', views.my_blog, name='my_blog'),
    path('doctor/home/', views.doctor_home, name='doctor_home'),
    path('patient/home/', views.patient_home, name='patient_home'),
    path('blog_list/', views.blog_list, name='blog_list'),  # List of blogs
    path('blog/<uuid:blog_id>/', views.blog_detail, name='blog_detail'),

]
