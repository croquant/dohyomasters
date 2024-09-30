from django.contrib import admin

from .models import Heya


@admin.register(Heya)
class HeyaAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "name_jp", "master")
    readonly_fields = ("id",)
    search_fields = ["name", "name_jp", "master"]
