from django.urls import path
from .views import *

app_name = 'quotes_api.apps.quote'

urlpatterns = [
    path('api/quotes/create', QuotesCreateView.as_view()),
    path('api/quotes/home', QuotesHomeView.as_view()),
    path('api/quotes/read', QuoteReadView.as_view()),
    path('api/quotes/up/update', QuotesUpUpdateView.as_view()),
    path('api/quotes/down/update', QuotesDownUpdateView.as_view()),
    
]