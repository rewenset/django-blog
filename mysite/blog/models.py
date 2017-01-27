from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)  # VARCHAR in SQL
    slug = models.SlugField(max_length=250,  # intended to be used in URLs
                            unique_for_date='publish')
    author = models.ForeignKey(User,  # defines a many-to-one relationship
                               related_name='blog_posts')
    body = models.TextField()  # TEXT in SQL
    publish = models.DateTimeField(default=timezone.now)  # a timezone-aware datetime.now
    created = models.DateTimeField(auto_now_add=True)  # the date will be saved automatically
    updated = models.DateTimeField(auto_now=True)  # the date will be updated automatically
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='draft')

    class Meta:
        ordering = ('-publish',)  # sort results by the publish field in descending order

    def __str__(self):
        return self.title

    objects = models.Manager()      # the default manager
    published = PublishedManager()  # out custom manager

    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.strftime('%m'),
                             self.publish.strftime('%d'),
                             self.slug])
