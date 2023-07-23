from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

def user_directory_path(instance, filename):
    return 'reserve/{0}/{1}'.format(instance.name, filename)

class Post(models.Model):

    class PostObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status='published')
        
    options = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    #post
    title = models.CharField(max_length=250)
    image = models.ImageField(upload_to=user_directory_path, blank=True, null=True)
    description = models.TextField(null=False)
    content = models.TextField()
    slug = models.SlugField(max_length=250, unique_for_date='published', null=False, unique=True)
    published = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reserve')
    #como ver el post
    status = models.CharField(max_length=10, choices=options, default='draft')
    objects = models.Manager()
    postObject = PostObjects()

class Location(models.Model):
    name = models.CharField(max_length=250)
    institution = models.CharField(max_length=250)
    general_info = models.TextField(null=False)
    schedule = models.TextField(null=False)
    services = models.TextField(null=False)
    geodata = models.TextField(null=False)
    web = models.URLField(max_length=200)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=250)
    image = models.ImageField(upload_to=user_directory_path, blank=True, null=True)

class Equipment(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(null=False)
    image = models.ImageField(upload_to=user_directory_path, blank=True, null=True)

class Space(models.Model):

    space = (
        ('desk', 'Desk'),
        ('room', 'Room'),
    )

    name = models.CharField(max_length=250)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)    
    image = models.ImageField(upload_to=user_directory_path, blank=True, null=True)
    type = models.CharField(max_length=10, choices=space)
    equipment = models.ManyToManyField(Equipment, blank=True)
    occupied = models.BooleanField(default=False)

class Room(Space):
    capacity = models.IntegerField()

class Desk(Space):
    nearby_pl = models.ManyToManyField('self', blank=True)

class Booking(models.Model):
    space = models.OneToOneField(Space, blank=False, null=False, on_delete=models.CASCADE)
    date = models.DateField() 
    start_time = models.TimeField()
    end_time = models.TimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
