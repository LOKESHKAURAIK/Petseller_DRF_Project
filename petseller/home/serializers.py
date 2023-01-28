from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_name',]

class AnimalBreedSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalBreed
        # fields = '__all__'
        fields = ['animal_breed']


class AnimalImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalImages
        fields = ['animal_images']

class AnimalColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalColor
        # fields = '__all__'
        fields = ['animal_color']


class AnimalSerializer(serializers.ModelSerializer):
    # <---METHOD01:- with the help of serializerMethodField---->

    # animal_category = serializers.SerializerMethodField()
    # def get_animal_category(self, obj):
    #     return obj.animal_category.category_name

    # <---METHOD02:- to show whole CategorySerializer data---->
    
    animal_category = CategorySerializer()      #yaha ham animal_category ko bhi serailiz kara rahe hai , hamne ForeignKey ka use kia he models me 
    animal_color = AnimalColorSerializer(many = True)
    animal_breed = AnimalBreedSerializer(many = True)
    images = AnimalImagesSerializer(many = True)       #related_name="images" k karan hame images likhna pada
    # <---METHOD03:- custom data return by PAYLOAD METHOD---->
    # def to_representation(self, instance):
    #     payload = {
    #         'animal_category' : instance.animal_category.category_name,
    #         'animal_views' : instance.animal_views,
    #         'animal_likes' : instance.animal_likes,
    #         'animal_name' : instance.animal_name,
    #         'animal_description' : instance.animal_description,
    #         'ANIMAL': 'XXXX' 
    #     }
    #     return  payload
    
    
    class Meta:
        model = Animal
        #fields = ['animal_category', 'animal_views', 'animal_likes']   # yaha vo sari field denge jiska json data chahiye
        exclude = [ 'updated_at']    # yaha exclude list item ko chod k sab ko show kareg
        # fields = '__all__'

class AnimalLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalLocation
        fields = '__all__'


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()

    #<--- for validation of data --->

    def validate(self, data):
        if 'username' is data:
            user = User.objects.filter(username = data['username'])
            if user.exists():
                raise serializers.ValidationError('user name already taken')

        if 'email' is data:
            user = User.objects.filter(email = data['email'])
            if user.exists():
                raise serializers.ValidationError('user email already taken')

        return data



class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        if 'username' in data:
            user = User.objects.filter(username = data['username'])
            if not user.exists():
                raise serializers.ValidationError('user dose not exists')
        
        return data

