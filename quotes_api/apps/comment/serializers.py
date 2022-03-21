from rest_framework import serializers
from .models import Comment
from quotes_api.apps.quote.serializers import CommentableModelSerializer


class CommentSerializer(CommentableModelSerializer,serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = CommentableModelSerializer.Meta.fields + ['original_quote']
        
class CommentToQuoteSerializer(serializers.Serializer):
    content = serializers.CharField(required=True)
    quote_id = serializers.CharField(required=True)
    
class CommentToCommentSerializer(serializers.Serializer):
    content = serializers.CharField(required=True)
    comment_id = serializers.CharField(required=True)
    
class CommentsReadSerializer(serializers.Serializer):
    quote_id = serializers.CharField(required=True)
    device_id = serializers.CharField(required=True)
    
class CommentsUpUpdateSerializer(serializers.Serializer):
    comment_id = serializers.CharField(required=True)
    device_id = serializers.CharField(required=True)
    
class CommentsDownUpdateSerializer(serializers.Serializer):
    comment_id = serializers.CharField(required=True)
    device_id = serializers.CharField(required=True)