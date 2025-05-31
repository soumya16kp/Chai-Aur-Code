from django.contrib import admin
from .models import ChaiVariety, ChaiReview

@admin.register(ChaiVariety)
class ChaiVarietyAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'price']

@admin.register(ChaiReview)
class ChaiReviewAdmin(admin.ModelAdmin):
    list_display = ['chai', 'user', 'rating', 'created_at']
    search_fields = ['chai__name', 'user__username', 'comment']

