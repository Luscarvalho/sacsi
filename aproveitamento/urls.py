from django.urls import path
from aproveitamento import views

urlpatterns = [
    path('<int:pk>', views.ListarAproveitamento.as_view(), name="listar_aproveitamento"),
    path('selecionar_modalidades/<int:pk>', views.selecionar_modalidade, name="selecionar_modalidades"),
    path('cadastrar/<int:pk>/<str:modalidade>',
         views.CadastrarAproveitamento.as_view(), name="cadastrar_aproveitamento"),
    path('editar/<int:pk>', views.EditarAproveitamento.as_view(), name="editar_aproveitamento"),
    path('excluir/<int:pk>', views.DeletarAproveitamento.as_view(), name="excluir_aproveitamento"),
]
