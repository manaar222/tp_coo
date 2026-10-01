"""
URL configuration for velos project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path

from high_level.views import (
    PaysDetailView,
    VilleDetailView,
    MachineDetailView,
    QuantiteMachineDetailView,
    LieuDetailView,
    TransportDetailView,
    OperationDetailView,
    QuantiteProduitDetailView,
    ProduitDetailView,
    PrixProduitDetailView,
    FournisseurDetailView,
    StockDetailView,
    PointDeVenteDetailView,
    FactureDetailView,
)
urlpatterns = [
    path("admin/", admin.site.urls),
    
    path("pays/<int:pk>/", PaysDetailView.as_view()),
    path("ville/<int:pk>/", VilleDetailView.as_view()),
    path("machine/<int:pk>/", MachineDetailView.as_view()),
    path("quantiteMachine/<int:pk>/", QuantiteMachineDetailView.as_view()),
    path("lieu/<int:pk>/", LieuDetailView.as_view()),
    path("transport/<int:pk>/", TransportDetailView.as_view()),
    path("operation/<int:pk>/", OperationDetailView.as_view()),
    path("quantiteProduit/<int:pk>/", QuantiteProduitDetailView.as_view()),
    path("produit/<int:pk>/", ProduitDetailView.as_view()),
    path("prixProduit/<int:pk>/", PrixProduitDetailView.as_view()),
    path("fournisseur/<int:pk>/", FournisseurDetailView.as_view()),
    path("stock/<int:pk>/", StockDetailView.as_view()),
    path("pointDeVente/<int:pk>/", PointDeVenteDetailView.as_view()),
    path("facture/<int:pk>/", FactureDetailView.as_view()),
]
