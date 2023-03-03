from django.shortcuts import render
from rest_framework.views import APIView, Response, status
from .models import Pet
from rest_framework.pagination import PageNumberPagination
from .serializers import PetSerializer
from traits.models import Trait
from groups.models import Group
from django.shortcuts import get_object_or_404

# Create your views here.
class PetView(APIView, PageNumberPagination):
    def get(self, request):
        pets = Pet.objects.all()

        traits = request.query_params.get("trait", None)

        if traits:
            trait = Trait.objects.filter(name=traits).first()
            print(trait)
            if trait:
                pets = Pet.objects.filter(traits=trait).all()

        pets_page = self.paginate_queryset(pets, request)

        serializer = PetSerializer(pets_page, many=True)

        return self.get_paginated_response(serializer.data)

    def post(self, request):

        serializer = PetSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        group_dict = serializer.validated_data.pop("group")

        traits = serializer.validated_data.pop("traits")

        group_find = Group.objects.filter(scientific_name__iexact=group_dict["scientific_name"]).first()

        if not group_find:
            group_find = Group.objects.create(**group_dict)

        pet = Pet.objects.create(**serializer.validated_data, group=group_find)

        for trait in traits:
            trait_find = Trait.objects.filter(
                name__iexact=trait["name"]
            ).first()

            if not trait_find:
                trait_find = Trait.objects.create(**trait)

            pet.traits.add(trait_find)

        # Formatando o objeto para saída
        serializer = PetSerializer(pet)

        return Response(serializer.data, status.HTTP_201_CREATED)
    

class PetDetailView(APIView, PageNumberPagination):
    def get(self, request, pet_id):
        pet = get_object_or_404(Pet, id=pet_id)

        serializer = PetSerializer(pet)

        return Response(serializer.data)

    
    def delete(self, request, pet_id):
        pet = get_object_or_404(Pet, id=pet_id)

        pet.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    
    def patch(self, request, pet_id):
        pet = get_object_or_404(Pet, id=pet_id)

        page = request.query_params.get("page", None)

        serializer = PetSerializer(data=request.data, partial=True)

        serializer.is_valid(raise_exception=True)

        group_dict = serializer.validated_data.pop("group", None)

        traits = serializer.validated_data.pop("traits", None)

        if group_dict:
            group_find = Group.objects.filter(scientific_name__iexact=group_dict["scientific_name"]).first()

            if not group_find:
                group_find = Group.objects.create(**group_dict)
            pet.group = group_find

        traits_list = []

        if traits:
            for trait in traits:
                trait_find = Trait.objects.filter(
                    name__iexact=trait["name"]
                ).first()

                if not trait_find:
                    trait_find = Trait.objects.create(**trait)

                traits_list.append(trait_find)


        pet.traits.set(traits_list)

        for key, value in serializer.validated_data.items():
            setattr(pet, key, value)

        pet.save()

        serializer = PetSerializer(pet)

        return Response(serializer.data)


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 2
    page_query_param = 'page'