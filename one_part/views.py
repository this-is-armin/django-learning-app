from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.core.paginator import Paginator

from .models import OnePart, Comment, OnePartSave


class AllOnePartView(View):
    template_name = 'one_part/all_one_part.html'

    def get(self, request):
        all_one_part = OnePart.objects.all().filter(is_published=True)

        paginator = Paginator(all_one_part, 4)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        if request.GET.get('search'):
            search_text = request.GET['search']
            all_one_part = OnePart.objects.filter(is_published=True, title__contains=search_text)

        return render(request, self.template_name, {
            'all_one_part': all_one_part,
            'page_obj': page_obj
        })


class OnePartView(View):
    template_name = 'one_part/one_part.html'

    def get(self, request, **kwargs):
        one_part = get_object_or_404(OnePart, slug=kwargs['slug'])
        comments = one_part.comments.all().filter(is_published=True)

        if request.user.is_authenticated:
            saved_one_part = OnePartSave.objects.filter(user=request.user, one_part=one_part)

            if saved_one_part.exists():
                is_saved = True
            else:
                is_saved = False
        else:
            is_saved = None

        return render(request, self.template_name, {
            'one_part': one_part,
            'comments': comments,
            'is_saved': is_saved
        })
    
    def post(self, request, **kwargs):
        one_part = get_object_or_404(OnePart, slug=kwargs['slug'])
        name = request.POST.get('name')
        comment = request.POST.get('comment')

        Comment.objects.create(one_part=one_part, name=name, comment=comment).save()
        
        return redirect(one_part.detail())


class OnePartSaveView(View):
    def setup(self, request, *args, **kwargs):
        self.one_part_instance = get_object_or_404(OnePart, slug=kwargs['slug'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated: return redirect(self.one_part_instance.detail())
        if self.one_part_instance.is_published == False: return redirect('one_part:all')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, **kwargs):
        one_part = self.one_part_instance

        saved_one_part = OnePartSave.objects.filter(user=request.user, one_part=one_part)
        if not saved_one_part.exists():
            OnePartSave.objects.create(user=request.user, one_part=one_part).save()
        return redirect(one_part.detail())


class OnePartUnSaveView(View):
    def setup(self, request, *args, **kwargs):
        self.one_part_instance = get_object_or_404(OnePart, slug=kwargs['slug'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated: return redirect(self.one_part_instance.detail())
        if self.one_part_instance.is_published == False: return redirect('one_part:all')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, **kwargs):
        one_part = self.one_part_instance

        saved_one_part = OnePartSave.objects.filter(user=request.user, one_part=one_part)
        if saved_one_part.exists():
            saved_one_part.delete()
        return redirect(one_part.detail())
