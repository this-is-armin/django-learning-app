from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.core.paginator import Paginator

from .models import Course, Episode, Comment, CourseSave


class AllCoursesView(View):
    template_name = 'course/all_courses.html'

    def get(self, request):
        courses = Course.objects.all().filter(is_published=True)        
        
        paginator = Paginator(courses, 4)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, self.template_name, {
            'courses': courses,
            'page_obj': page_obj
        })


class CourseView(View):
    template_name = 'course/course.html'

    def setup(self, request, *args, **kwargs):
        self.course_instance = get_object_or_404(Course, slug=kwargs['slug'])
        return super().setup(request, *args, **kwargs)
    
    def dispatch(self, request, *args, **kwargs):
        if self.course_instance.is_published == False: return redirect('course:all')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        course = self.course_instance
        episodes = course.episodes.all().filter(is_published=True)

        if request.user.is_authenticated:
            saved_course = CourseSave.objects.filter(user=request.user, course=course)

            if saved_course.exists(): 
                is_saved = True
            else: 
                is_saved = False
        else:
            is_saved = None

        return render(request, self.template_name, {
            'course': course,
            'episodes': episodes,
            'is_saved': is_saved
        })


class EpisodeView(View):
    template_name = 'course/episode.html'

    def setup(self, request, *args, **kwargs):
        self.course_instance = get_object_or_404(Course, slug=kwargs['slug'])
        self.episode_instance = get_object_or_404(Episode, counter=kwargs['counter'])
        return super().setup(request, *args, **kwargs)
    
    def dispatch(self, request, *args, **kwargs):
        if self.episode_instance.is_published == False: return redirect('course:all')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, **kwargs):
        episode = self.episode_instance
        comments = episode.comments.all().filter(is_published=True)
        return render(request, self.template_name, {
            'episode': episode,
            'comments': comments
        })
    
    def post(self, request, **kwargs):
        episode = self.episode_instance
        name = request.POST.get('name')
        comment = request.POST.get('comment')

        Comment.objects.create(episode=episode, name=name, comment=comment).save()
        
        return redirect(episode.detail())


class CourseSaveView(View):
    def setup(self, request, *args, **kwargs):
        self.course_instance = get_object_or_404(Course, slug=kwargs['slug'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated: return redirect(self.course_instance.detail())
        if self.course_instance.is_published == False: return redirect('course:all')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, **kwargs):
        course = self.course_instance

        saved_course = CourseSave.objects.filter(user=request.user, course=course)
        if not saved_course.exists():
            CourseSave.objects.create(user=request.user, course=course).save()
        return redirect(course.detail())


class CourseUnSaveView(View):
    def setup(self, request, *args, **kwargs):
        self.course_instance = get_object_or_404(Course, slug=kwargs['slug'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated: return redirect(self.course_instance.detail())
        if self.course_instance.is_published == False: return redirect('course:all')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, **kwargs):
        course = self.course_instance

        saved_course = CourseSave.objects.filter(user=request.user, course=course)
        if saved_course.exists():
            saved_course.delete()
        return redirect(course.detail())
