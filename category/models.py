
from user.models import MyUser
from django.db import models
from user.models import MyUser
# Create your models here.


class Category(models.Model):
    CATEGORY_CHOICES = [
        ('Life', (
            ('daily', 'Daily',),
            ('relationship', 'RelationShip',),
            ('family', 'Family',),
            ('pets', 'Pets',),
            ('hobby', 'Hobby',),
            ('photography', 'Photography',),
            ('cook', 'Cook',),
            ('car', 'Car',),
            ('interior', 'Interior',),
            ('fashion/beauty', 'Fashion/Beauty',),
            ('health', 'Health',),
        )),
        ('Travel/Restaurants', (
            ('domestic', 'Domestic',),
            ('oversea', 'Oversea',),
            ('camping/hiking', 'Camping/Hiking',),
            ('restaurants', 'Restaurants',),
            ('cafe', 'Cafe',),
        )),
        ('Entertainment', (
            ('tv', 'Tv',),
            ('star', 'Star'),
            ('movie', 'Movie'),
            ('music', 'Music'),
            ('book', 'Book'),
            ('animation', 'Animation'),
            ('exhibition', 'Exhibition'),
            ('show', 'Show'),
            ('craft', 'Craft'),
        )),
        ('Sports', (
            ('sports', 'Sports'),
            ('sports', 'Soccer'),
            ('volleyball', 'Volleyball'),
            ('baseball', 'Baseball'),
            ('basketball', 'Basketball'),
            ('golf', 'Golf'),
        )),
        ('Current', (
            ('government', 'Government'),
            ('society', 'Society'),
            ('education', 'Education'),
            ('international', 'International'),
            ('business', 'Business'),
            ('economy', 'Economy'),
            ('job', 'Job'),
        )),
        ('Event', (
            ('event', 'Event'),
        ))
    ]
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    topic = models.CharField(max_length=40, choices=CATEGORY_CHOICES)
    name = models.CharField(max_length=40, blank=False)
    parent = models.ForeignKey('self', on_delete=models.PROTECT)
    slug = models.SlugField(max_length=100)

    def __str__(self) -> str:
        return self.topic