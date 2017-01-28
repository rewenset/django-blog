from django.contrib.sitemaps import Sitemap
from .models import Post


class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9  # relevance (maximum value is 1)

    def items(self):
        """ returns the QuerySet of objects
            to include in sitemap
        """
        return Post.published.all()

    def lastmod(self, obj):
        """ returns the last time the obj was modified
        """
        return obj.publish
