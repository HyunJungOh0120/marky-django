from django.db import models
from django.conf import settings
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
        ('IT', (
            ('IT Internet', 'IT Internet'),
            ('Mobile', 'Mobile'),
            ('Game', 'Game'),
            ('Science', 'Science'),
            ('IT Product', 'IT Product'),
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
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    topic = models.CharField(max_length=40, choices=CATEGORY_CHOICES)
    name = models.CharField(max_length=40, blank=False)
    parent = models.ForeignKey(
        'self', on_delete=models.PROTECT, blank=True, null=True)
    slug = models.SlugField(max_length=100)

    def __str__(self) -> str:
        return f'{self.name}-{self.topic}'

    class Meta:
        db_table = 'category'
