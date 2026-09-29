# Create your models here.
from django.db import models 


class Pays (models.Model):
	nom = models.CharField(max_length=100)
	tva = models.FloatField()
	tarif_electrique = models.FloatField()
	salaire_minimum = models.FloatField()




class Ville (models.Model):
	nom = models.CharField(max_length=100)
	taxe_immobiliere = models.FloatField()
	prix_m2 = models.FloatField()
	pays = models.ForeignKey(
	Pays,
	on_delete=models.PROTECT,
	)





class Machine (models.Model):
	nom = models.CharField(max_length=100)
	prix = models.FloatField()
	duree_de_vie = models.FloatField()
	cout_maintenance = models.FloatField()
	superficie = models.FloatField()



class QuantiteMachine (models.Model):
	machine = models.ForeignKey(
	Machine,
	on_delete=models.PROTECT,
	)
	nombre = models.IntegerField()


class Lieu (models.Model):
	nom = models.CharField(max_length=100)
	ville = models.ForeignKey(
	Ville,
	on_delete=models.PROTECT,
	)
	superficie = models.FloatField()
	quantite_machines = models.ForeignKey(
	QuantiteMachine,
	on_delete=models.PROTECT,
	)
	consommation_electrique = models.FloatField()


class Transport (models.Model):
	nombre_palettes = models.IntegerField()
	cout = models.FloatField()
	delai = models.IntegerField()
	depart = models.ForeignKey(
	Lieu,
	on_delete=models.PROTECT,
	related_name="transport_depart",
	)
	arrivee = models.ForeignKey(
	Lieu,
	on_delete=models.PROTECT,
	related_name="transport_arivee",
	)



class Operation (models.Model):
	nom = models.CharField(max_length=100)
	operation_suivante = models.ForeignKey(
	"self",
	on_delete=models.PROTECT,
	null=True,
	blank=True,
	)
	cout = models.FloatField()
	machine = models.ForeignKey(
	Machine,
	on_delete=models.PROTECT,
	)
	heures_de_travail = models.IntegerField()
	consommation_electrique = models.FloatField()
	quantite_produits = models.ForeignKey(
	"QuantiteProduit",
	on_delete=models.PROTECT,
	blank=True,
	null=True,
	)

class QuantiteProduit (models.Model):
	nombre = models.IntegerField()
	matiere_premiere = models.ForeignKey(
	"Produit",
	on_delete=models.PROTECT,
	)
	
class Produit (models.Model):
	nom = models.CharField(max_length=100)
	prix_de_vente = models.FloatField()
	duree_de_vie = models.IntegerField()
	nombre_par_palette = models.IntegerField()
	operations = models.ManyToManyField(Operation)
	
class PrixProduit (models.Model):
	produit = models.ForeignKey(
	Produit,
	on_delete=models.PROTECT,
	)	
	prix_achat = models.FloatField()

class Fournisseur (models.Model):
	nom = models.CharField(max_length=100)
	prix_produits = models.ForeignKey(
	PrixProduit,
	on_delete=models.PROTECT,
	)


class Stock (models.Model):
	quantite_produits = models.ManyToManyField(QuantiteProduit)
	palettes_max = models.IntegerField()



class PointDeVente (models.Model):
	nom = models.CharField(max_length=100)
	lieu = models.ForeignKey(
	Lieu,
	on_delete=models.PROTECT,
	)
	heures_de_travail = models.IntegerField()
	stock = models.ForeignKey(
	Stock,
	on_delete=models.PROTECT,
	)


class Facture (models.Model):
	quantite_produits = models.ForeignKey(
	QuantiteProduit,
	on_delete=models.PROTECT,
	)
	reduction = models.FloatField()
	point_de_vente = models.ForeignKey(
	PointDeVente,
	on_delete=models.PROTECT,
	)
	client = models.CharField(max_length=100) 

