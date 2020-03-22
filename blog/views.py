from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView

from blog.models import Post, Comments
from blog.forms import PostForm, CommentForm


class AboutView(TemplateView):
    template_name = 'about.html'


class PostListView(ListView):
    model = Post
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login/'  # Where to direct useres if not logged in
    redirect_field_name = 'blog/post_detail.html'  # Direct them to html when logging in

    model = Post
    form_class = PostForm


class PostUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'  # Where to direct useres if not logged in
    redirect_field_name = 'blog/post_detail.html'  # Direct them to html when logging in

    model = Post
    form_class = PostForm


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    login_url = '/login/'
    template_name = 'post_confirm_delete.html'
    success_url = reverse_lazy('post_list')

class DraftListView(LoginRequiredMixin, ListView):
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('-created_date')


# Comments Functions
@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)


@login_required
def add_comment_to_post(request, pk):
        post = get_object_or_404(Post, pk=pk)
        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                # Connect comment to post object -- comment.post is foreign key to Post model
                comment.post = post
                comment.save()
                return redirect('post_detail', pk=post.pk)
        else:
            form = CommentForm()
        return render(request, 'comment_form.html', {'form': form})


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comments, pk=pk)
    comment.approve()
    comment.save()
    return redirect('post_detail', pk=comment.post.pk)


@login_required
def comment_remove(requet, pk):
    comment = get_object_or_404(Comments, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)