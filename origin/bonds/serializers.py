from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Bond


class BondSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Bond
        fields = ('isin', 'size', 'currency', 'maturity', 'lei', 'legal_name', 'owner')

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username']