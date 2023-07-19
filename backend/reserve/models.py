from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

def user_directory_path(instance, filename):
    return 'reserve/{0}/{1}'.format(instance.title, filename)

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

class Spaces(models.Model):

    equipment = (
        ('plug', 'Plug'),
        ('screen', 'Screen'),
        ('hdmi', 'HDMI'),
        ('board', 'Board'),
        ('soundproof', 'Soundproof'),    
    )

    space = (
        ('desk', 'Desk'),
        ('room', 'Room'),
    )

    name = models.CharField(max_length=250)
    image = models.ImageField(upload_to=user_directory_path, blank=True, null=True)
    #occtime?
    # equip = models.ManyToManyField(Equipment, blank=True)
    type = models.CharField(max_length=10, choices=space)

class Booking(models.Model):
    space = models.OneToOneField(Spaces, blank=False, null=False, on_delete=models.CASCADE)
    date = models.DateField() 
    start_time = models.TimeField()
    end_time = models.TimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pplNumber = models.IntegerField() 
    