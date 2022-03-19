from rest_framework.response import Response
from rest_framework.views import APIView

from quotes_api.apps.utils import check_request_param as rp
from .serializers import *
from bson import ObjectId
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
        
class QuotesCreateView(APIView):
    def post(self, request):
        data=QuotesCreateSerializer(data=request.data)
        if data.is_valid():
            print(data.validated_data)
            quote = Quote.objects.create_quote(data.validated_data)
            print(quote)
            js = QuoteSerializer(quote)
            return Response(data={'ok': True,
                                  'message': 'quote created successfully',
                                  'quotes': [js.data]
                                  })
        else:
            return Response(data={'ok': False, 'message': data.errors})

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
                comment = Comment.objects.create_to_quote(data.validated_data)
                quote.comments.append(str(comment._id))
                quote.comments_count += 1
                quote.save()
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
                })
                to_comment.comments.append(str(comment._id))
                to_comment.comments_count += 1
                to_comment.save()
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
        return Response(data={'ok': True})
    
class QuotesUpUpdateView(APIView):
    def put(self, request):
        data=QuotesUpUpdateSerializer(data={
            'quote_id': rp(request,'quote_id'),
            'device_id': rp(request,'device_id'),
        })
        if data.is_valid():
            print(data.validated_data)
            quote = Quote.objects.filter(
                _id=ObjectId(data.validated_data['quote_id'])).first()
            if quote is not None:
                device_id = data.validated_data['device_id']
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
                return Response(data={'ok': True, 'message': 'quote ups updated successfully'})
            else:
                return Response(data={'ok':False, 'message': 'invalid quote id'})
        else:
            return Response(data={'ok':False, 'message': data.errors})
    
class QuotesDownUpdateView(APIView):
    def put(self, request):
        data=QuotesDownUpdateSerializer(data={
            'quote_id': rp(request,'quote_id'),
            'device_id': rp(request,'device_id'),
        })
        if data.is_valid():
            print(data.validated_data)
            quote = Quote.objects.filter(
                _id=ObjectId(data.validated_data['quote_id'])).first()
            if quote is not None:
                device_id = data.validated_data['device_id']
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
                return Response(data={'ok': True, 'message': 'quote downs updated successfully'})
            else:
                return Response(data={'ok':False, 'message': 'invalid quote id'})
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
            comment = Comment.objects.filter(
                _id=ObjectId(data.validated_data['comment_id'])).first()
            if comment is not None:
                device_id = data.validated_data['device_id']
                if device_id in comment.downs:
                    comment.downs.remove(device_id)
                    comment.downs_count -= 1
                    
                if device_id in comment.ups:
                    comment.ups.remove(device_id)
                    comment.ups_count -= 1
                else:
                    comment.ups.append(device_id)
                    comment.ups_count += 1
                    
                comment.save()
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
            comment = Comment.objects.filter(
                _id=ObjectId(data.validated_data['comment_id'])).first()
            if comment is not None:
                device_id = data.validated_data['device_id']
                if device_id in comment.ups:
                    comment.ups.remove(device_id)
                    comment.ups_count -= 1
                    
                if device_id in comment.downs:
                    comment.downs.remove(device_id)
                    comment.downs_count -= 1
                else:
                    comment.downs.append(device_id)
                    comment.downs_count += 1
                    
                comment.save()
                return Response(data={'ok': True, 'message': 'comment downs updated successfully'})
            else:
                return Response(data={'ok':False, 'message': 'invalid comment id'})
        else:
            return Response(data={'ok':False, 'message': data.errors})