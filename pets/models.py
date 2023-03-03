from django.db import models


class SexPet(models.TextChoices):
    MALE = "Male"
    FEMALE = "Female"
    DEFAULT = "Not Informed"


# Create your models here.
class Pet(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    weight = models.FloatField()
    sex = models.CharField(
        max_length=20, choices=SexPet.choices, default=SexPet.DEFAULT
    )
    group = models.ForeignKey(
        "groups.Group", related_name="pets", on_delete=models.RESTRICT, null=True
    )
    traits = models.ManyToManyField("traits.Trait", related_name="pets")
