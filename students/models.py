from django.db import models

class Group(models.Model):
    name = models.TextField("Название")

    def __str__(self) -> str:
        return self.name

class Student(models.Model):
    name = models.TextField("Название")
    group = models.ForeignKey("Group", on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "Студент"
        verbose_name_plural = 'Студенты'