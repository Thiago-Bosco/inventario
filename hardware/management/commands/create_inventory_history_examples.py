
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from hardware.models import Inventory, InventoryHistory
from django.utils import timezone

class Command(BaseCommand):
    help = 'Creates example inventory history records'

    def handle(self, *args, **kwargs):
        # Ensure we have a test user
        user, created = User.objects.get_or_create(
            username='admin',
            defaults={'is_staff': True, 'is_superuser': True}
        )
        
        # Create a test inventory item if it doesn't exist
        inventory, created = Inventory.objects.get_or_create(
            name='Laptop Dell XPS',
            defaults={
                'quantity': 5,
                'minimum_quantity': 2,
                'category': 'Notebooks',
                'location': 'Almoxarifado'
            }
        )

        # Create example history records
        examples = [
            {
                'action': 'created',
                'new_quantity': 5,
                'new_location': 'Almoxarifado',
                'responsible_person': 'João Silva',
                'notes': 'Registro inicial do equipamento'
            },
            {
                'action': 'moved',
                'old_location': 'Almoxarifado',
                'new_location': 'Setor TI',
                'responsible_person': 'Maria Santos',
                'notes': 'Transferência para setor de TI'
            },
            {
                'action': 'maintenance',
                'old_status': 'in_use',
                'new_status': 'maintenance',
                'responsible_person': 'Carlos Técnico',
                'notes': 'Manutenção preventiva'
            },
            {
                'action': 'updated',
                'old_quantity': 5,
                'new_quantity': 4,
                'responsible_person': 'Ana Costa',
                'notes': 'Atualização de quantidade após empréstimo'
            },
            {
                'action': 'returned',
                'old_status': 'maintenance',
                'new_status': 'available',
                'responsible_person': 'Carlos Técnico',
                'notes': 'Retorno da manutenção'
            }
        ]

        for example in examples:
            InventoryHistory.objects.create(
                inventory=inventory,
                user=user,
                created_at=timezone.now(),
                **example
            )

        self.stdout.write(self.style.SUCCESS('Successfully created inventory history examples'))
