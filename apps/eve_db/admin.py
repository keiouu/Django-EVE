from django.contrib import admin
from apps.eve_db.models import *

class EVERaceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'short_description')
admin.site.register(EVERace, EVERaceAdmin)

class EVEPlayerCorporationInline(admin.TabularInline):
    model = EVEPlayerCorporation
    fields = ('name', 'ticker')
    extra = 0

class EVEPlayerAllianceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'ticker', 'member_count', 'date_founded')
    search_fields = ['name', 'ticker']
    date_hierarchy = 'date_founded'
    inlines = [EVEPlayerCorporationInline]
admin.site.register(EVEPlayerAlliance, EVEPlayerAllianceAdmin)

class EVEPlayerCorporationAdmin(admin.ModelAdmin):
    list_display = ('id', '__unicode__', 'ticker', 'member_count', 'alliance')
    search_fields = ['name', 'ticker']
admin.site.register(EVEPlayerCorporation, EVEPlayerCorporationAdmin)
