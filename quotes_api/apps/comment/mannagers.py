from djongo import models
from django.utils import timezone

class CommentManager(models.DjongoManager):
    def create_to_quote(self, data):
        comment = self.create(
            content=data['content'],
            original_quote=data['quote_id'],
            date=timezone.now(),
        )
        return comment
    
    def create_to_comment(self, data):
        comment = self.create(
            content=data['content'],
            original_quote=data['original_quote'],
            date=timezone.now(),
        )
        return comment