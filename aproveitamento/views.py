from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from .forms import AproveitamentoForm, AproveitamentoEditForm
from .models import Aproveitamento, Aluno


class ListarAproveitamento(LoginRequiredMixin, ListView):
    template_name = 'listar_aproveitamento.html'
    model = Aproveitamento
    context_object_name = 'aproveitamentos'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id_aluno = None

    def dispatch(self, request, *args, **kwargs):
        self.id_aluno = kwargs.get('pk', None)
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(aluno=Aluno.objects.get(id_aluno=self.id_aluno))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        aluno = Aluno.objects.get(id_aluno=self.id_aluno)
        context['id_aluno'] = self.id_aluno
        context['aluno_nome'] = aluno.nome
        return context


def selecionar_modalidade(request, pk):
    aluno = get_object_or_404(Aluno, pk=pk)
    return render(request, 'selecionar_modalidades.html', {'aluno': aluno})


class CadastrarAproveitamento(LoginRequiredMixin, CreateView):
    template_name = 'cadastrar.html'
    form_class = AproveitamentoForm
    model = Aproveitamento

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id_aluno = None
        self.modalidade = None

    def get_success_url(self):
        return reverse_lazy('listar_aproveitamento', kwargs={'pk': self.id_aluno})

    def dispatch(self, request, *args, **kwargs):
        self.id_aluno = kwargs.get('pk', None)
        self.modalidade = kwargs.get('modalidade', None)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.aluno = self.get_aluno()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Cadastrar Aproveitamento"
        return context

    def get_aluno(self):
        return Aluno.objects.get(id_aluno=self.id_aluno)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'id_aluno': self.id_aluno,
            'modalidade': self.modalidade,
            'request': self.request
        })
        return kwargs


class EditarAproveitamento(LoginRequiredMixin, UpdateView):
    template_name = 'cadastrar.html'
    model = Aproveitamento
    form_class = AproveitamentoEditForm

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id_aluno = None

    def dispatch(self, request, *args, **kwargs):
        aproveitamento = self.get_object()
        self.id_aluno = aproveitamento.aluno.id_aluno
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'id_aluno': self.id_aluno,
            'request': self.request
             })
        return kwargs

    def form_valid(self, form):
        self.id_aluno = form.instance.aluno.id_aluno
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('listar_aproveitamento', kwargs={'pk': self.id_aluno})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Editar Aproveitamento"
        return context


class DeletarAproveitamento(LoginRequiredMixin, DeleteView):
    model = Aproveitamento
    template_name = 'excluir.html'

    def get_success_url(self):
        id_aluno = self.object.aluno.id_aluno
        return reverse_lazy('listar_aproveitamento', kwargs={'pk': id_aluno})
