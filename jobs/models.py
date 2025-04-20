from django.db import models
from servidores.models import Servidores_CC, Servidores_FastShop
class Job(models.Model):
    """
    Modelo para gerenciamento de jobs/tarefas.
    """
    nome_job = models.CharField('Nome do Job', max_length=255, blank=True)
    stream_job = models.CharField('Stream', max_length=255, blank=True, null=True)
    estacao_trabalho = models.CharField('Estação de Trabalho', max_length=255, blank=True, null=True)
    aplicacao = models.CharField('Aplicação', max_length=255, blank=True, null=True)
    responsavel_primario = models.CharField('Responsável Primário', max_length=255, blank=True, null=True)
    responsavel_secundario = models.CharField('Responsável Secundário', max_length=255, blank=True, null=True)
    responsavel_terciario = models.CharField('Responsável Terciário', max_length=255, blank=True, null=True)
    horario_ativacao = models.CharField('Horário de Ativação', max_length=255, blank=True, null=True)
    criticidade = models.CharField('Criticidade', max_length=255, blank=True, null=True)
    descricao = models.TextField('Descrição', blank=True, null=True)

    class Meta:
        verbose_name = 'Job'
        verbose_name_plural = 'Jobs'
        ordering = ['nome_job']

    def __str__(self):
        return self.nome_job or "Job sem nome"
    first_responsible = models.CharField(max_length=255, blank=True, null=True)
    second_responsible = models.CharField(max_length=255, blank=True, null=True)
    third_responsible = models.CharField(max_length=255, blank=True, null=True)
    activation_time = models.CharField(max_length=255, blank=True, null=True)
    criticality = models.CharField(max_length=255, blank=True, null=True)
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.job_name or "Nome não definido"


