from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
   
    path('admin/login/', views.admin_login, name='admin_login'),
    path('user/login/', views.user_login, name='user_login'),
    path('', views.home, name='home'),  # Define the home page URL
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),  # Add the logout URL
    path('add_review/<int:product_id>/', views.add_review, name='add_review'),  # New review page URL
 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
