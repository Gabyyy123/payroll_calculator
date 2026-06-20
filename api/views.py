import os
import json
import requests
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def home_view(request):
    return render(request, 'index.html')

@csrf_exempt 
def generate_summary(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            prompt = data.get('prompt', '')
            api_key = os.environ.get('GEMINI_API_KEY')
            
            if not api_key:
                return JsonResponse({'error': 'API key missing.'}, status=500)

            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
            payload = {"contents": [{"parts": [{"text": prompt}]}]}
            
            response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})
            response_data = response.json()

            if response.status_code == 200:
                text = response_data['candidates'][0]['content']['parts'][0]['text']
                return JsonResponse({'summary': text})
            else:
                return JsonResponse({'error': 'Gemini API Error'}, status=500)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
            
    return JsonResponse({'error': 'Invalid request'}, status=400)