from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.feed, name='feed'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('perfil/', views.perfil_usuario, name='perfil'),
    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),
    path('perfil/senha/', views.alterar_senha, name='alterar_senha'),
    path('usuario/<str:username>/', views.detalhe_usuario, name='detalhe_usuario'),
    path('usuario/<int:user_id>/seguir/', views.seguir_usuario, name='seguir_usuario'),
    path('post/novo/', views.criar_post, name='criar_post'),
    path('post/<int:post_id>/curtir/', views.curtir_post, name='curtir_post'),
    path('post/<int:post_id>/comentar/', views.comentar_post, name='comentar_post'),
]
