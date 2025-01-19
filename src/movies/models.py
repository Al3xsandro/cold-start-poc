from enum import Enum
from django.db import models
from coldstart import settings


class RatingEnum(Enum):
    LIKE = "LIKE"
    DISLIKE = "DISLIKE"
    NONE = "NONE"

    @classmethod
    def choices(self):
        return [(key.value, key.name.title()) for key in self]


class MyMovieList(models.Model):
    movie_id = models.IntegerField()
    title = models.CharField(max_length=255)
    poster_path = models.CharField(max_length=512)
    vote_average = models.FloatField(null=True)
    genre_ids = models.CharField(max_length=512)
    overview = models.CharField(max_length=1024)
    release_date = models.DateField(null=True)
    rating = models.CharField(
        max_length=7,
        choices=RatingEnum.choices(),
        default=RatingEnum.NONE.value,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="mymovielist"
    )

    def __str__(self):
        return self.title
