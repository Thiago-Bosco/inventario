from django.contrib import admin
from .models import Job

class JobAdmin(admin.ModelAdmin):
    list_display = ('id', 'job_name', 'job_stream', 'workstation', 'aplicacao', 'activation_time', 'criticality', 'descricao')
    search_fields = ('id', 'job_name', 'job_stream', 'aplicacao', 'first_responsible', 'descricao')
    list_filter = ('criticality', 'job_stream', 'aplicacao')
    list_display_links = ('id', 'job_name')

    fields = ('job_name', 'job_stream', 'workstation', 'aplicacao', 'activation_time', 'first_responsible', 'second_responsible', 'third_responsible', 'criticality', 'descricao')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if change:
            self.message_user(request, "Job atualizado com sucesso.")
        else:
            self.message_user(request, "Job criado com sucesso.")

admin.site.register(Job, JobAdmin)