from django.db import models


class Banner(models.Model):
    title = models.CharField(max_length=50, blank=True, null=True)
    image = models.ImageField(upload_to="banner_image/", blank=True, null=True)
    is_active = models.BooleanField(default=False)
    
    
    class Meta:
        verbose_name_plural = "Banners"
        
    def __str__(self):
        return self.title
    