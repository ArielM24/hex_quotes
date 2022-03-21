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
            quotes = Quote.objects.mongo_aggregate(
                [{'$sample': {'size': 5}}]
            )
            js = QuoteSerializer(quotes, many=True).data
            device_id = data.validated_data['device_id']
            i = 0
            while i < len(js):
                if device_id in js[i]['ups']:
                    js[i]['ups'] = True
                    js[i]['downs'] = False
                elif device_id in js[i]['downs']:
                    js[i]['ups'] = False
                    js[i]['downs'] = True
                else:
                    js[i]['ups'] = False
                    js[i]['downs'] = False
                js[i]['comments'] = None
                i += 1
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
