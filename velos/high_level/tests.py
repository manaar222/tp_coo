# Create your tests here.
from django.test import TestCase


from .models import (
    Machine,
    QuantiteMachine,
    Lieu,
    Ville,
    Pays,
    Produit,
    QuantiteProduit,
    Stock,
    PointDeVente,
)


class LieuModelTests(TestCase):

    def test_lieu_costs(self):
        france = Pays.objects.create(
            nom="France",
            tva=20,
            tarif_electrique=0.2,
            salaire_minimum=12,
        )

        ville = Ville.objects.create(
            nom="Labège",
            taxe_immobiliere=0,
            prix_m2=2000,
            pays=france,
        )

        m1 = Machine.objects.create(
            nom="Machine 1",
            prix=10000,
            duree_de_vie=10,
            cout_maintenance=1000,
            superficie=20,
        )

        m2 = Machine.objects.create(
            nom="Machine 2",
            prix=5000,
            duree_de_vie=6,
            cout_maintenance=600,
            superficie=9,
        )

        qm1 = QuantiteMachine.objects.create(
            machine=m1,
            nombre=1,
        )

        qm2 = QuantiteMachine.objects.create(
            machine=m2,
            nombre=1,
        )

        acier = Produit.objects.create(
            nom="Tubes d'acier",
            prix_de_vente=1000,
            duree_de_vie=40,
            nombre_par_palette=1,
        )

        cable = Produit.objects.create(
            nom="Cables",
            prix_de_vente=3000,
            duree_de_vie=20,
            nombre_par_palette=1,
        )

        q_acier = QuantiteProduit.objects.create(
            nombre=2,
            matiere_premiere=acier,
        )

        q_cable = QuantiteProduit.objects.create(
            nombre=1,
            matiere_premiere=cable,
        )

        l1 = Lieu.objects.create(
            nom="TLS-01",
            superficie=50,
            consommation_electrique=5000,
            ville=ville,
        )

        l1.quantite_machines.add(qm1, qm2)

        stock1 = Stock.objects.create(
            palettes_max=10,
        )

        stock1.quantite_produits.add(q_acier, q_cable)

        pdv1 = PointDeVente.objects.create(
            nom="pdv1",
            lieu=l1,
            heures_de_travail=12,
            stock=stock1,
        )

        self.assertEqual(l1.costs(), 121000)
