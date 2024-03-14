from django.urls import path
from relatorio import views

urlpatterns = [
    path('', views.RelatorioGeral.as_view(), name='relatorio'),
    path('exportar/', views.exportar_dados, name="exportar"),
    path('exportar/<int:pk>', views.exportar_dados_aluno_simples, name="exportar-simples"),
    path('exportar-completo/<int:pk>', views.exportar_dados_aluno_completo, name="exportar-completo"),
]
