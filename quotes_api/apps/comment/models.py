from djongo import models
from quotes_api.apps.comment.mannagers import CommentManager

from quotes_api.apps.quote.models import CommentableModel

# Create your models here.
class Comment(models.Model):
    _id = models.ObjectIdField(primary_key=True, db_column='_id')
    content = models.TextField()
    ups = models.JSONField(blank=True, null=True, default=list)
    ups_count = models.PositiveIntegerField(default=0)
    downs = models.JSONField(blank=True, null=True, default=list)
    downs_count = models.PositiveIntegerField(default=0)
    comments = models.JSONField(blank=True, null=True, default=list)
    comments_count = models.PositiveIntegerField(default=0)
    date = models.DateTimeField()    
    
    original_quote = models.TextField(default="")
    objects = CommentManager()
    class Meta:
        db_table = 'Comment'
    
    def __str__(self):
        return "{}".format(self._id)