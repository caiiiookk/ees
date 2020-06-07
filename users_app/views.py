from django.shortcuts import render, redirect, Http404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from .models import EESUser
from courses_app.models import CourseModel, Course2Teacher, Course2Employee, Course2Student
from .forms import AdminPanelEESUserChangeForm
from django import views
from users_app import permissions
from .forms import EESUserProfileEditForm, UserProfileEditForm, forms
# Create your views here.


def users_view(request):
    users = User.objects.filter(is_active=True).order_by('username')
    context = {
        'users': users,
    }
    return render(request, 'users/index.html', context)


def profile_view(request, id):
    try:
        opened_user = User.objects.get(id=id)
    except:
        raise Http404
    student_courses = CourseModel.objects.filter(course2student__in=Course2Student.objects.filter(student=opened_user)).order_by('id')
    teacher_courses = CourseModel.objects.filter(course2teacher__in=Course2Teacher.objects.filter(teacher=opened_user)).order_by('id')
    employee_courses = CourseModel.objects.filter(course2employee__in=Course2Employee.objects.filter(employee=opened_user)).order_by('id')
    context = {
        'opened_user': opened_user,
        'student_courses': student_courses,
        'teacher_courses': teacher_courses,
        'employee_courses': employee_courses,
    }
    return render(request, 'users/profile.html', context)


class ProfileEditView(views.View):
    def get(self, request, id):
        try:
            opened_user = User.objects.get(id=id)
        except:
            raise Http404
        if opened_user != request.user:
            return redirect('users_app:profile', id=id)

        eesuser_form = EESUserProfileEditForm(instance=opened_user.eesuser)
        user_form = UserProfileEditForm(instance=opened_user)
        eesuser = opened_user.eesuser
        can_change_username = getattr(eesuser, 'can_change_username')
        can_change_email = getattr(eesuser, 'can_change_email')
        can_change_first_name = getattr(eesuser, 'can_change_first_name')
        can_change_last_name = getattr(eesuser, 'can_change_last_name')
        user_form.fields['username'].widget.attrs['readonly'] = not can_change_username
        user_form.fields['email'].widget.attrs['readonly'] = not can_change_email
        user_form.fields['last_name'].widget.attrs['readonly'] = not can_change_last_name
        user_form.fields['first_name'].widget.attrs['readonly'] = not can_change_first_name
        context = {
            'opened_user': opened_user,
            'eesuser_form': eesuser_form,
            'user_form': user_form,
        }
        return render(request, 'users/edit.html', context)

    def post(self, request, id):
        try:
            opened_user = User.objects.get(id=id)
        except:
            raise Http404
        if opened_user != request.user:
            return redirect('users_app:profile', id=id)

        eesuser_form = EESUserProfileEditForm(request.POST, request.FILES, instance=opened_user.eesuser)
        user_form = UserProfileEditForm(request.POST, instance=opened_user)
        eesuser = opened_user.eesuser
        can_change_username = getattr(eesuser, 'can_change_username')
        can_change_email = getattr(eesuser, 'can_change_email')
        can_change_first_name = getattr(eesuser, 'can_change_first_name')
        can_change_last_name = getattr(eesuser, 'can_change_last_name')
        cached_username = opened_user.username
        cached_last_name = opened_user.last_name
        cached_first_name = opened_user.first_name
        cached_email = opened_user.email
        if eesuser_form.is_valid() and user_form.is_valid():
            eesuser_form.save()
            updated_user = user_form.save(commit=False)
            if not can_change_first_name:
                updated_user.first_name = cached_first_name
            if not can_change_last_name:
                updated_user.last_name = cached_last_name
            if not can_change_email:
                updated_user.email = cached_email
            if not can_change_username:
                updated_user.username = cached_username
            updated_user.save()
            return redirect('users_app:profile', id=id)

        return redirect('users_app:edit', id=id)


class ProfileAdminPanelView(views.View):
    def get(self, request, id):
        try:
            opened_user = User.objects.get(id=id)
        except:
            raise Http404
        if not permissions.has_admin_permission(request.user):
            return redirect('users_app:profile', id=id)
        courses = CourseModel.objects.all()
        user_student_courses    = CourseModel.objects.filter(course2student__in=Course2Student.objects.filter(student=opened_user)).order_by('id')
        user_teacher_courses    = CourseModel.objects.filter(course2teacher__in=Course2Teacher.objects.filter(teacher=opened_user)).order_by('id')
        user_employee_courses   = CourseModel.objects.filter(course2employee__in=Course2Employee.objects.filter(employee=opened_user)).order_by('id')
        eesuser = opened_user.eesuser
        permissions_form = AdminPanelEESUserChangeForm(instance=eesuser)

        class UserIsActiveForm(forms.ModelForm):
            is_active = forms.BooleanField(
                widget=forms.CheckboxInput(
                    attrs={
                        'class': 'form-check-input',
                    },
                ),
                required=False,
            )
            class Meta:
                model = User
                fields = ['is_active']
        user_is_active_form = UserIsActiveForm(instance=opened_user)
        context = {
            'permissions_form': permissions_form,
            'opened_user': opened_user,
            'courses': courses,
            'user_student_courses': user_student_courses,
            'user_teacher_courses': user_teacher_courses,
            'user_employee_courses': user_employee_courses,
            'is_active': user_is_active_form,
        }
        return render(request, 'users/admin-panel.html', context)

    def post(self, request, id):
        try:
            opened_user = User.objects.get(id=id)
        except:
            raise Http404
        if not(request.user.is_superuser or permissions.has_admin_permission(request.user) and not opened_user == request.user):
            return redirect('users_app:profile', id=id)
        eesuser = opened_user.eesuser
        permissions_form = AdminPanelEESUserChangeForm(request.POST, instance=eesuser)

        class UserIsActiveForm(forms.ModelForm):
            is_active = forms.BooleanField(
                widget=forms.CheckboxInput(
                    attrs={
                        'class': 'form-check-input',
                    },
                ),
                required=False,
            )
            class Meta:
                model = User
                fields = ['is_active']
        user_is_active_form = UserIsActiveForm(request.POST, instance=opened_user)
        if permissions_form.is_valid() and user_is_active_form.is_valid():
            user_is_active_form.save()
            permissions_form.save()
            opened_user.is_active = user_is_active_form
            teacher_courses = request.POST.getlist('select2')
            employee_courses = request.POST.getlist('select4')
            student_courses = request.POST.getlist('select6')
            try:
                Course2Student.objects.filter(student=opened_user).delete()
            except:
                pass
            try:
                Course2Employee.objects.filter(employee=opened_user).delete()
            except:
                pass
            try:
                Course2Teacher.objects.filter(teacher=opened_user).delete()
            except:
                pass
            for course in student_courses:
                Course2Student.objects.create(student=opened_user, course=CourseModel.objects.get(id=course))
            for course in teacher_courses:
                Course2Teacher.objects.create(teacher=opened_user, course=CourseModel.objects.get(id=course))
            for course in employee_courses:
                Course2Employee.objects.create(employee=opened_user, course=CourseModel.objects.get(id=course))
        return redirect('users_app:admin-panel', id=id)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('main_app:main')
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.user_cache
            login(request, user)
            return redirect('/')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


def sign_up_view(request):
    if request.user.is_authenticated:
        return redirect('main_app:main')
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            EESUser.objects.create(user=user)
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('users_app:edit', id=user.id)
    else:
        form = UserCreationForm()
    return render(request, 'users/sign_up.html', {'form': form})


def my_profile_view(request):
    return redirect('users_app:profile', id=request.user.id)


def logout_view(request):
    logout(request)
    return redirect('/')
