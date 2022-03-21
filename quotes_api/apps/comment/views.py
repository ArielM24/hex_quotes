from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from quotes_api.apps.quote.models import Quote
from .serializers import *
from .models import *
from bson import ObjectId
from quotes_api.apps.utils import check_request_param as rp


# Create your views here.
class CreateCommentView(APIView):
    def post(self, request):
        comment = CommentSerializer(data=request.data)
        print(request.data)
        if comment.is_valid():
            print(comment.validated_data)
            comment.save()
            return Response(data={'success': True})
        else:
            print(comment.errors)
            return Response(data={'success': False, 'errors': comment.errors})
        
class CommentToQuoteView(APIView):
    def post(self, request):
        print(request.query_params)
        
        data=CommentToQuoteSerializer(data={
            'content': request.data['content'],
            'quote_id': rp(request, 'quote_id'),
            })
        if data.is_valid():
            print(data.validated_data)
            quote = Quote.objects.filter(_id = ObjectId(data.validated_data['quote_id'])).first()
            if quote is not None:
                comment = Comment.objects.create_to_quote(data.validated_data, quote)
                
                js = CommentSerializer(comment)
                return Response(data={'ok':True,
                                      'message': 'comment created successfully',
                                      'comments': [js.data]})
            else:
                return Response(data={'ok':False, 'message':'invalid quote id'})
                
        else:
            return Response(data={'ok':False, 'message': data.errors})

    
class CommentToCommentView(APIView):
    def post(self, request):
        print(request.query_params)
        
        data=CommentToCommentSerializer(data={
            'content': request.data['content'],
            'comment_id': rp(request, 'comment_id'),
            })
        if data.is_valid():
            print(data.validated_data)
            to_comment = Comment.objects.filter(_id = ObjectId(data.validated_data['comment_id'])).first()
            if to_comment is not None:
                comment = Comment.objects.create_to_comment({
                    'content': data.validated_data['content'],
                    'original_quote': to_comment.original_quote
                }, to_comment)
                
                js = CommentSerializer(comment)
                return Response(data={'ok':True,
                                      'message': 'comment created successfully',
                                      'comments': [js.data]})
            else:
                return Response(data={'ok':False, 'message':'invalid comment id'})
                
        else:
            return Response(data={'ok':False, 'message': data.errors})
    
    
    
class CommentsReadView(APIView):
    def get(self, request):
        data=CommentsReadSerializer(data={
            'quote_id': rp(request,'quote_id'),
            'device_id': rp(request,'device_id'),
        })
        if data.is_valid():
            print(data.validated_data)
            device_id = data.validated_data['device_id']
            comments = Comment.objects.find_ups_downs_comments(device_id)
            
            js = CommentSerializer(comments, many=True).data
                    
            print(comments)
            return Response(data={'ok': True, 'message': 'list of comments',
                                  'comments':js})
        else:
            return Response(data={'ok':False, 'message': data.errors})
        
        
    
class CommentsUpUpdateView(APIView):
    def put(self, request):
        data=CommentsUpUpdateSerializer(data={
            'comment_id': rp(request,'comment_id'),
            'device_id': rp(request,'device_id'),
        })
        if data.is_valid():
            print(data.validated_data)
            comment = Comment.objects.update_ups(
                device_id = data.validated_data['device_id'],
                _id=ObjectId(data.validated_data['comment_id']))
            if comment is not None:
                return Response(data={'ok': True, 'message': 'comment ups updated successfully'})
            else:
                return Response(data={'ok':False, 'message': 'invalid comment id'})
        else:
            return Response(data={'ok':False, 'message': data.errors})
    
class CommentsDownUpdateView(APIView):
    def put(self, request):
        data=CommentsDownUpdateSerializer(data={
            'comment_id': rp(request,'comment_id'),
            'device_id': rp(request,'device_id'),
        })
        if data.is_valid():
            print(data.validated_data)
            comment = Comment.objects.update_downs(
                device_id = data.validated_data['device_id'],
                _id=ObjectId(data.validated_data['comment_id']))
            if comment is not None:
                return Response(data={'ok': True, 'message': 'comment downs updated successfully'})
            else:
                return Response(data={'ok':False, 'message': 'invalid comment id'})
        else:
            return Response(data={'ok':False, 'message': data.errors})