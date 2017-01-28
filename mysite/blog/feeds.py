from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from .models import Post


class LatestPostsFeed(Feed):
    title = 'My blog'                     # correspond to the <title>,
    link = '/blog/'                       # <link>,
    description = 'New posts of my blog'  # <description> RSS elements

    def items(self):
        return Post.published.all()[:5]   # retrieving only the last five published posts

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords(item.body, 30)
