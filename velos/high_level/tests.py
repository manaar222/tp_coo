# Create your tests here.
from django.test import TestCase
from .models import Machine
class MachineModelTests(TestCase):
def test_machine_creation(self):
self.assertEqual(Machine.objects.count(), 0)
Machine.objects.create(nom="CNC", prix=28_000, duree_de_vie = 12, cout_maintenance = 850, superficie = 9)
self.assertEqual(Machine.objects.count(), 1)
