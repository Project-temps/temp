from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse

def process_data(request):
    # Logic to process data (e.g., machine learning models) goes here
    return JsonResponse({'status': 'Data processed successfully'})


