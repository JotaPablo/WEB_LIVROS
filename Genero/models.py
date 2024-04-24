from django.db import models
#from Usuario.models import Usuario

# Create your models here.

class Genero(models.Model):
    nome_genero = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = 'Generos'
    
    def __str__(self):
        return self.nome_genero