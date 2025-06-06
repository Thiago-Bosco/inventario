from django.db import models


class Hardware(models.Model):
    marca = models.CharField(max_length=255, blank=True)
    modelo = models.CharField(max_length=255, blank=True)
    serial_number = models.CharField(max_length=255, blank=True) 
    descricao = models.CharField(max_length=255, default='unknown', blank=True)
    local = models.CharField(max_length=255, default='unknown', blank=True)
    fornecedor_manut = models.CharField(max_length=255, default='unknown', blank=True)
    data_inicial_manut = models.DateField(null=True, blank=True) 
    data_final_manut = models.DateField(null=True, blank=True)  
    meses_contratados = models.CharField(max_length=255, default='unknown', blank=True)
    dias_para_termino = models.IntegerField(default=0, null=True, blank=True)  
    status_contrato = models.CharField(max_length=255, default='unknown', blank=True)
    brand = models.CharField(max_length=255, default='unknown', blank=True)
    end_datacenter = models.CharField(max_length=255, default='unknown', blank=True)
    rack = models.CharField(max_length=255, default='unknown', blank=True, null=True)
    storage = models.CharField(max_length=255, default='unknown', blank=True, null=True)
    ip = models.CharField(max_length=255, default='unknown', blank=True)
    alerta = models.CharField(max_length=255, default='unknown', blank=True)

    def __str__(self):
        return self.modelo or "Modelo não definido"  

    class Meta:
        verbose_name = "Hardware"
        verbose_name_plural = "Hardwares"




from django.core.exceptions import ValidationError
from django.utils import timezone
from decimal import Decimal

from django.contrib.auth.models import User
import qrcode
from io import BytesIO
from django.core.files import File

class Inventory(models.Model):
    STATUS_CHOICES = [
        ('disponivel', 'Disponível'),
        ('em_uso', 'Em Uso'),
        ('manutencao', 'Em Manutenção'),
        ('reservado', 'Reservado'),
        ('descontinuado', 'Descontinuado'),
        ('pendente', 'Pendente')
    ]
    
    PRIORITY_CHOICES = [
        ('baixa', 'Baixa'),
        ('media', 'Média'),
        ('alta', 'Alta'),
        ('critica', 'Crítica')
    ]
    
    name = models.CharField(max_length=255, verbose_name='Nome')
    
    def clean(self):
        # Validações de quantidade
        if self.quantity < 0:
            raise ValidationError({'quantity': 'A quantidade não pode ser negativa.'})
        if self.minimum_quantity < 0:
            raise ValidationError({'minimum_quantity': 'A quantidade mínima não pode ser negativa.'})
        if self.minimum_quantity > self.quantity:
            raise ValidationError({'minimum_quantity': 'A quantidade mínima não pode ser maior que a quantidade atual.'})

        # Validações de preço
        if self.unit_price and self.unit_price < Decimal('0.00'):
            raise ValidationError({'unit_price': 'O preço unitário não pode ser negativo.'})
            
        # Validações de datas
        if self.warranty_expiration and self.warranty_expiration < timezone.now().date():
            raise ValidationError({'warranty_expiration': 'A data de vencimento da garantia não pode estar no passado.'})
            
        # Validações de manutenção
        if self.last_maintenance and self.next_maintenance:
            if self.last_maintenance > self.next_maintenance:
                raise ValidationError({'next_maintenance': 'A próxima manutenção deve ser depois da última manutenção.'})
            
        if self.next_maintenance and self.next_maintenance < timezone.now().date():
            raise ValidationError({'next_maintenance': 'A data da próxima manutenção não pode estar no passado.'})
            
        # Validação de código de barras
        if self.barcode and not self.barcode.startswith('INV-'):
            raise ValidationError({'barcode': 'O código de barras deve começar com "INV-"'})
            
    def get_total_value(self):
        if self.quantity and self.unit_price:
            return self.quantity * self.unit_price
        return Decimal('0.00')
        
    def is_low_stock(self):
        return self.quantity <= self.minimum_quantity
    description = models.TextField(blank=True, verbose_name='Descrição')
    quantity = models.IntegerField(default=0, verbose_name='Quantidade')
    minimum_quantity = models.IntegerField(default=1, verbose_name='Quantidade Mínima')
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Preço Unitário')
    image = models.ImageField(upload_to='inventory_images/', blank=True, null=True, verbose_name='Imagem')
    category = models.CharField(max_length=100, blank=True, verbose_name='Categoria')
    location = models.CharField(max_length=255, blank=True, verbose_name='Localização')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='available', verbose_name='Status')
    supplier = models.CharField(max_length=255, blank=True, verbose_name='Fornecedor')
    notes = models.TextField(blank=True, verbose_name='Observações')
    warranty_expiration = models.DateField(null=True, blank=True, verbose_name='Vencimento da Garantia')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')
    barcode = models.CharField(max_length=100, unique=True, blank=True, null=True, verbose_name='Código de Barras')
    qr_code = models.ImageField(upload_to='qrcodes/', blank=True, null=True, verbose_name='QR Code')
    maintenance_interval = models.IntegerField(default=180, verbose_name='Intervalo de Manutenção (dias)')
    last_maintenance = models.DateField(null=True, blank=True, verbose_name='Última Manutenção')
    next_maintenance = models.DateField(null=True, blank=True, verbose_name='Próxima Manutenção')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='low', verbose_name='Prioridade')
    
    def save(self, *args, **kwargs):
        # Gerar código de barras se não existir
        if not self.barcode:
            self.barcode = f"INV-{self.id if self.id else 0:06d}"
        
        # Calcular próxima manutenção se necessário
        if self.last_maintenance and not self.next_maintenance and self.maintenance_interval:
            self.next_maintenance = self.last_maintenance + timezone.timedelta(days=self.maintenance_interval)
            
        # Gerar QR code se não existir
        if not self.qr_code:
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(self.barcode)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            
            buffer = BytesIO()
            img.save(buffer, format='PNG')
            filename = f'qr_{self.barcode}.png'
            
            self.qr_code.save(filename, File(buffer), save=False)
        
        # Validar dados antes de salvar    
        self.full_clean()
            
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Inventory"
        verbose_name_plural = "Inventories"



class AccessLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user} - {self.timestamp}"
class InventoryHistory(models.Model):
    ACTION_CHOICES = [
        ('criado', 'Criado'),
        ('atualizado', 'Atualizado'),
        ('movido', 'Movido'),
        ('manutencao', 'Em Manutenção'),
        ('retornado', 'Retornado'),
        ('deletado', 'Deletado')
    ]
    
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name='history')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    old_status = models.CharField(max_length=50, blank=True, null=True)
    new_status = models.CharField(max_length=50, blank=True, null=True)
    old_quantity = models.IntegerField(null=True)
    new_quantity = models.IntegerField(null=True)
    old_location = models.CharField(max_length=255, blank=True, null=True)
    new_location = models.CharField(max_length=255, blank=True, null=True)
    responsible_person = models.CharField(max_length=255, blank=True)
    document_reference = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    details = models.JSONField(default=dict, blank=True)

    class Meta:
        verbose_name = "Histórico de Inventário"
        verbose_name_plural = "Históricos de Inventário"
        ordering = ['-created_at']

    def clean(self):
        if self.action == 'movido' and not (self.old_location and self.new_location):
            raise ValidationError('Localizações antiga e nova são necessárias para movimentação')
        if self.action == 'atualizado' and not (self.old_quantity is not None and self.new_quantity is not None):
            raise ValidationError('Quantidades antiga e nova são necessárias para atualização')
        if self.new_location and len(self.new_location) > 255:
            raise ValidationError('A localização não pode ter mais que 255 caracteres')
        if self.new_quantity is not None and self.new_quantity < 0:
            raise ValidationError('A nova quantidade não pode ser negativa')
        if not self.responsible_person and self.action in ['movido', 'manutencao']:
            raise ValidationError('É necessário informar um responsável para esta ação')
        if self.action == 'manutencao' and not self.notes:
            raise ValidationError('É necessário incluir observações para manutenção')
            
    def get_change_description(self):
        if self.action == 'moved':
            return f"Movido de {self.old_location} para {self.new_location}"
        elif self.action == 'updated':
            return f"Quantidade alterada de {self.old_quantity} para {self.new_quantity}"
        return self.get_action_display()
            
    def __str__(self):
        return f"{self.inventory.name} - {self.action} - {self.created_at}"
