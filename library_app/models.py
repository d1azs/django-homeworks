from django.db import models


class Author(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="First name")
    last_name = models.CharField(max_length=100, verbose_name="Last name")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Book(models.Model):
    title = models.CharField(max_length=200, verbose_name="Title")
    publishing_year = models.IntegerField(verbose_name="Publishing year")
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Price")
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name="books",
        verbose_name="Author",
    )

    def __str__(self):
        return f"{self.title} ({self.publishing_year})"