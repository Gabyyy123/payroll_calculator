import os
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import google.generativeai as genai

@csrf_exempt
def summarize_payslip(request):
    if request.method == 'POST':
        try:
            # 1. Get the prompt from your HTML frontend
            data = json.loads(request.body)
            prompt = data.get('prompt', '')

            # 2. Grab the API key you saved in Render
            api_key = os.environ.get("GEMINI_API_KEY")
            if not api_key:
                return JsonResponse({'error': 'GEMINI_API_KEY is missing on Render'}, status=500)
            
            # 3. Connect to Google Gemini
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # 4. Generate the response
            response = model.generate_content(prompt)

            # 5. Send it back to the HTML
            return JsonResponse({'summary': response.text})

        except Exception as e:
            # If anything breaks, send the exact error back to the screen
            return JsonResponse({'error': str(e)}, status=500)
            
    return JsonResponse({'error': 'Only POST requests allowed'}, status=400)