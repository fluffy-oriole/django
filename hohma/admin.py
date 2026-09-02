from django.contrib import admin

# Register your models here.
from hohma.models import hohma
@admin.register(hohma)
class HohmaAdmin(admin.ModelAdmin):
    pass