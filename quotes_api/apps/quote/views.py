from rest_framework.response import Response
from rest_framework.views import APIView

from quotes_api.apps.utils import check_request_param as rp
from .serializers import *
from bson import ObjectId
# Create your views here.

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


class QuotesHomeView(APIView):
    def get(self, request):
        data=QuotesHomeSerializer(data={
            'device_id': rp(request,'device_id'),
        })
        if data.is_valid():    
            quotes = Quote.objects.find_random_home(
               device_id = data.validated_data['device_id'])
            
            js = QuoteSerializer(quotes, many=True).data
            return Response(data={'ok':True,
                                'message': 'random quotes', 'quotes': js})
        else:
            return Response(data={'ok':False, 'message':data.errors})
        
class QuoteReadView(APIView):
    def get(self, request):
        data=QuoteReadSerializer(data={
            'quote_id': rp(request, 'quote_id')
        })
        if data.is_valid():
            quote = Quote.objects.filter(
                _id=ObjectId(data.validated_data['quote_id'])).first()
            if quote is not None:
                js = QuoteSerializer(quote).data
                return Response(data={'ok': True,
                                      'message': 'a quote from the server',
                                      'quote': js})
            else:
                return Response(data={'ok': False, 'message': 'invalid quote id'})
        else:
            return Response(data={'ok':False, 'message': data.errors})
    
class QuotesUpUpdateView(APIView):
    def put(self, request):
        data=QuotesUpUpdateSerializer(data={
            'quote_id': rp(request,'quote_id'),
            'device_id': rp(request,'device_id'),
        })
        if data.is_valid():
            print(data.validated_data)
            quote = Quote.objects.update_ups(
                device_id = data.validated_data['device_id'],
                _id=ObjectId(data.validated_data['quote_id']))
            if quote is not None:
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
            quote = Quote.objects.update_downs(
                device_id = data.validated_data['device_id'],
                _id=ObjectId(data.validated_data['quote_id']))
            if quote is not None:
                return Response(data={'ok': True, 'message': 'quote downs updated successfully'})
            else:
                return Response(data={'ok':False, 'message': 'invalid quote id'})
        else:
            return Response(data={'ok':False, 'message': data.errors})
