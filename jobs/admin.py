
from django.contrib import admin
from .models import Job

class JobAdmin(admin.ModelAdmin):
    list_display = ('id', 'job_name', 'stream', 'workstation', 'application', 'activation_time', 'criticality', 'description')
    search_fields = ('id', 'job_name', 'stream', 'application', 'primary_responsible', 'description')
    list_filter = ('criticality', 'stream', 'application')
    list_display_links = ('id', 'job_name')

    fields = ('job_name', 'stream', 'workstation', 'application', 'activation_time', 'primary_responsible', 'secondary_responsible', 'tertiary_responsible', 'criticality', 'description')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if change:
            self.message_user(request, "Job atualizado com sucesso.")
        else:
            self.message_user(request, "Job criado com sucesso.")

admin.site.register(Job, JobAdmin)
