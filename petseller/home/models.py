from django.db import models
from django.contrib.auth.models import User    # inbuilt user ko import kia
# from .choices import ANIMAL_CHOICES
from .choices import GENDER_CHOICES
import uuid


# <---imp Notes--->

# class Animal(models.Model):
#     user = models.ForeignKey(User, 
#            models.DO_NOTHING,          # DO_NOTHING :- ye parent(User) ko delete karne pe kooch nahi karega vaisa ka vaisa delete ho jayega
#            models.SET_DEFAULT,         # SET_DEFAULT:- ye Uset delete hone par ek default value show karega jo bhi dikhana chahe
#            models.SET_NULL,            # SET_NULL:- ye User delete hone pe null value de dega
#            models.CASCADE)             # CASCADE:-User delete karne pe jitne Animal(objects) usne create kie the sab delete ho jayenge 


class BaseModel(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now_add=True)

    class Meta:                  # class Meta ko abstract banayenge tab ye BaseModel ko as a model na le ke as a class treat karega
        abstract = True



class Category(BaseModel):
    category_name = models.CharField(max_length=100)
    def __str__(self) ->str:
        return self.category_name

class AnimalBreed(BaseModel):
    animal_breed = models.CharField(max_length=50)
    def __str__(self) ->str:
        return self.animal_breed
    

class AnimalColor(BaseModel):
    animal_color = models.CharField(max_length=50)
    def __str__(self) ->str:
        return self.animal_color
    



class Animal(BaseModel):
    animal_owner = models.ForeignKey(User, related_name="animal", on_delete=models.CASCADE)    #related_name="" :- foreign key me reverse relationship karne k lie
    # animal_category = models.CharField(max_length=100, choices = ANIMAL_CHOICES)     #ye ham tab use karenge jan hamari category limited hogi, mtlb ham age aur cate. add nahi karenge
    animal_category = models.ForeignKey(Category, related_name="category", on_delete=models.CASCADE)
    animal_views = models.IntegerField(default=0)
    animal_likes = models.IntegerField(default=1)
    animal_name = models.CharField(max_length=100)
    animal_description = models.TextField()
    animal_slug = models.SlugField(max_length=1000, unique=True)   #always make slug field unique
    animal_gender = models.CharField(max_length=50, choices=GENDER_CHOICES)
    animal_breed = models.ManyToManyField(AnimalBreed, null=True)
    animal_color = models.ManyToManyField(AnimalColor, null=True)

    def IncrementViews(self):
        self.animal_views += 1            #for the increment of Views
        self.save()

    def IncrementLikes(self):
        self.animal_likes += 1
        self.save()


    def __str__(self) ->str:
        return self.animal_name


class AnimalLocation(BaseModel):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name="location")
    location = models.CharField(max_length=100)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now_add=True)

    def __str__(self) ->str:
        return f'{self.animal.animal_name} Location'


class AnimalImages(BaseModel):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name="images")
    animal_images = models.ImageField(upload_to="animals", height_field=None, width_field=None, max_length=None)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now_add=True)

    def __str__(self) ->str:
        return f'{self.animal.animal_name} Images'
    


