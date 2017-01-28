from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown

from ..models import Post

register = template.Library()


@register.simple_tag  # processes the data and return a string
def total_posts():
    return Post.published.count()


@register.inclusion_tag('blog/post/latest_posts.html')  # processes the data and returns a rendered template
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


# Deprecated since version 1.9 (simple_tag should be used instead)
# but I'm using 1.8 version, soooo meh, whatever.
@register.assignment_tag  # processes the data nad sets a variable in the context
def get_most_commented_posts(count=5):
    return Post.published.annotate(
        total_comments=Count('comments')
    ).order_by('-total_comments')[:count]


@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
