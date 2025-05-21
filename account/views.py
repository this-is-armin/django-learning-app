from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.views import View


class SignUpView(View):
    template_name = 'account/sign_up.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated: return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        try:
            user = User.objects.filter(username=username)
            if user.exists():
                raise ValidationError('نام کاربری قبلا استفاده شده است')
            
            invalid_chars = ['(', ')', '[', ']', '{', '}', '<', '>', '/', '\\', '|', '-', '~' '`', '!', '?', '@', '#', '%', '^', '&', '*', '-', '=', '+', 'username']
            for char in invalid_chars:
                if char in username:
                    raise ValidationError('نام کاربری حاوی علامت های غیر معتبر است')
            
            if password and confirm_password and password != confirm_password:
                raise ValidationError('گذرواژه ها باید مطابقت داشته باشند')
            
            User.objects.create_user(username=username, email=email, password=password).save()
            return redirect('account:sign-in')
        except ValidationError as e:
            for error in e.messages:
                messages.error(request, error)
            return render(request, self.template_name, {
                'username': username,
                'email': email,
                'password': password,
                'confirm_password': confirm_password
            })


class SignInView(View):
    template_name = 'account/sign_in.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated: return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home:home')
            raise ValidationError('نام کاربری یا گذرواژه نادرست است')
        except ValidationError as e:
            for error in e.messages:
                messages.error(request, error)
            return render(request, self.template_name, {
                'username': username,
                'password': password
            })


class SignOutView(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated: return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        logout(request)
        return redirect('home:home')


class ProfileView(View):
    template_name = 'account/profile.html'

    def setup(self, request, *args, **kwargs):
        self.user_instance = get_object_or_404(User, username=kwargs['username'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated: return redirect('home:home')
        if request.user.username != self.user_instance.username: return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, **kwargs):
        user = self.user_instance
        return render(request, self.template_name, {
            'user': user
        })


class SavedCoursesView(View):
    template_name = 'account/saved_courses.html'

    def setup(self, request, *args, **kwargs):
        self.user_instance = get_object_or_404(User, username=kwargs['username'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated: return redirect('home:home')
        if request.user.username != self.user_instance.username: return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, **kwargs):
        user = self.user_instance
        saved_courses = user.saved_courses.all()
        return render(request, self.template_name, {
            'user': user,
            'saved_courses': saved_courses
        })


class SavedOnePartsView(View):
    template_name = 'account/saved_one_parts.html'

    def setup(self, request, *args, **kwargs):
        self.user_instance = get_object_or_404(User, username=kwargs['username'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated: return redirect('home:home')
        if request.user.username != self.user_instance.username: return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, **kwargs):
        user = self.user_instance
        saved_one_parts = user.saved_one_parts.all()
        return render(request, self.template_name, {
            'user': user,
            'saved_one_parts': saved_one_parts
        })