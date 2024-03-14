from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from .models import Aluno


class ListarAlunos(LoginRequiredMixin, ListView):
    template_name = 'listar_aluno.html'
    model = Aluno
    context_object_name = 'alunos'


class CadastrarAluno(LoginRequiredMixin, CreateView):
    template_name = 'cadastrar.html'
    model = Aluno
    fields = ['nome', 'matricula', 'email', 'telefone']
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Cadastrar Aluno"
        return context


class EditarAluno(LoginRequiredMixin, UpdateView):
    template_name = 'cadastrar.html'
    model = Aluno
    fields = ['nome', 'matricula', 'email', 'telefone']
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Editar Aluno"
        return context
