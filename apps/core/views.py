from django.shortcuts import render
from django.http import JsonResponse
from .services import send_contact_email

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        try:
            send_contact_email(name, email, subject, message)
            return JsonResponse({'status': 'success', 'message': 'Message sent!'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

def index(request):
    context = {}
    return render(request, 'index.html', context)