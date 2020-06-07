from django.shortcuts import render, redirect, Http404
from django.views import View
from .models import NewsModel
from .forms import EditNewsForm
from users_app.models import EESUser, User
from users_app.permissions import has_moderator_permission, has_admin_permission
from django.core.exceptions import PermissionDenied

# Create your views here.


class NewsView(View):
    def get(self, request):
        news = NewsModel.objects.order_by('-publish_date')
        context = {
            'news': news
        }
        return render(request, 'news/index.html', context)


class NewsDeleteView(View):
    def post(self, request, id):
        try:
            news = NewsModel.objects.get(id=id)
        except NewsModel.DoesNotExist:
            raise Http404
        if not ((has_moderator_permission(request.user) and id == getattr(news, 'publisher') or has_admin_permission(request.user))):
            raise PermissionDenied
        news.delete()
        return redirect('news_app:news')


class NewsAddView(View):
    def get(self, request):
        if not has_moderator_permission(request.user):
            raise PermissionDenied
        form = EditNewsForm()
        context = {
            'form': form
        }
        return render(request, 'news/add.html', context)

    def post(self, request):
        if not has_moderator_permission(request.user):
            raise PermissionDenied

        form = EditNewsForm(request.POST)
        if form.is_valid():
            news = form.save(commit=False)
            news.publisher = User.objects.get(username=request.user)
            news.save()
            return redirect('news_app:show', id=NewsModel._meta.get_field('id').value_from_object(news))
        else:
            return redirect('news_app:add')


class NewsShowView(View):
    def get(self, request, id):
        try:
            news = NewsModel.objects.get(id=id)
        except NewsModel.DoesNotExist:
            raise Http404
        context = {
            'news': news
        }
        return render(request, 'news/show.html', context)


class NewsEditView(View):
    def get(self, request, id):
        try:
            news = NewsModel.objects.get(id=id)
        except NewsModel.DoesNotExist:
            raise Http404
        if not (has_moderator_permission(request.user) and request.user == getattr(news, 'publisher')):
            raise PermissionDenied
        form = EditNewsForm(instance=news)
        context = {
            'form': form,
            'id': id,
        }
        return render(request, 'news/edit.html', context)

    def post(self, request, id):
        try:
            news = NewsModel.objects.get(id=id)
        except NewsModel.DoesNotExist:
            raise Http404
        if not (has_moderator_permission(request.user) and request.user == getattr(news, 'publisher')):
            raise PermissionDenied
        form = EditNewsForm(request.POST, instance=news)
        if form.is_valid():
            news = form.save()
        return redirect('news_app:show', id=id)
