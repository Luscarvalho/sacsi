from django.db import models

MODALIDADE_CHOICES = (
    ('ENS', 'Ensino'),
    ('PES', 'Pesquisa'),
    ('EXT', 'Extensão'),
)


class Atividade(models.Model):
    id_atividade = models.AutoField(primary_key=True)
    codigo = models.CharField(unique=True, max_length=5)
    modalidade = models.CharField(max_length=3, choices=MODALIDADE_CHOICES)
    descricao = models.CharField(max_length=250)
    ch_min = models.IntegerField()
    ch_max = models.IntegerField()
    ap_max = models.IntegerField()

    def __str__(self):
        return self.codigo + ' - ' + self.descricao
