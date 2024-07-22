from django.contrib import admin
from django.db.models import Q

from .models import Division, Heya, Rank, Rikishi, Shusshin


@admin.register(Division)
class DivisionAdmin(admin.ModelAdmin):
    list_display = ("name", "level")
    readonly_fields = ("slug",)


@admin.register(Rank)
class RankAdmin(admin.ModelAdmin):
    list_display = ("name", "division", "order", "direction")
    readonly_fields = ("slug",)
    list_filter = ("division", "direction")


@admin.register(Heya)
class HeyaAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "master")
    readonly_fields = ("id",)


@admin.register(Shusshin)
class ShusshinAdmin(admin.ModelAdmin):
    list_display = ("__str__", "country", "prefecture")
    readonly_fields = ("slug",)


class ActiveFilter(admin.SimpleListFilter):
    title = "active"  # or use _('country') for translated title
    parameter_name = "active"

    def lookups(self, request, model_admin):
        return [("Yes", "Yes")]

    def queryset(self, request, queryset):
        if self.value() == "Yes":
            return queryset.exclude(Q(rank=None) | Q(intai__isnull=False))
        if self.value():
            return queryset.all()


@admin.register(Rikishi)
class RikishiAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "name_jp",
        "rank",
        "heya",
        "shusshin",
        "height",
        "weight",
        "birth_date",
        "debut",
        "intai",
    )
    list_filter = (ActiveFilter, "heya", "shusshin")
    search_fields = ("name", "name_jp")
    readonly_fields = ("id",)
