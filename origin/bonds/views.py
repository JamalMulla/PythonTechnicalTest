import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import generics
from django.contrib.auth.models import User
from bonds.permissions import IsOwner
from django.contrib.auth.models import AnonymousUser


from .serializers import BondSerializer, UserSerializer
from .models import Bond


class BondView(APIView):
    permission_classes = [IsOwner]

    def get(self, request):
        if self.request.user == AnonymousUser():
            return JsonResponse({"Error": "Must be authenticated"}, status=401)
        # Filter on user
        bonds = Bond.objects.filter(owner=request.user.id)

        # Filter on query paramters

        size = self.request.query_params.get('size', None)
        if size is not None:
            bonds = bonds.filter(size=size)

        currency = self.request.query_params.get('currency', None)
        if currency is not None:
            bonds = bonds.filter(currency=currency)

        maturity = self.request.query_params.get('maturity', None)
        if maturity is not None:
            bonds = bonds.filter(maturity=maturity)

        lei = self.request.query_params.get('lei', None)
        if lei is not None:
            bonds = bonds.filter(lei=lei)

        legal_name = self.request.query_params.get('legal_name', None)
        if legal_name is not None:
            bonds = bonds.filter(legal_name=legal_name)

        serializer = BondSerializer(bonds, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        if self.request.user == AnonymousUser():
            return JsonResponse({"Error": "Must be authenticated"}, status=401)
        r = requests.get('https://leilookup.gleif.org/api/v2/leirecords?lei=' +
                         request.data['lei'], params=request.GET)
        if r.status_code == 200:
            # get legalname from json response and remove spaces
            request.data['legal_name'] = (
                r.json()[0]['Entity']['LegalName']['$']).replace(" ", "")
            serializer = BondSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(owner=self.request.user)
                return JsonResponse(serializer.data, status=201)
            return JsonResponse(serializer.errors, status=400)
        return JsonResponse({"Error": "Could not get LegalName"}, status=r.status_code)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class HelloWorld(APIView):
    def get(self, request):
        return Response("Hello World!")
