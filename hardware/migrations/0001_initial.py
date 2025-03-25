# Generated by Django 5.1.7 on 2025-03-25 03:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AccessLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Hardware',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marca', models.CharField(blank=True, max_length=255)),
                ('modelo', models.CharField(blank=True, max_length=255)),
                ('serial_number', models.CharField(blank=True, max_length=255)),
                ('descricao', models.CharField(blank=True, default='unknown', max_length=255)),
                ('local', models.CharField(blank=True, default='unknown', max_length=255)),
                ('fornecedor_manut', models.CharField(blank=True, default='unknown', max_length=255)),
                ('data_inicial_manut', models.DateField(blank=True, null=True)),
                ('data_final_manut', models.DateField(blank=True, null=True)),
                ('meses_contratados', models.CharField(blank=True, default='unknown', max_length=255)),
                ('dias_para_termino', models.IntegerField(blank=True, default=0, null=True)),
                ('status_contrato', models.CharField(blank=True, default='unknown', max_length=255)),
                ('brand', models.CharField(blank=True, default='unknown', max_length=255)),
                ('end_datacenter', models.CharField(blank=True, default='unknown', max_length=255)),
                ('rack', models.CharField(blank=True, default='unknown', max_length=255, null=True)),
                ('storage', models.CharField(blank=True, default='unknown', max_length=255, null=True)),
                ('ip', models.CharField(blank=True, default='unknown', max_length=255)),
                ('alerta', models.CharField(blank=True, default='unknown', max_length=255)),
            ],
            options={
                'verbose_name': 'Hardware',
                'verbose_name_plural': 'Hardwares',
            },
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Nome')),
                ('description', models.TextField(blank=True, verbose_name='Descrição')),
                ('quantity', models.IntegerField(default=0, verbose_name='Quantidade')),
                ('minimum_quantity', models.IntegerField(default=1, verbose_name='Quantidade Mínima')),
                ('unit_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Preço Unitário')),
                ('image', models.ImageField(blank=True, null=True, upload_to='inventory_images/', verbose_name='Imagem')),
                ('category', models.CharField(blank=True, max_length=100, verbose_name='Categoria')),
                ('location', models.CharField(blank=True, max_length=255, verbose_name='Localização')),
                ('status', models.CharField(choices=[('available', 'Disponível'), ('in_use', 'Em Uso'), ('maintenance', 'Em Manutenção'), ('reserved', 'Reservado'), ('discontinued', 'Descontinuado')], default='available', max_length=50, verbose_name='Status')),
                ('supplier', models.CharField(blank=True, max_length=255, verbose_name='Fornecedor')),
                ('notes', models.TextField(blank=True, verbose_name='Observações')),
                ('warranty_expiration', models.DateField(blank=True, null=True, verbose_name='Vencimento da Garantia')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
                ('barcode', models.CharField(blank=True, max_length=100, null=True, unique=True, verbose_name='Código de Barras')),
                ('qr_code', models.ImageField(blank=True, null=True, upload_to='qrcodes/', verbose_name='QR Code')),
                ('maintenance_interval', models.IntegerField(default=180, verbose_name='Intervalo de Manutenção (dias)')),
                ('last_maintenance', models.DateField(blank=True, null=True, verbose_name='Última Manutenção')),
                ('next_maintenance', models.DateField(blank=True, null=True, verbose_name='Próxima Manutenção')),
                ('priority', models.CharField(choices=[('low', 'Baixa'), ('medium', 'Média'), ('high', 'Alta'), ('critical', 'Crítica')], default='low', max_length=20, verbose_name='Prioridade')),
            ],
            options={
                'verbose_name': 'Inventory',
                'verbose_name_plural': 'Inventories',
            },
        ),
        migrations.CreateModel(
            name='InventoryHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(max_length=50)),
                ('old_status', models.CharField(blank=True, max_length=50, null=True)),
                ('new_status', models.CharField(blank=True, max_length=50, null=True)),
                ('old_quantity', models.IntegerField(null=True)),
                ('new_quantity', models.IntegerField(null=True)),
                ('notes', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('inventory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history', to='hardware.inventory')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Histórico de Inventário',
                'verbose_name_plural': 'Históricos de Inventário',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='InventoryMovement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movement_type', models.CharField(choices=[('transfer', 'Transferência'), ('loan', 'Empréstimo'), ('maintenance', 'Manutenção'), ('return', 'Devolução')], default='transfer', max_length=20, verbose_name='Tipo de Movimentação')),
                ('previous_location', models.CharField(max_length=255, verbose_name='Localização Anterior')),
                ('current_location', models.CharField(max_length=255, verbose_name='Nova Localização')),
                ('moved_at', models.DateTimeField(auto_now_add=True, verbose_name='Data da Movimentação')),
                ('expected_return_date', models.DateField(blank=True, null=True, verbose_name='Data Prevista de Retorno')),
                ('responsible_person', models.CharField(max_length=255, verbose_name='Pessoa Responsável')),
                ('contact_info', models.CharField(blank=True, max_length=255, verbose_name='Informação de Contato')),
                ('notes', models.TextField(blank=True, verbose_name='Observações')),
                ('inventory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='movements', to='hardware.inventory', verbose_name='Item')),
                ('moved_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Movido por')),
            ],
            options={
                'verbose_name': 'Movimentação de Inventário',
                'verbose_name_plural': 'Movimentações de Inventário',
                'ordering': ['-moved_at'],
            },
        ),
    ]
