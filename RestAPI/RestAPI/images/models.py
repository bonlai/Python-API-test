from django.db import models

# Create your models here.
class Image(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    image=models.ImageField(upload_to='Images/', default='Images/None/No-img.jpg')

    class Meta:
        db_table = "image"
