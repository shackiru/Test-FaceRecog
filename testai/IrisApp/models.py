from django.db import models

class Photo(models.Model):
    image = models.ImageField(upload_to='photos/')
    image_with_boundaries = models.ImageField(upload_to='photos/with_boundaries/', blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Photo {self.id}'
