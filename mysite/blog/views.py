from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.db.models import Count  # will allow to perform aggregated count

from taggit.models import Tag
from haystack.query import SearchQuerySet

from .models import Post
from .forms import CommentForm, SearchForm


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

    # List of similar posts (using tags)
    post_tags_ids = post.tags.values_list('id', flat=True)  # retrieve list of ID's for the tags
    similar_posts = Post.published.filter(tags__in=post_tags_ids) \
        .exclude(id=post.id)  # get all posts that contain any of these tags
    similar_posts = similar_posts.annotate(same_tags=Count('tags')) \
                        .order_by('-same_tags', '-publish')[:4]  # descendant order of shared tags
    return render(request,
                  'blog/post/detail.html',
                  {'post': post,
                   'comments': comments,
                   'comment_form': comment_form,
                   'similar_posts': similar_posts})


def post_search(request):
    form = SearchForm()  # instantiate the SearchForm
    if 'query' in request.GET:
        form = SearchForm(request.GET)  # instantiate with the submitted GET data
        if form.is_valid():
            cd = form.cleaned_data
            results = SearchQuerySet().models(Post) \
                .filter(content=cd['query']).load_all()

            total_results = results.count()  # count total results

            return render(request,
                          'blog/post/search.html',
                          {'form': form,
                           'cd': cd,  # form.cleaned_data
                           'results': results,
                           'total_results': total_results})
    return render(request,
                  'blog/post/search.html',
                  {'form': form})
