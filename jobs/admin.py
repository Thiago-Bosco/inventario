
from django.contrib import admin
from .models import Job

class JobAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome_job', 'stream_job', 'estacao_trabalho', 'aplicacao', 'horario_ativacao', 'criticidade', 'descricao')
    search_fields = ('id', 'nome_job', 'stream_job', 'aplicacao', 'responsavel_primario', 'descricao')
    list_filter = ('criticidade', 'stream_job', 'aplicacao')
    list_display_links = ('id', 'nome_job')

    fields = ('nome_job', 'stream_job', 'estacao_trabalho', 'aplicacao', 'horario_ativacao', 'responsavel_primario', 'responsavel_secundario', 'responsavel_terciario', 'criticidade', 'descricao')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if change:
            self.message_user(request, "Job atualizado com sucesso.")
        else:
            self.message_user(request, "Job criado com sucesso.")

admin.site.register(Job, JobAdmin)
