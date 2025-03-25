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
        ('available', 'Disponível'),
        ('in_use', 'Em Uso'),
        ('maintenance', 'Em Manutenção'),
        ('reserved', 'Reservado'),
        ('discontinued', 'Descontinuado')
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Baixa'),
        ('medium', 'Média'),
        ('high', 'Alta'),
        ('critical', 'Crítica')
    ]
    
    name = models.CharField(max_length=255, verbose_name='Nome')
    
    def clean(self):
        if self.quantity < 0:
            raise ValidationError({'quantity': 'A quantidade não pode ser negativa.'})
        if self.minimum_quantity < 0:
            raise ValidationError({'minimum_quantity': 'A quantidade mínima não pode ser negativa.'})
        if self.unit_price and self.unit_price < Decimal('0.00'):
            raise ValidationError({'unit_price': 'O preço unitário não pode ser negativo.'})
        if self.warranty_expiration and self.warranty_expiration < timezone.now().date():
            raise ValidationError({'warranty_expiration': 'A data de vencimento da garantia não pode estar no passado.'})
            
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
        if not self.barcode:
            self.barcode = f"INV-{self.id if self.id else 0:06d}"
            
        if not self.qr_code:
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(self.barcode)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            
            buffer = BytesIO()
            img.save(buffer, format='PNG')
            filename = f'qr_{self.barcode}.png'
            
            self.qr_code.save(filename, File(buffer), save=False)
            
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
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name='history')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=50)
    old_status = models.CharField(max_length=50, blank=True, null=True)
    new_status = models.CharField(max_length=50, blank=True, null=True)
    old_quantity = models.IntegerField(null=True)
    new_quantity = models.IntegerField(null=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Histórico de Inventário"
        verbose_name_plural = "Históricos de Inventário"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.inventory.name} - {self.action} - {self.created_at}"
