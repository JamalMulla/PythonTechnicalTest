from django.db import models

class Bond(models.Model):
    isin = models.CharField(max_length=35)
    size = models.IntegerField()
    currency = models.CharField(max_length=6)
    maturity = models.DateField()
    lei = models.CharField(max_length=20)
    legal_name = models.CharField(max_length=100)
    owner = models.ForeignKey('auth.User', related_name='bonds', on_delete=models.CASCADE)
    def __str__(self):
        return self.legal_name
