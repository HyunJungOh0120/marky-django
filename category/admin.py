from django.contrib import admin

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'topic', 'user']
