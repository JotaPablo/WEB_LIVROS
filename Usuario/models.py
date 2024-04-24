from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from Pais.models import Pais
from django.utils import timezone
from Autor.models import Autor
from Genero.models import Genero


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        if not email:
            raise ValueError('O email é obrigatório.')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        user = self.create_user(username, email, password, **extra_fields)

        return user

class Usuario(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    data_joined = models.DateField(default=timezone.now)
    
    nome = models.CharField(max_length=150, null=True)
    telefone = models.CharField(max_length=11, null = True)
    descricao = models.TextField(null=True, blank=True)
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE, null=True)
    autor = models.ForeignKey(Autor, on_delete=models.SET_NULL, null=True, blank=True)
    generos_favoritos = models.ManyToManyField(Genero, blank=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_autor = models.BooleanField(default=False)
    is_private = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']