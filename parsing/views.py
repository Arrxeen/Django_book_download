from django.views.generic import ListView, DetailView, DeleteView
from .models import Chapter, WebBook
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from core import celery_app
from django.http import JsonResponse
from .tasks import parse_chapter_task, book_find
from django.contrib.auth.decorators import login_required

class ChapterDetailView(DetailView):
    model = Chapter
    context_object_name = 'chapter'

class ChapterDeleteView(DeleteView):
    model = Chapter

    def get_success_url(self):
        book_id = self.object.book.id
        return reverse_lazy('book_detail', kwargs={'pk': book_id})

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

def stop_task_view(request):
    task_id = request.session.get('celery_task_id')
    print(task_id)
    if task_id:
        celery_app.control.revoke(task_id, terminate=True)
        return JsonResponse({'status': 'stopped'})
    else:
        return JsonResponse({'status': 'no task found'})

class BookDeliteView(DeleteView):
    model = WebBook
    success_url = reverse_lazy('book_list')
    
    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

class BookListView(ListView):
    model = WebBook
    context_object_name = 'books'

class BookDetailView(DetailView):
    model = WebBook
    context_object_name = 'book'

    def post(self, request, *args, **kwargs):
        book = self.get_object()
        parse_chapter_task.delay(book.id)
        return redirect('book_detail', pk=book.pk)

@login_required(login_url="/")
def start_parsing_view(request):
    if request.method == 'POST' and not request.POST.get('stop'):
        book_id = request.POST.get('book_id')
        process = parse_chapter_task.delay(book_id)
        task_status = process.status
        request.session['celery_task_id'] = process.id  
        book = WebBook.objects.get(id=book_id)
        return render(request, 'parsing/webbook_detail.html', {'book': book, 'task_status': task_status})
    return JsonResponse({'status': 'no task found'})

@login_required(login_url="/")
def book_fin(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        user_id = request.user.id
        book_find.delay(url, user_id)
        return redirect('book_list')
    return render(request, 'book_find.html')
