from rest_framework.views import APIView
from rest_framework.response import Response
from .models import (Animal)
from .serializers import (AnimalSerializer, RegisterSerializer, LoginSerializer)
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token


class AnimalDetailView(APIView):
    def get(self, request, pk):
        try:
            queryset = Animal.objects.get(pk = pk)
            queryset.IncrementViews()
            serializer = AnimalSerializer(queryset)
            return Response({'status':True, 
                            'message': 'Animal fetched with GET',
                            'data': serializer.data,
                             })
        except Exception as e:
            print(e)
            return Response({'status':False, 
                            'message': 'Somthing went wrong',
                            'data': {},
                             })




class AnimalView(APIView):

    def get(self, request):
        queryset = Animal.objects.all()
        if request.GET.get('search'):
            search = request.GET.get('search')
            queryset = queryset.filter(Q(animal_name__icontains = search) | 
                                       Q(animal_description__icontains = search) |
                                       Q(animal_gender__iexact = search) |                         #iexact exact word ko filter kar k dega
                                       Q(animal_breed__animal_breed__icontains = search) | 
                                       Q(animal_color__animal_color__icontains = search))
        serializer = AnimalSerializer(queryset, many=True)  # jab bahut sare queryset ho tab many = True likhenge
        return Response({'status':True, 
                        'message': 'Animal fetched with GET',
                         'data': serializer.data,
                         })

    def post(self, request):
        return Response({'status':True, 'message': 'Animal fetched with POST',})

    def put(self, request):
        return Response({'status':True, 'message': 'Animal fetched with PUT',})

    def patch(self, request):
        return Response({'status':True, 'message': 'Animal fetched with Patch',})


#   <--- Register User --->

class RegisterAPI(APIView):
    def post(self, request):
        try:
            data = request.data        # ye hame sara data nikal k dega
            serializer = RegisterSerializer(data=data)

            if serializer.is_valid():
                user = User.objects.create(username = serializer.data['username'],email = serializer.data['email'])
                user.set_password(serializer.data['password'])
                user.save()
                return Response({
                    'status': True,
                    'message': "account created",
                    'data': {}
                })
            
            return Response({
                    'status': False,
                    'message': "keys errors",
                    'data': serializer.errors
                })
        except Exception as e:
            print(e)


#   <--- Login User --->

class LoginAPI(APIView):
    def post(self, request):
        try:
            data = request.data        # ye hame sara data nikal k dega
            serializer = LoginSerializer(data=data)

            if serializer.is_valid():
                user = authenticate(username = serializer.data['username'], password = serializer.data['password'])
                if user:
                    token ,_= Token.objects.get_or_create(user=user)
                    return Response({
                        'status': True,
                        'message': "Login successfull",
                        'data': {'token': str(token)}
                    })
                return Response({
                    'status': False,
                    'message': "invalid password",
                    'data': {}
                    })
            return Response({
                    'status': False,
                    'message': "keys errors",
                    'data': serializer.errors
                })
        except Exception as e:
            print(e)
            return Response({
                    'status': False,
                    'message': "Somthing went wrong",
                    'data': {}
                })
