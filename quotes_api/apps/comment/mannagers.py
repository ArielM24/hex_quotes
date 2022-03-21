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
    
    def find_ups_downs_comments(self, device_id):
        comments = self.mongo_aggregate(
                [
                    {
                        '$project': {
                            '_id': '$_id',
                            'content': 'content',
                            'original_quote': '$original_quote',
                            'ups_count': '$ups_count',
                            'downs_count': '$downs_count',
                            'comments': '$comments',
                            'comments_count': '$comments_count',
                            'date': '$date',
                            
                            "ups": {
                                '$in': [device_id, '$ups']
                            },
                            "downs": {
                                '$in': [device_id, '$downs']
                            }
                        }
                    }
                ]
            )
        return comments