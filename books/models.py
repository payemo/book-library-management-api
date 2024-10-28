from django.db import models
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError

class Book(models.Model):
    title = models.CharField(max_length=80)
    author = models.CharField(max_length=80)
    published_date = models.DateField(blank=True, null=True)
    isbn = models.CharField(
        primary_key=True,
        max_length=13,
        validators=[MinLengthValidator(13, message="ISBN must be exactly 13 characters")]
    )
    pages = models.PositiveIntegerField(blank=True, null=True)
    cover = models.URLField(blank=True, null=True)
    language = models.CharField(
        max_length=3,
        validators=[MinLengthValidator(3, message="ISO 639-3 language code must be exactly 3 characters.")],
        db_comment="ISO 639-3 language code"
    )

    def clean(self):
        """
        Additional model-level validation to ensure the exact length of an appropriate fields.
        """
        super().clean()
        if len(self.isbn) != 13:
            raise ValidationError({'isbn': "ISBN must be exactly 13 characters long."})
        if len(self.language) != 3:
            raise ValidationError({'language': "Language code must be exactly 3 characters long."})

    def __str__(self):
        return f"{self.title}:{self.isbn}"
    
    class Meta:
        db_table = 'books'
        unique_together = ["title", "author"]
        constraints: [
            models.CheckConstraint(
                check=models.Q(isbn__regex=r'^.{13}$'),
                name='isbn_fixed_len_13'
            ),
            models.CheckConstraint(
                check=models.Q(language__regex=r'^.{3}$'),
                name='language_fixed_len_3'
            ),
        ]
