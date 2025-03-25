
from django.contrib import admin
from django.contrib import messages
from .models import Hardware, AccessLog, Inventory, InventoryMovement

def marcar_manutencao(modeladmin, request, queryset):
    queryset.update(status_contrato='Em Manutenção')
marcar_manutencao.short_description = "Marcar itens selecionados como Em Manutenção"

def marcar_ativo(modeladmin, request, queryset):
    queryset.update(status_contrato='Ativo')
marcar_ativo.short_description = "Marcar itens selecionados como Ativo"

class HardwareAdmin(admin.ModelAdmin):
    list_display = ('marca', 'modelo', 'serial_number', 'local', 'status_contrato', 'dias_para_termino', 'alerta')
    list_filter = ('status_contrato', 'local', 'marca', 'fornecedor_manut')
    search_fields = ('marca', 'modelo', 'serial_number', 'ip')
    ordering = ('marca', 'modelo')
    actions = [marcar_manutencao, marcar_ativo]

    fieldsets = (
        ('Informações Básicas', {
            'fields': ('marca', 'modelo', 'serial_number', 'descricao')
        }),
        ('Localização', {
            'fields': ('local', 'end_datacenter', 'rack', 'storage', 'ip')
        }),
        ('Manutenção', {
            'fields': ('fornecedor_manut', 'data_inicial_manut', 'data_final_manut', 
                      'meses_contratados', 'dias_para_termino', 'status_contrato')
        }),
        ('Status', {
            'fields': ('brand', 'alerta')
        })
    )

    list_per_page = 20
    date_hierarchy = 'data_inicial_manut'

class AccessLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'user')
    search_fields = ('user',)
    list_filter = ('timestamp',)

from django.utils.html import format_html
from django.contrib import admin, messages
from decimal import Decimal

def marcar_disponivel(modeladmin, request, queryset):
    queryset.update(status='available')
marcar_disponivel.short_description = "Marcar itens como Disponível"

def marcar_manutencao(modeladmin, request, queryset):
    queryset.update(status='maintenance')
marcar_manutencao.short_description = "Marcar itens para Manutenção"

class InventoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'formatted_quantity', 'formatted_price', 'category', 'status_colored', 'priority', 'next_maintenance', 'supplier', 'location')
    list_filter = ('category', 'status', 'priority', 'location', 'supplier')
    search_fields = ('name', 'description', 'category', 'supplier', 'notes', 'barcode')
    readonly_fields = ('created_at', 'updated_at', 'qr_code', 'barcode')

    fieldsets = (
        ('Informações do Item', {
            'fields': (
                'name', 'description', 'image', 'barcode', 'qr_code',
                'quantity', 'minimum_quantity', 'unit_price',
                'location', 'status', 'supplier', 'category',
                'notes', 'warranty_expiration',
                'maintenance_interval', 'last_maintenance', 'next_maintenance', 'priority',
                'created_at', 'updated_at'
            )
        }),
    )

    class Media:
        css = {
            'all': [
                'admin/css/forms.css',
                'https://code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css'
            ]
        }
        js = [
            'https://code.jquery.com/jquery-3.6.0.min.js',
            'https://code.jquery.com/ui/1.12.1/jquery-ui.min.js',
            'admin/js/jquery.init.js'
        ]

    class Media:
        js = [
            'admin/js/jquery.init.js',
            'admin/js/collapse.js',
            'admin/js/core.js'
        ]
        css = {
            'all': [
                'admin/css/forms.css',
                'admin/css/base.css'
            ]
        }

    def save_model(self, request, obj, form, change):
        if obj.quantity <= obj.minimum_quantity:
            messages.warning(request, f'Atenção: O item {obj.name} está com quantidade abaixo ou igual ao mínimo!')
        obj.full_clean()
        super().save_model(request, obj, form, change)

    def formatted_quantity(self, obj):
        html = f"{obj.quantity} un."
        if obj.is_low_stock():
            html = f'<span style="color: red;">{html}</span>'
        return format_html(html)
    formatted_quantity.short_description = "Quantidade"

    def formatted_price(self, obj):
        if obj.unit_price:
            total = obj.get_total_value()
            return format_html('R$ {:.2f}<br/><small>Total: R$ {:.2f}</small>', 
                             obj.unit_price, total)
        return '-'
    formatted_price.short_description = "Preço Un./Total"

    def status_colored(self, obj):
        colors = {
            'available': 'green',
            'in_use': 'blue',
            'maintenance': 'orange',
            'reserved': 'purple',
            'discontinued': 'red'
        }
        return format_html('<span style="color: {};">{}</span>',
                         colors.get(obj.status, 'black'),
                         obj.get_status_display())
    status_colored.short_description = "Status"

    def dias_garantia(self, obj):
        if obj.warranty_expiration:
            dias = (obj.warranty_expiration - timezone.now().date()).days
            if dias < 0:
                return format_html('<span style="color: red;">Vencida</span>')
            elif dias <= 30:
                return format_html('<span style="color: orange;">{} dias</span>', dias)
            return f"{dias} dias"
        return "-"
    dias_garantia.short_description = "Garantia"

admin.site.register(Inventory, InventoryAdmin)
admin.site.register(Hardware, HardwareAdmin)
class InventoryMovementInline(admin.TabularInline):
    model = InventoryMovement
    extra = 0
    readonly_fields = ('moved_at', 'moved_by', 'previous_location')
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False

class InventoryMovementAdmin(admin.ModelAdmin):
    list_display = ('inventory', 'movement_type', 'responsible_person', 'previous_location', 'current_location', 'moved_by', 'moved_at', 'expected_return_date')
    list_filter = ('movement_type', 'moved_by', 'moved_at', 'current_location', 'previous_location')
    search_fields = ('inventory__name', 'previous_location', 'current_location', 'notes', 'responsible_person', 'contact_info')
    readonly_fields = ('moved_at', 'moved_by', 'previous_location')
    date_hierarchy = 'moved_at'
    ordering = ('-moved_at',)
    
    fields = ('inventory', 'movement_type', 'responsible_person', 'contact_info', 
              'previous_location', 'current_location', 'moved_at', 'expected_return_date',
              'moved_by', 'notes')

class InventoryAdmin(InventoryAdmin):
    inlines = [InventoryMovementInline]

    def save_model(self, request, obj, form, change):
        if change and 'location' in form.changed_data:
            InventoryMovement.objects.create(
                inventory=obj,
                previous_location=Inventory.objects.get(pk=obj.pk).location,
                current_location=obj.location,
                moved_by=request.user
            )
        super().save_model(request, obj, form, change)

admin.site.register(AccessLog, AccessLogAdmin)

class InventoryHistoryAdmin(admin.ModelAdmin):
    list_display = ('inventory', 'action_display', 'user', 'responsible_person', 'location_changes', 'created_at')
    list_filter = ('action', 'user', 'created_at')
    search_fields = ('inventory__name', 'notes', 'responsible_person')
    readonly_fields = ('created_at', 'user')
    
    def action_display(self, obj):
        return obj.get_action_display()
    action_display.short_description = 'Ação'
    
    def location_changes(self, obj):
        if obj.old_location and obj.new_location:
            return f"{obj.old_location} → {obj.new_location}"
        return "-"
    location_changes.short_description = 'Mudança de Local'

admin.site.register(InventoryHistory, InventoryHistoryAdmin)
admin.site.register(InventoryMovement, InventoryMovementAdmin)
