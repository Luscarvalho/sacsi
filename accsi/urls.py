from django.urls import path, include
from django.contrib import admin
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Auth Urls
    path('login/', auth_views.LoginView.as_view(
        template_name='login.html'
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Admin Url
    path('admin/', admin.site.urls),

    # App Urls
    path('', include('aluno.urls')),
    path('relatorio/', include('relatorio.urls')),
    path('atividade/', include('atividade.urls')),
    path('aproveitamento/', include('aproveitamento.urls')),
]
