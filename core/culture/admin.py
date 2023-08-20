from django.contrib import admin
from django.http import FileResponse

from .models import Exhibit, FeedBack, Review, Route, RouteExhibit
from .utils import generate_pdf


class ExhibitInline(admin.TabularInline):
    model = RouteExhibit
    extra = 1


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username', 'exhibit',)
    search_fields = ['exhibit__name', 'username']
    list_filter = ['exhibit', 'username']
    empty_value_display = '-пусто-'


@admin.register(Exhibit)
class ExhibitAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'name',)
    search_fields = ['author', 'name']
    list_filter = ['author', 'name']
    empty_value_display = '-пусто-'


@admin.register(FeedBack)
class FeedBackAdmin(admin.ModelAdmin):
    list_display = ('pk', 'email', 'text',)
    search_fields = ['email', 'text']
    list_filter = ['email', 'text']
    empty_value_display = '-пусто-'
    actions = ["export_as_pdf"]

    @admin.action(description="Скачать выбранные опросы в формате .pdf")
    def export_as_pdf(self, request, queryset):
        pdf = generate_pdf(queryset)
        return FileResponse(
            pdf, as_attachment=True, filename="report.pdf"
        )


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name',)
    search_fields = ['name']
    list_filter = ['name']
    empty_value_display = '-пусто-'
    inlines = (ExhibitInline,)
