from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login as auth_login, update_session_auth_hash
from .models import Post, Profile, Comentario

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.get_or_create(user=user)
            auth_login(request, user)
            return redirect('feed')
    else:
        form = UserCreationForm()
    return render(request, 'twitter/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('feed')
    else:
        form = AuthenticationForm()
    return render(request, 'twitter/login.html', {'form': form})

@login_required
def feed(request):
    perfil, created = Profile.objects.get_or_create(user=request.user)
    seguidos_ids = perfil.seguindo.values_list('id', flat=True)
    
    posts = Post.objects.filter(autor__id__in=seguidos_ids).union(
        Post.objects.filter(autor=request.user)
    ).order_by('-criado_em')
    
    sugestoes = Profile.objects.exclude(user=request.user).exclude(user__id__in=seguidos_ids)[:5]

    return render(request, 'twitter/feed.html', {
        'posts': posts, 
        'perfil': perfil, 
        'sugestoes': sugestoes
    })

@login_required
def perfil_usuario(request):
    perfil, created = Profile.objects.get_or_create(user=request.user)
    posts = Post.objects.filter(autor=request.user).order_by('-criado_em')
    return render(request, 'twitter/perfil.html', {'perfil': perfil, 'posts': posts})

@login_required
def editar_perfil(request):
    perfil, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        novo_nome = request.POST.get('first_name', '')
        if novo_nome:
            request.user.first_name = novo_nome
            request.user.save()
        
        nova_bio = request.POST.get('bio', '')
        if nova_bio != '':
            perfil.bio = nova_bio
            
        nova_foto = request.POST.get('foto_perfil', '')
        if nova_foto != '':
            perfil.foto_perfil = nova_foto
            
        perfil.save()
        return redirect('perfil')
    
    return render(request, 'twitter/editar_perfil.html', {'perfil': perfil})

@login_required
def alterar_senha(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('perfil')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'twitter/alterar_senha.html', {'form': form})

@login_required
def detalhe_usuario(request, username):
    usuario_alvo = get_object_or_404(User, username=username)
    perfil_alvo, created = Profile.objects.get_or_create(user=usuario_alvo)
    perfil_atual, created = Profile.objects.get_or_create(user=request.user)
    
    posts = Post.objects.filter(autor=usuario_alvo).order_by('-criado_em')
    esta_seguindo = perfil_atual.seguindo.filter(id=usuario_alvo.id).exists()
    
    return render(request, 'twitter/usuario.html', {
        'usuario_alvo': usuario_alvo,
        'perfil_alvo': perfil_alvo,
        'posts': posts,
        'esta_seguindo': esta_seguindo
    })

@login_required
def seguir_usuario(request, user_id):
    usuario_alvo = get_object_or_404(User, id=user_id)
    perfil_atual, created = Profile.objects.get_or_create(user=request.user)
    
    if request.user == usuario_alvo:
        return redirect('feed')
        
    if perfil_atual.seguindo.filter(id=usuario_alvo.id).exists():
        perfil_atual.seguindo.remove(usuario_alvo)
    else:
        perfil_atual.seguindo.add(usuario_alvo)
        
    return redirect('detalhe_usuario', username=usuario_alvo.username)

@login_required
def criar_post(request):
    if request.method == 'POST':
        conteudo = request.POST.get('conteudo')
        imagem = request.POST.get('imagem')
        if conteudo:
            Post.objects.create(autor=request.user, conteudo=conteudo, imagem=imagem)
    return redirect('feed')

@login_required
def curtir_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.curtidas.all():
        post.curtidas.remove(request.user)
    else:
        post.curtidas.add(request.user)
    return redirect('feed')

@login_required
def comentar_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        conteudo = request.POST.get('conteudo')
        if conteudo:
            Comentario.objects.create(post=post, autor=request.user, conteudo=conteudo)
    return redirect('feed')
    