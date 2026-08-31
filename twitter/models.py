from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, max_length=500)
    foto_perfil = models.URLField(blank=True, default='https://abs.twimg.com/sticky/default_profile_images/default_profile_400x400.png')
    seguindo = models.ManyToManyField(User, related_name='usuarios_seguidos', blank=True)

    def __str__(self):
        return self.user.username

class Post(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    conteudo = models.TextField(max_length=280)
    imagem = models.URLField(blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    curtidas = models.ManyToManyField(User, related_name='posts_curtidos', blank=True)

    def __str__(self):
        return f'{self.autor.username}: {self.conteudo[:30]}'

class Comentario(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comentarios')
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    conteudo = models.TextField(max_length=280)
    criado_em = models.DateTimeField(auto_now_add=True)
    