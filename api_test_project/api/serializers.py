from rest_framework import serializers

from .models import Certificate, Farmer, Product


class FarmerSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Farmer
        fields = ('id','url', 'nom', 'numero_siret', 'adresse')

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'id',
            'url', 
            'nom', 
            'unite', 
            'codification_internationnale', 
            'producteurs'
        )
        # depth = 1 supprime la possibilité d'ajouter un producteurs 
        # permets de voir les attributs des producteurs.(nested)

class CertificateSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        """
            modification du constructeur pour adapter dynamiquement les 
            champs retournés, grace au paramètre fields.
        """
        # Don't pass the 'fields' arg up to the superclass
        request = kwargs.get('context', {}).get('request')
        str_fields = request.GET.get('fields', '') if request else None
        fields = str_fields.split(',') if str_fields else None 
        # Instantiate the superclass normally
        super(CertificateSerializer, self).__init__(*args, **kwargs)
        if fields is not None:
            # Drop any fields that are not specified in the `fields`
            # argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    class Meta:
        model = Certificate
        fields = ('id', 'url', 'nom', 'type', 'farmer_certifie')
