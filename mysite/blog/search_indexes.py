from haystack import indexes
from .models import Post


class PostIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)  # primary search field
    publish = indexes.DateTimeField(model_attr='publish')  # to provide additional filters to searches

    def get_model(self):
        return Post

    def index_queryset(self, using=None):
        return self.get_model().published.all()  # we are only including published posts
