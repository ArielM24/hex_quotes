from djongo import models
from django.utils import timezone

class QuoteManager(models.DjongoManager):
    def create_quote(self, data):
        quote = self.create(
            content=data['content'],
            author=data['author'],
            enabled=True,
            date=timezone.now(),
        )
        return quote
    
