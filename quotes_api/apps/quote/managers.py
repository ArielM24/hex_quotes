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
    
    def find_random_home(self, device_id):
        quotes = self.mongo_aggregate(
            [
                {'$sample': {'size': 5}},
                {
                    '$project': {
                        '_id': '$_id',
                        'content': '$content',
                        'ups_count': '$ups_count',
                        'downs_count': '$downs_count',
                        'comments_coun': '$comments_coun',
                        'date': '$date',
                        'author': '$author',
                        'enabled': '$enabled',
                        'days_to_die': '$days_to_die',
                        'ups': {
                            '$in': [device_id, '$ups']
                        },
                        'downs': {
                            '$in': [device_id, '$downs']
                        }
                    }
                }
            ]
        )
        return quotes
    
    def update_ups(self, _id, device_id,):
        quote = self.filter(_id=_id).first()
        if quote is not None:
            if device_id in quote.downs:
                    quote.downs.remove(device_id)
                    quote.downs_count -= 1
            if device_id in quote.ups:
                quote.ups.remove(device_id)
                quote.ups_count -= 1
            else:
                quote.ups.append(device_id)
                quote.ups_count += 1
                
            quote.save()
        return quote
    
    def update_downs(self, _id, device_id):
        quote = self.filter(_id=_id).first()
        if quote is not None:
            if device_id in quote.ups:
                    quote.ups.remove(device_id)
                    quote.ups_count -= 1
            if device_id in quote.downs:
                quote.downs.remove(device_id)
                quote.downs_count -= 1
            else:
                quote.downs.append(device_id)
                quote.downs_count += 1
                
            quote.save()
        return quote