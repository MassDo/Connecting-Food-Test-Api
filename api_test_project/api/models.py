from django.db import models


class Farmer(models.Model):
    nom = models.CharField(max_length=50)
    numero_siret = models.IntegerField() # 14 chiffres (9 siren + 5 NIC)
    adresse = models.CharField(max_length=500)

    def __str__(self):
        return self.nom

class Product(models.Model):
    nom = models.CharField(max_length=50)
    unite = models.CharField(max_length=50)
    codification_internationnale = models.CharField(max_length=50)
    producteurs = models.ManyToManyField(Farmer)

    def __str__(self):
        return f'{self.nom} ({", ".join(p.nom for p in self.producteurs.all())})' # a optimiser avec prefetch_related

class Certificate(models.Model):
    TYPE_CHOICES = [
        ('biologique', 'biologique'),
        ('sans ogm', 'sans ogm'),
        ('origine', 'origine'),
    ]
    nom = models.CharField(max_length=50)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES) # biologique, sans ogm, origine
    farmer_certifie = models.ForeignKey(Farmer, on_delete=models.CASCADE) # suppression de l'enregistrement certificat si le farmer associé est supprimé

    def __str__(self):
        return self.nom
