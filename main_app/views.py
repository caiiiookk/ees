from django.shortcuts import render, Http404, redirect
from django.views.generic import View
from .models import InfoPageModel
from .forms import EditPageForm
from users_app import permissions

# Create your views here.

allowed_pages = [
    'main',
    'contacts',
    'about',
]


class MainView(View):
    def get(self, request):
        page = InfoPageModel.objects.get_or_create_page(name='main')
        context = {
            'page': page,
        }
        return render(request, 'main/index.html', context)


class AboutView(View):
    def get(self, request):
        page = InfoPageModel.objects.get_or_create_page(name='about')
        context = {
            'page': page
        }
        return render(request, 'main/index.html', context)


class ContactsView(View):
    def get(self, request):
        page = InfoPageModel.objects.get_or_create_page(name='contacts')
        context = {
            'page': page
        }
        return render(request, 'main/index.html', context)


class EditPageView(View):
    def get(self, request, name):
        if name not in allowed_pages:
            raise Http404
        has_admin_permission = permissions.has_admin_permission(request.user)
        if not has_admin_permission:
            raise Http404
        page = InfoPageModel.objects.get_or_create_page(name=name)
        form = EditPageForm(instance=page)
        context = {
            'form': form,
            'name': name,
        }
        return render(request, 'main/edit.html', context)

    def post(self, request, name):
        if name not in allowed_pages:
            raise Http404
        if not permissions.has_admin_permission(request.user):
            raise Http404
        page = InfoPageModel.objects.get(name=name)
        form = EditPageForm(request.POST, instance=page)
        if form.is_valid():
            page = form.save()
        return redirect('main_app:' + name)
