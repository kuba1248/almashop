from django.contrib import admin
from .models import Category, Product, Chat, Watchlist, Likelist, Rating


# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug':('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'available', 'created', 'updated']
    list_filter = [ 'available', 'created', 'updated']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug':('name',)}

admin.site.register(Chat)
admin.site.register(Watchlist)
admin.site.register(Likelist)
admin.site.register(Rating)