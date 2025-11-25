from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def index(request):
    return render(request, 'index.html')    

def starter(request):
    return render(request,'starter-page.html')

def appointment_request(request):
    if request.method == 'POST':
        # Get form data
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        date = request.POST.get('date', '')
        department = request.POST.get('department', '')
        doctor = request.POST.get('doctor', '')
        message = request.POST.get('message', '')
        
        # Validate required fields
        if not all([name, email, phone, date, department, doctor]):
            messages.error(request, 'Please fill in all required fields.')
            return redirect('index')
        
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
            logger.info(f'Appointment request sent successfully for {name}')
            
        except BadHeaderError:
            messages.error(request, 'Invalid header found. Please check your input.')
            logger.error(f'BadHeaderError in appointment request from {name}')
        except Exception as e:
            messages.error(request, f'There was an error: {str(e)}. Please try again.')
            logger.error(f'Error sending appointment email: {str(e)}')
        
        return redirect('index')
    
    return redirect('index')

def contact_request(request):
    if request.method == 'POST':
        # Get form data
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        subject = request.POST.get('subject', '')
        message = request.POST.get('message', '')
        
        # Validate required fields
        if not all([name, email, subject, message]):
            messages.error(request, 'Please fill in all fields.')
            return redirect('index')
        
        try:
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
            
            # Send email to admin
            send_mail(
                email_subject,
                email_message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.ADMIN_EMAIL],
                fail_silently=False,
            )
            
            # Send confirmation email to sender
            send_mail(
                'Message Received - CareCloud',
                f'Dear {name},\n\nThank you for contacting CareCloud.\n\nWe have received your message regarding: {subject}\n\nOur team will review your message and get back to you as soon as possible.\n\nBest regards,\nCareCloud Team',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            
            messages.success(request, 'Your message has been sent. Thank you!')
            logger.info(f'Contact message sent successfully from {name}')
            
        except BadHeaderError:
            messages.error(request, 'Invalid header found. Please check your input.')
            logger.error(f'BadHeaderError in contact form from {name}')
        except Exception as e:
            messages.error(request, f'There was an error: {str(e)}. Please try again.')
            logger.error(f'Error in contact form: {str(e)}')
        
        return redirect('index')
    
    return redirect('index')
