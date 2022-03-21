from rest_framework import serializers
from .models import *


class CommentableModelSerializer(serializers.Serializer):
    _id = serializers.CharField(required=False)
    content = serializers.CharField()
    ups = serializers.JSONField(required=False)
    ups_count = serializers.IntegerField(default=0)
    downs = serializers.JSONField(required=False)
    downs_count = serializers.IntegerField(default=0)
    comments = serializers.JSONField(required=False)
    comments_count = serializers.IntegerField(default=0)
    date = serializers.DateTimeField(required=False)
    class Meta:
        fields = ['_id', 'content', 'ups', 'ups_count', 'downs',
         'downs_count', 'comments', 'comments_count', 'date']
        

class QuoteSerializer(CommentableModelSerializer,serializers.ModelSerializer):
    class Meta:
        model = Quote
        fields = CommentableModelSerializer.Meta.fields + ['author', 'enabled', 'days_to_die']
        
class QuotesCreateSerializer(serializers.Serializer):
    author = serializers.CharField(required=True)
    content = serializers.CharField(required=True)
    

    
class QuotesUpUpdateSerializer(serializers.Serializer):
    quote_id = serializers.CharField(required=True)
    device_id = serializers.CharField(required=True)
    
class QuotesDownUpdateSerializer(serializers.Serializer):
    quote_id = serializers.CharField(required=True)
    device_id = serializers.CharField(required=True)
    

    
class QuotesHomeSerializer(serializers.Serializer):
    device_id = serializers.CharField(required=True)
    
class QuoteReadSerializer(serializers.Serializer):
    quote_id = serializers.CharField(required=True)
    