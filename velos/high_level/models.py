# Create your models here.
from django.db import models 


class Pays (models.Model):
	nom = models.CharField(max_length=100)
	tva = models.FloatField()
	tarif_electrique = models.FloatField()
	salaire_minimum = models.FloatField()

	def __str__(self):
		return self.nom
	def json(self):
		return{
		"id" : self.id,
		"nom" : self.nom, 
		"tva" : self.tva,
		"tarif_electrique" : self.tarif_electrique,
		"salaire_minimum" : self.salaire_minimum,
	}
	
	def json_extended(self):
    		return self.json()

class Ville (models.Model):
	nom = models.CharField(max_length=100)
	taxe_immobiliere = models.FloatField()
	prix_m2 = models.FloatField()
	pays = models.ForeignKey(
	Pays,
	on_delete=models.PROTECT,
	)
	
	def __str__(self):
		return self.nom
	def json(self):
		return{
		"nom" : self.nom,
		"taxe_immobiliere" : self.taxe_immobiliere, 
		"prix_m2" : self.prix_m2,
		"pays" : self.pays.pk,
	}

	def json_extended(self):
    		return{
        	"nom": self.nom,
        	"taxe_immobiliere": self.taxe_immobiliere,
        	"prix_m2": self.prix_m2,
        	"pays": self.pays.json(),
    }
class Machine (models.Model):
	nom = models.CharField(max_length=100)
	prix = models.FloatField()
	duree_de_vie = models.FloatField()
	cout_maintenance = models.FloatField()
	superficie = models.FloatField()

	def __str__(self):
		return self.nom
	def costs(self):
		return self.prix
	def json(self):
		return{
		"nom" : self.nom,
		"prix" : self.prix, 
		"duree_de_vie" : self.duree_de_vie,
		"cout_maintenance" : self.cout_maintenance,
		"superficie" : self.superficie,
	}
	def json_extended(self):
   	 return self.json()
		

class QuantiteMachine (models.Model):
	machine = models.ForeignKey(
	Machine,
	on_delete=models.PROTECT,
	)
	nombre = models.IntegerField()

	def __str__(self):
		return str(self.nombre)
	def costs(self):
		return self.nombre * self.machine.costs()
	def json(self):
		return{
		"machine" : self.machine.pk,
		"nombre" : self.nombre, 
	}
	def json_extended(self):
   		return {
        "machine": self.machine.json(),
        "nombre": self.nombre,
    }	

class Lieu (models.Model):
	nom = models.CharField(max_length=100)
	ville = models.ForeignKey(
	Ville,
	on_delete=models.PROTECT,
	)
	superficie = models.FloatField()
	quantite_machines = models.ManyToManyField(QuantiteMachine)
	consommation_electrique = models.FloatField()
	def __str__(self):
		return str(self.nom)
	def costs(self):
		couts = self.superficie * self.ville.prix_m2 + self.consommation_electrique * self.ville.pays.tarif_electrique 
		couts += sum( 
			quantite_machines.costs()
			for quantite_machines in self.quantite_machines.all())
		couts += sum( 
			PointDeVente.stock.costs()
			for PointDeVente in self.pointdevente_set.all())
		return couts
	def json(self):
		return{
		"nom" : self.nom,
		"ville" : self.ville.pk, 
		"superficie" : self.superficie,
		"quantite_machines" : [
			quantiteMachine.pk
			for quantiteMachine in self.quantite_machines.all()
		],
		"consommation_electrique" : self.consommation_electrique,
	}
	def json_extended(self):
    		return {
        	"nom": self.nom,
        	"ville": self.ville.json(),
        	"superficie": self.superficie,
        	"quantite_machines": [
           	 quantite_machine.json()
           	 for quantite_machine in self.quantite_machines.all()
        	],
        	"consommation_electrique": self.consommation_electrique,
   	 }

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
	def costs(self):
		return self.cout
	def json(self):
		return{
		"nombre_palettes" : self.nombre_palettes,
		"cout" : self.cout, 
		"delai" : self.delai,
		"depart" : self.depart.pk,
		"arrivee" : self.arrivee.pk,
	}
	def json_extended(self):
		return{
		"nombre_palettes" : self.nombre_palettes,
		"cout" : self.cout, 
		"delai" : self.delai,
		"depart" : self.depart.json(),
		"arrivee" : self.arrivee.json(),
	}


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
	
	def __str__(self):
		return self.nom
	def costs(self):
		return self.cout+self.heures_de_travail*self.pays.salaire_minimum+self.consommation_electrique*self.pays.tarif_electrique
	def json(self):
		return{
		"nom" : self.nom,
		"operation_suivante": (
    		self.operation_suivante.pk
    		if self.operation_suivante
    		else None
		), 
		"cout" : self.cout,
		"machine" : self.machine.pk,
		"heures_de_travail" : self.heures_de_travail,
		"consommation_electrique" : self.consommation_electrique,
		"quantite_produits": (
    		self.quantite_produits.pk
    		if self.quantite_produits
    		else None
		),
	}
	def json_extended(self):
		return{
		"nom" : self.nom,
		"operation_suivante" : (
            self.operation_suivante.json()
            if self.operation_suivante
            else None
        ),
		"cout" : self.cout,
		"machine" : self.machine.json(),
		"heures_de_travail" : self.heures_de_travail,
		"consommation_electrique" : self.consommation_electrique,
		"quantite_produits": (
			self.quantite_produits.json() 
			if self.quantite_produits 
			else None,
		),
	}
	
	
