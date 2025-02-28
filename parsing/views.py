from django.views.generic import ListView, DetailView, DeleteView
from .models import Chapter
from django.urls import reverse_lazy
from django.shortcuts import render
from .models import Chapter , WebBook
from core import celery_app
from django.http import JsonResponse
from .tasks import parse_chapter_task , book_find
from core import celery_app
from django.contrib.auth.decorators import login_required


class ChapterDetailView(DetailView):
    model = Chapter
    context_object_name = 'chapter'

def stop_task_view(request):
    task_id = request.session.get('celery_task_id')
    if task_id:
        print(task_id)
        celery_app.control.revoke(task_id,terminate=True)
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

    
@login_required(login_url="/")
def start_parsing_view(request):
    if request.method == 'POST' and not request.POST.get('stop'):
        tom = int(request.POST.get('tom'))
        chapter = int(request.POST.get('chapter'))
        process = parse_chapter_task.delay(tom, chapter)
        task_status = process.status
        request.session['celery_task_id'] = process.id  
        return render(request, 'parse_form.html', {'task_status': task_status})
    return render(request, 'parse_form.html')


@login_required(login_url="/")
def book_fin(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        user_id = request.user.id
        book_find.delay(url, user_id)
        return render(request, 'book_find.html')
    return render(request, 'book_find.html')
