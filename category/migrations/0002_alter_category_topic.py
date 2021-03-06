# Generated by Django 3.2.6 on 2021-08-18 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='topic',
            field=models.CharField(choices=[('Life', (('daily', 'Daily'), ('relationship', 'RelationShip'), ('family', 'Family'), ('pets', 'Pets'), ('hobby', 'Hobby'), ('photography', 'Photography'), ('cook', 'Cook'), ('car', 'Car'), ('interior', 'Interior'), ('fashion/beauty', 'Fashion/Beauty'), ('health', 'Health'))), ('Travel/Restaurants', (('domestic', 'Domestic'), ('oversea', 'Oversea'), ('camping/hiking', 'Camping/Hiking'), ('restaurants', 'Restaurants'), ('cafe', 'Cafe'))), ('Entertainment', (('tv', 'Tv'), ('star', 'Star'), ('movie', 'Movie'), ('music', 'Music'), ('book', 'Book'), ('animation', 'Animation'), ('exhibition', 'Exhibition'), ('show', 'Show'), ('craft', 'Craft'))), ('IT', (('IT Internet', 'IT Internet'), ('Mobile', 'Mobile'), ('Game', 'Game'), ('Science', 'Science'), ('IT Product', 'IT Product'))), ('Sports', (('sports', 'Sports'), ('sports', 'Soccer'), ('volleyball', 'Volleyball'), ('baseball', 'Baseball'), ('basketball', 'Basketball'), ('golf', 'Golf'))), ('Current', (('government', 'Government'), ('society', 'Society'), ('education', 'Education'), ('international', 'International'), ('business', 'Business'), ('economy', 'Economy'), ('job', 'Job'))), ('Event', (('event', 'Event'),))], max_length=40),
        ),
    ]
