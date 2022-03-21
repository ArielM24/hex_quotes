from djongo import models
from .managers import *

# Create your models here.

class CommentableModel(models.Model):
    _id = models.ObjectIdField(primary_key=True, db_column='_id')
    content = models.TextField()
    ups = models.JSONField(blank=True, null=True, default=list)
    ups_count = models.PositiveIntegerField(default=0)
    downs = models.JSONField(blank=True, null=True, default=list)
    downs_count = models.PositiveIntegerField(default=0)
    comments = models.JSONField(blank=True, null=True, default=list)
    comments_count = models.PositiveIntegerField(default=0)
    date = models.DateTimeField()
    class Meta:
        abstract = True

class Quote(models.Model):
    _id = models.ObjectIdField(primary_key=True, db_column='_id')
    content = models.TextField()
    ups = models.JSONField(blank=True, null=True, default=list)
    ups_count = models.PositiveIntegerField(default=0)
    downs = models.JSONField(blank=True, null=True, default=list)
    downs_count = models.PositiveIntegerField(default=0)
    comments = models.JSONField(blank=True, null=True, default=list)
    comments_count = models.PositiveIntegerField(default=0)
    date = models.DateTimeField()
    
    author = models.TextField()
    enabled = models.BooleanField()
    days_to_die = models.PositiveIntegerField(default=7)
    objects = QuoteManager()
    class Meta:
        db_table = 'Quote'
    def __str__(self):
        return "{} {}".format(self._id, self.author)


