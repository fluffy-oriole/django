from django.contrib import admin

# Register your models here.
from students.models import Student, Group

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'group_id']

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]