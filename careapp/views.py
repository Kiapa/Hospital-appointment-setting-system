from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

def index(request):
    return render(request, 'index.html')    

def starter(request):
    return render(request,'starter-page.html')

def appointment_request(request):
    if request.method == 'POST':
        # Get form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        date = request.POST.get('date')
        department = request.POST.get('department')
        doctor = request.POST.get('doctor')
        message = request.POST.get('message', '')
        
        # Compose email
        subject = f'New Appointment Request from {name}'
        email_message = f"""
        New Appointment Request:
        
        Name: {name}
        Email: {email}
        Phone: {phone}
        Date: {date}
        Department: {department}
        Doctor: {doctor}
        Message: {message}
        """
        
        try:
            # Send email to admin
            send_mail(
                subject,
                email_message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.ADMIN_EMAIL],
                fail_silently=False,
            )
            
            # Send confirmation email to patient
            send_mail(
                'Appointment Request Received - CareCloud',
                f'Dear {name},\n\nWe have received your appointment request for {date}.\nOur team will contact you shortly to confirm.\n\nThank you for choosing CareCloud.',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            
            messages.success(request, 'Your appointment request has been sent successfully!')
        except Exception as e:
            messages.error(request, 'There was an error sending your request. Please try again.')
        
        return redirect('index')
    
    return redirect('index')

def contact_request(request):
    if request.method == 'POST':
        # Get form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Save to database
        from .models import ContactMessage
        ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        
        # Compose email
        email_subject = f'Contact Form: {subject}'
        email_message = f"""
        New Contact Message:
        
        Name: {name}
        Email: {email}
        Subject: {subject}
        
        Message:
        {message}
        """
        
        try:
            # Send email to admin
            send_mail(
                email_subject,
                email_message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.ADMIN_EMAIL],
                fail_silently=False,
            )
            
            messages.success(request, 'Your message has been sent. Thank you!')
        except Exception as e:
            messages.error(request, 'There was an error sending your message. Please try again.')
        
        return redirect('index')
    
    return redirect('index')
