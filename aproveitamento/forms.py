from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Sum
from django.contrib import messages
from .models import Aproveitamento, Atividade


class AproveitamentoForm(forms.ModelForm):
    class Meta:
        model = Aproveitamento
        fields = ['categoria', 'descricao', 'semestre', 'ano', 'ch']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.id_aluno = kwargs.pop('id_aluno', None)
        self.modalidade = kwargs.pop('modalidade', None)
        super().__init__(*args, **kwargs)
        if self.modalidade is not None:
            self.fields['categoria'].queryset = Atividade.objects.filter(modalidade=self.modalidade)

    def clean(self):
        cleaned_data = super().clean()
        ch = cleaned_data.get('ch')
        categoria = cleaned_data.get('categoria')

        if ch == 0:
            raise ValidationError("A carga horária não pode ser 0.")

        if categoria and ch:
            if ch < categoria.ch_min or ch > categoria.ch_max:
                raise ValidationError(
                    f"A carga horária deve estar entre {categoria.ch_min} e {categoria.ch_max} horas.")

            total_ch = Aproveitamento.objects.filter(categoria=categoria,
                                                     aluno=self.id_aluno).aggregate(Sum('ch'))['ch__sum'] or 0
            restante_ch = categoria.ap_max - total_ch
            if total_ch + ch > categoria.ap_max:
                cleaned_data['ch'] = restante_ch
                (messages.warning(self.request,
                                  f'A carga horária de {categoria} foi ajustada de {ch} para {restante_ch}. '
                                  'Isso ocorreu para não exceder o limite máximo de aproveitamento.'))
            if total_ch == categoria.ap_max:
                raise ValidationError(
                    f"A carga horária da atividade {categoria} já atingiu o limite máximo de aproveitamento.")
        return cleaned_data


class AproveitamentoEditForm(forms.ModelForm):
    class Meta:
        model = Aproveitamento
        fields = ['categoria', 'descricao', 'semestre', 'ano', 'ch']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.id_aluno = kwargs.pop('id_aluno', None)
        super().__init__(*args, **kwargs)
        self.fields['categoria'].widget = forms.HiddenInput()
        self.original_ch = self.instance.ch

    def clean(self):
        cleaned_data = super().clean()
        ch = cleaned_data.get('ch')
        categoria = cleaned_data.get('categoria')

        if ch == 0:
            raise ValidationError("A carga horária não pode ser 0.")

        if categoria and ch:
            if ch < categoria.ch_min or ch > categoria.ch_max:
                raise ValidationError(
                    f"A carga horária deve estar entre {categoria.ch_min} e {categoria.ch_max} horas.")

            total_ch = Aproveitamento.objects.filter(categoria=categoria,
                                                     aluno=self.id_aluno).aggregate(Sum('ch'))['ch__sum'] or 0
            total_ch -= self.original_ch
            restante_ch = categoria.ap_max - total_ch
            if total_ch + ch > categoria.ap_max:
                cleaned_data['ch'] = restante_ch
                (messages.warning(self.request,
                                  f'A carga horária de {categoria} foi ajustada de {ch} para {restante_ch}. '
                                  'Isso ocorreu para não exceder o limite máximo de aproveitamento.'))
        return cleaned_data
