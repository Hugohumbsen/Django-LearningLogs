from django.shortcuts import render, get_object_or_404
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
from django.http import HttpResponseRedirect ,Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

def index(request):
    """Página principal do learning_Log"""
    return render(request, 'learning_logs/index.html')

@login_required
def topics(request):
    """Mostra todos os assuntos"""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}  # Criando uma lista
    return render(request, 'learning_logs/topics.html', context)
@login_required
def topic(request, topic_id):
    """Mostra um único assunto e todas as suas entradas"""
    topic = get_object_or_404(Topic, id=topic_id)
    #garante que o assunto percente ao usuario atual
    if topic.owner != request.user:
        raise Http404
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)
@login_required
def new_topic(request):
    """Adiciona um novo tópico"""
    if request.method != 'POST':
        # Nenhum dado submetido, cria um formulário em branco
        form = TopicForm()
    else:
        # DADOS DE POST SUBMETIDOS, PROCESSA OS DADOS
        form = TopicForm(request.POST)  # Corrigido para request.POST
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            form.save()
            return HttpResponseRedirect(reverse('topics'))  # Corrigido para reverse

    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)
@login_required
def new_entry(request, topic_id):
    """Acrescenta uma nova entrada para um assunto em particular"""
    topic = get_object_or_404(Topic, id=topic_id)  # Uso de get_object_or_404
     #garante que o assunto percente ao usuario atual
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # Nenhum dado submetido, cria um formulário em branco
        form = EntryForm()
    else:
        # DADOS DE POST SUBMETIDOS, PROCESSA OS DADOS
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('topic', args=[topic_id]))

    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)
@login_required
def edit_entry(request, entry_id):
    """Edita uma entrada existente"""
    entry = get_object_or_404(Entry, id=entry_id)  # Uso de get_object_or_404
    topic = entry.topic
     #garante que o assunto percente ao usuario atual
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        # Dados de POST submetidos: processa os dados
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('topic', args=[topic.id]))

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)
