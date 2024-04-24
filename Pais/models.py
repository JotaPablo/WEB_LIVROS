from django.db import models

# Create your models here.

class Pais(models.Model):
    nome_pais = models.CharField(max_length = 30)

    class Meta:
        verbose_name_plural = 'Países'
    
    def __str__(self):
        return self.nome_pais