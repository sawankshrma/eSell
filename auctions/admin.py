
from django.contrib import admin

from .models import User, Listing, Bid, Comment

# Register your models here.

# class FlightAdmin(admin.ModelAdmin):
#     list_display = ("__str__", "duration")

# class PassengerAdmin(admin.ModelAdmin):
#     filter_horizontal = ("flights",)
    

admin.site.register(User)
admin.site.register(Listing)
admin.site.register(Bid)
admin.site.register(Comment)

    