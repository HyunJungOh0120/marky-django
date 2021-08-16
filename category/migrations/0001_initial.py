# Generated by Django 3.2.6 on 2021-08-16 09:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(choices=[('Life', (('daily', 'Daily'), ('relationship', 'RelationShip'), ('family', 'Family'), ('pets', 'Pets'), ('hobby', 'Hobby'), ('photography', 'Photography'), ('cook', 'Cook'), ('car', 'Car'), ('interior', 'Interior'), ('fashion/beauty', 'Fashion/Beauty'), ('health', 'Health'))), ('Travel/Restaurants', (('domestic', 'Domestic'), ('oversea', 'Oversea'), ('camping/hiking', 'Camping/Hiking'), ('restaurants', 'Restaurants'), ('cafe', 'Cafe'))), ('Entertainment', (('tv', 'Tv'), ('star', 'Star'), ('movie', 'Movie'), ('music', 'Music'), ('book', 'Book'), ('animation', 'Animation'), ('exhibition', 'Exhibition'), ('show', 'Show'), ('craft', 'Craft'))), ('Sports', (('sports', 'Sports'), ('sports', 'Soccer'), ('volleyball', 'Volleyball'), ('baseball', 'Baseball'), ('basketball', 'Basketball'), ('golf', 'Golf'))), ('Current', (('government', 'Government'), ('society', 'Society'), ('education', 'Education'), ('international', 'International'), ('business', 'Business'), ('economy', 'Economy'), ('job', 'Job'))), ('Event', (('event', 'Event'),))], max_length=40)),
                ('slug', models.SlugField(max_length=100)),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='category.category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
