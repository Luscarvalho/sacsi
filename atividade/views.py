from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from .models import Atividade


class ListarEnsino(LoginRequiredMixin, ListView):
    template_name = 'listar_atividade.html'
    model = Atividade
    context_object_name = 'atividades'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(modalidade='ENS')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Ensino"
        return context


class ListarPesquisa(LoginRequiredMixin, ListView):
    template_name = 'listar_atividade.html'
    model = Atividade
    context_object_name = 'atividades'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(modalidade='PES')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Pesquisa"
        return context


class ListarExtensao(LoginRequiredMixin, ListView):
    template_name = 'listar_atividade.html'
    model = Atividade
    context_object_name = 'atividades'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(modalidade='EXT')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Extensão"
        return context


class CadastrarEnsino(LoginRequiredMixin, CreateView):
    template_name = 'cadastrar.html'
    model = Atividade
    fields = ['codigo', 'descricao', 'ch_min', 'ch_max', 'ap_max']
    success_url = reverse_lazy('listar_atividade_ensino')

    def form_valid(self, form):
        form.instance.modalidade = 'ENS'
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Cadastrar Ensino"
        return context


class CadastrarPesquisa(LoginRequiredMixin, CreateView):
    template_name = 'cadastrar.html'
    model = Atividade
    fields = ['codigo', 'descricao', 'ch_min', 'ch_max', 'ap_max']
    success_url = reverse_lazy('listar_atividade_pesquisa')

    def form_valid(self, form):
        form.instance.modalidade = 'PES'
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Cadastrar Pesquisa"
        return context


class CadastrarExtensao(LoginRequiredMixin, CreateView):
    template_name = 'cadastrar.html'
    model = Atividade
    fields = ['codigo', 'descricao', 'ch_min', 'ch_max', 'ap_max']
    success_url = reverse_lazy('listar_atividade_extensao')

    def form_valid(self, form):
        form.instance.modalidade = 'EXT'
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Cadastrar Extensão"
        return context


class EditarEnsino(LoginRequiredMixin, UpdateView):
    template_name = 'cadastrar.html'
    model = Atividade
    fields = ['codigo', 'descricao', 'ch_min', 'ch_max', 'ap_max']
    success_url = reverse_lazy('listar_atividade_ensino')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Editar Ensino"
        return context


class EditarPesquisa(LoginRequiredMixin, UpdateView):
    template_name = 'cadastrar.html'
    model = Atividade
    fields = ['codigo', 'descricao', 'ch_min', 'ch_max', 'ap_max']
    success_url = reverse_lazy('listar_atividade_pesquisa')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Editar Pesquisa"
        return context


class EditarExtensao(LoginRequiredMixin, UpdateView):
    template_name = 'cadastrar.html'
    model = Atividade
    fields = ['codigo', 'descricao', 'ch_min', 'ch_max', 'ap_max']
    success_url = reverse_lazy('listar_atividade_extensao')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Editar Extensão"
        return context


class DeletarEnsino(LoginRequiredMixin, DeleteView):
    model = Atividade
    template_name = 'excluir.html'
    success_url = reverse_lazy('listar_atividade_ensino')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Excluir Ensino"
        return context


class DeletarPesquisa(LoginRequiredMixin, DeleteView):
    model = Atividade
    template_name = 'excluir.html'
    success_url = reverse_lazy('listar_atividade_pesquisa')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Excluir Pesquisa"
        return context


class DeletarExtensao(LoginRequiredMixin, DeleteView):
    model = Atividade
    template_name = 'excluir.html'
    success_url = reverse_lazy('listar_atividade_extensao')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Excluir Extensão"
        return context
