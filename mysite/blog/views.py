from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from taggit.models import Tag
from .models import Post
from .forms import CommentForm


class PostListView(ListView):
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)

        if self.kwargs.get('tag_slug'):
            tag_slug = self.kwargs.get('tag_slug')
            tag = get_object_or_404(Tag, slug=tag_slug)
            context['tag'] = tag

        return context

    def get_queryset(self):
        if self.kwargs.get('tag_slug'):
            tag_slug = self.kwargs.get('tag_slug')
            tag = get_object_or_404(Tag, slug=tag_slug)
            return Post.published.filter(tags__in=[tag])

        return Post.published.all()


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    # list of active comments for this post
    comments = post.comments.filter(active=True)

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request,
                  'blog/post/detail.html',
                  {'post': post,
                   'comments': comments,
                   'comment_form': comment_form})
