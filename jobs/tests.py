
from django.test import TestCase
from .models import Job

class JobTestCase(TestCase):
    def setUp(self):
        Job.objects.create(
            nome_job="Teste Job",
            stream_job="Stream Teste",
            estacao_trabalho="Estação 1",
            criticidade="Alta"
        )
    
    def test_criacao_job(self):
        """Testa a criação básica de um job"""
        job = Job.objects.get(nome_job="Teste Job")
        self.assertEqual(job.criticidade, "Alta")
        self.assertEqual(job.estacao_trabalho, "Estação 1")

    def test_str_job(self):
        """Testa a representação string do job"""
        job = Job.objects.get(nome_job="Teste Job")
        self.assertEqual(str(job), "Teste Job")
