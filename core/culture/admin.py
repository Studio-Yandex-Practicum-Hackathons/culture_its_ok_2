from django.contrib import admin

from .models import Exhibit, FeedBack, Review, Route, RouteExhibit


class ExhibitInline(admin.TabularInline):
    model = RouteExhibit
    extra = 1


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username', 'exhibit', 'text',)
    search_fields = ['exhibit__name', 'username']
    list_filter = ['exhibit', 'text', 'username']
    empty_value_display = '-пусто-'


@admin.register(Exhibit)
class ExhibitAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'name',)
    search_fields = ['author', 'name']
    list_filter = ['author', 'name']
    empty_value_display = '-пусто-'


@admin.register(FeedBack)
class FeedBackAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username', 'text',)
    search_fields = ['username', 'text']
    list_filter = ['username', 'text']
    empty_value_display = '-пусто-'


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name',)
    search_fields = ['name']
    list_filter = ['name']
    empty_value_display = '-пусто-'
    inlines = (ExhibitInline,)