class QuantiteProduit (models.Model):
	nombre = models.IntegerField()
	matiere_premiere = models.ForeignKey(
	"Produit",
	on_delete=models.PROTECT,
	)
	
	def __str__(self):
		return str(self.nombre)
	def costs(self):
		return (self.nombre * self.matiere_premiere.costs())
	def json(self):
		return{
		"nombre" : self.nombre,
		"matiere_premiere" : self.matiere_premiere.pk,
	}
	def json_extended(self):
		return{
		"nombre" : self.nombre,
		"matiere_premiere" : self.matiere_premiere.json(),
	}
	
		
class Produit (models.Model):
	nom = models.CharField(max_length=100)
	prix_de_vente = models.FloatField()
	duree_de_vie = models.IntegerField()
	nombre_par_palette = models.IntegerField()
	operations = models.ManyToManyField(Operation)
	
	def __str__(self):
		return self.nom
	def costs(self):
		return self.prix_de_vente
	def json(self):
		return{
		"nom" : self.nom,
		"prix_de_vente" : self.prix_de_vente, 
		"duree_de_vie" : self.duree_de_vie,
		"nombre_par_palette" : self.nombre_par_palette,
		"operations" :[ 
			operation.pk
			for operation in self.operations.all()
		],
	}
	def json_extended(self):
		return{
		"nom" : self.nom,
		"prix_de_vente" : self.prix_de_vente, 
		"duree_de_vie" : self.duree_de_vie,
		"nombre_par_palette" : self.nombre_par_palette,
		"operations" :[ 
			operation.json()
			for operation in self.operations.all()
		],
	}
	
class PrixProduit (models.Model):
	produit = models.ForeignKey(
	Produit,
	on_delete=models.PROTECT,
	)	
	prix_achat = models.FloatField()
	
	def __str__(self):
		return str(self.prix_achat)
	def json(self):
		return{
		"produit" : self.produit.pk,
		"prix_achat" : self.prix_achat, 
	}
	def json_extended(self):
		return{
		"produit" : self.produit.json(),
		"prix_achat" : self.prix_achat, 
	}

class Fournisseur (models.Model):
	nom = models.CharField(max_length=100)
	prix_produits = models.ForeignKey(
	PrixProduit,
	on_delete=models.PROTECT,
	)
	def json(self):
		return{
		"nom" : self.nom,
		"prix_produits" : self.prix_produits.pk, 
	}
	def json_extended(self):
		return{
		"nom" : self.nom,
		"prix_produits" : self.prix_produits.json(), 
	}


class Stock (models.Model):
	quantite_produits = models.ManyToManyField(QuantiteProduit)
	palettes_max = models.IntegerField()
	
	def costs(self):
		return sum( quantite_produits.costs()
		 for quantite_produits in self.quantite_produits.all())
	def json(self):
		return{
		"quantite_produits": [
            		quantite_produit.pk
            		for quantite_produit in self.quantite_produits.all()
        	],
		"palettes_max" : self.palettes_max, 
	}
	def json_extended(self):
		return{
		"quantite_produits": [
            		quantite_produit.json()
            		for quantite_produit in self.quantite_produits.all()
        	],
		"palettes_max" : self.palettes_max, 
	}


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

	def __str__(self):
		return self.nom
	def json(self):
		return{
		"nom" : self.nom,
		"lieu" : self.lieu.pk, 
		"heures_de_travail" : self.heures_de_travail,
		"stock" : self.stock.pk,
	}
	def json_extended(self):
		return{
		"nom" : self.nom,
		"lieu" : self.lieu.json(), 
		"heures_de_travail" : self.heures_de_travail,
		"stock" : self.stock.json(),
	}

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
	def json(self):
		return{
		"quantite_produits" : self.quantite_produits.pk,
		"reduction" : self.reduction, 
		"point_de_vente" : self.point_de_vente.pk,
		"client" : self.client,
	}
	def json_extended(self):
		return{
		"quantite_produits" : self.quantite_produits.json(),
		"reduction" : self.reduction, 
		"point_de_vente" : self.point_de_vente.json(),
		"client" : self.client,
	}
