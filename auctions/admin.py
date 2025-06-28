
from django.contrib import admin

from .models import User, Listing, Bid, Comment

# Register your models here.

  

@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    filter_horizontal = ('watchlist',)

admin.site.register(Listing)
admin.site.register(Bid)
admin.site.register(Comment)

