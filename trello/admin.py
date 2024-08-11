from django.contrib import admin
from .models import Company, UserProfile, Board, Add_Staff, Card_List, Board_Card

# Register your models here.
admin.site.register(Company)
admin.site.register(UserProfile)
admin.site.register(Board)
admin.site.register(Add_Staff)
admin.site.register(Board_Card)
admin.site.register(Card_List)
