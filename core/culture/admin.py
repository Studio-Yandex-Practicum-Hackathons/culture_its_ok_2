from django.contrib import admin
from django.utils.safestring import mark_safe
from django.http import FileResponse
from rangefilter.filters import (
    DateRangeQuickSelectListFilterBuilder,
)

from .models import (
    Exhibit, FeedBack, Review, Route,
    Photo, RouteExhibit, ExhibitPhoto)
from .utils import generate_pdf, update_spreadsheet


class ExhibitInline(admin.TabularInline):
    model = RouteExhibit
    extra = 1


class PhotoInline(admin.TabularInline):
    model = ExhibitPhoto
    extra = 1


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    readonly_fields = ["img_preview"]
    list_display = (
        "pk",
        "img_preview"
    )
    empty_value_display = "-пусто-"


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "username",
        "exhibit",
        "created_at"
    )
    search_fields = ["exhibit__name", "username"]
    list_filter = (
        "exhibit",
        "username",
        ("created_at", DateRangeQuickSelectListFilterBuilder()),
    )
    empty_value_display = "-пусто-"
    actions = ["export_to_spreadsheets", "export_as_pdf"]

    @admin.action(description="Скачать выбранные отзывы в формате pdf")
    def export_as_pdf(self, request, queryset):
        pdf = generate_pdf(queryset.order_by("exhibit"))
        return FileResponse(pdf, as_attachment=True, filename="report.pdf")

    @admin.action(
        description="Экспортировать выбранные отзывы в Google Spreadsheets"
    )
    def export_to_spreadsheets(self, request, queryset):
        return update_spreadsheet(queryset.order_by("exhibit"))


@admin.register(Exhibit)
class ExhibitAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "author",
        "name",
    )
    search_fields = ["author", "name"]
    list_filter = ["author", "name"]
    empty_value_display = "-пусто-"
    inlines = (PhotoInline,)


@admin.register(FeedBack)
class FeedBackAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "email",
        "text",
    )
    search_fields = ["email", "text"]
    list_filter = ["email", "text"]
    empty_value_display = "-пусто-"


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
    )
    search_fields = ["name"]
    list_filter = ["name"]
    empty_value_display = "-пусто-"
    inlines = (ExhibitInline,)
    readonly_fields = ["preview", "preview_map"]

    def preview(self, obj):
        return mark_safe(
            f'<img src="{obj.image.url}" style="max-height: 300px;">')

    def preview_map(self, obj):
        return mark_safe(
            f'<img src="{obj.route_map.url}" style="max-height: 200px;">')
