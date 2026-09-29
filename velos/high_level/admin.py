# Register your models here.
from django.contrib import admin 

from .models import (
	Pays,
	Ville,
	Machine,
	Lieu,
	Transport,
	Operation,
	Produit,
	PrixProduit,
	Fournisseur,
	QuantiteProduit,
	Stock,
	PointDeVente,
	QuantiteMachine,
	Facture,
)
admin.site.register(Pays)
admin.site.register(Ville)
admin.site.register(Machine)
admin.site.register(QuantiteMachine)
admin.site.register(Lieu)
admin.site.register(Transport)
admin.site.register(Operation)
admin.site.register(Produit)
admin.site.register(PrixProduit)
admin.site.register(Fournisseur)
admin.site.register(QuantiteProduit)
admin.site.register(Stock)
admin.site.register(PointDeVente)
admin.site.register(Facture)
	

