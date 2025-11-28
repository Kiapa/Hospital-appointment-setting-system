from email import message
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError 
from django.contrib.auth.models import User
from django.conf import settings
from datetime import datetime
import logging


logger = logging.getLogger(__name__)

def index(request):
    from .models import Department, Doctor
    departments = Department.objects.all()
    doctors = Doctor.objects.filter(is_available=True)
    return render(request, 'index.html', {'departments': departments, 'doctors': doctors})

    

def starter(request):
    return render(request,'starter-page.html')

def appointment_request(request):
    if request.method == 'POST':
        # Get form data
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        date = request.POST.get('date', '')
        department_id = request.POST.get('department', '')
        doctor_id = request.POST.get('doctor', '')
        message = request.POST.get('message', '')
        
        # Validate required fields
        if not all([name, email, phone, date, department_id, doctor_id]):
            messages.error(request, 'Please fill in all required fields.')
            return redirect('index')
        
        try:
            # Save to database
            from .models import AppointmentRequest, Appointment, Patient, Doctor, Department
            from django.contrib.auth.models import User
            
            # Parse the datetime string
            appointment_dt = datetime.fromisoformat(date.replace('Z', '+00:00'))
            
            # Get objects
            dept_obj = Department.objects.get(id=department_id)
            doc_obj = Doctor.objects.get(id=doctor_id)
            
            # Create AppointmentRequest
            AppointmentRequest.objects.create(
                name=name,
                email=email,
                phone=phone,
                appointment_datetime=appointment_dt,
                department=dept_obj.name,
                doctor=f"Dr. {doc_obj.first_name} {doc_obj.last_name}",
                message=message
            )
            
            # Create User and Patient if not exist (to satisfy Appointment model constraints)
            user, created = User.objects.get_or_create(username=email, defaults={'email': email})
            if created:
                user.set_password('carecloud123') # Default password
                user.save()
            
            patient, created = Patient.objects.get_or_create(user=user, defaults={
                'first_name': name.split()[0],
                'last_name': name.split()[-1] if len(name.split()) > 1 else '',
                'phone': phone,
                'date_of_birth': '2000-01-01', # Placeholder
                'gender': 'O', # Placeholder
                'address': 'Unknown',
                'emergency_contact': 'Unknown'
            })
            
            # Create Appointment
            Appointment.objects.create(
                patient=patient,
                doctor=doc_obj,
                department=dept_obj,
                appointment_date=appointment_dt.date(),
                appointment_time=appointment_dt.time(),
                reason=message,
                status='pending'
            )
            
            # Compose email
            subject = f'New Appointment Request from {name}'
            email_message = f"""
New Appointment Request:

Name: {name}
Email: {email}
Phone: {phone}
Date: {date}
Department: {dept_obj.name}
Doctor: Dr. {doc_obj.first_name} {doc_obj.last_name}
Message: {message}
"""
            
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

def show(request):
    from .models import AppointmentRequest
    all = AppointmentRequest.objects.all()
    return render(request, 'show.html', {'all': all})

def delete(request, id):
    from .models import AppointmentRequest
    try:
        obj = AppointmentRequest.objects.get(id=id)
        obj.delete()
        messages.success(request, 'Deleted the patient')
        logger.info(f'Appointment request id {id} deleted successfully')
        return redirect('show')
    except Exception as e:
        messages.error(request, 'Error deleting the patient')
        logger.error(f'Error deleting appointment request id {id}: {str(e)}')   
        return redirect('show')
    
def edit(request, id):
    from .models import AppointmentRequest

    obj = get_object_or_404(AppointmentRequest, id=id)

    if request.method == 'POST':
        # Basic fields
        obj.name = request.POST.get('name', '')
        obj.email = request.POST.get('email', '')
        obj.phone = request.POST.get('phone', '')

        # appointment_datetime comes from <input type="datetime-local"> as 'YYYY-MM-DDTHH:MM'
        appt_dt = request.POST.get('appointment_datetime', '')
        try:
            if appt_dt:
                # fromisoformat accepts 'YYYY-MM-DDTHH:MM' (no seconds)
                obj.appointment_datetime = datetime.fromisoformat(appt_dt)
        except Exception:
            # if parsing fails, keep previous value and log
            logger.exception(f'Failed to parse appointment_datetime: {appt_dt}')

        obj.department = request.POST.get('department', '')
        obj.doctor = request.POST.get('doctor', '')
        obj.message = request.POST.get('message', '')

        # Status must match model choices (pending/confirmed/rejected)
        status_val = request.POST.get('status', '')
        if status_val in dict(AppointmentRequest.STATUS_CHOICES):
            obj.status = status_val

        # Checkbox presence -> boolean
        obj.is_processed = 'is_processed' in request.POST

        obj.save()
        messages.success(request, 'Appointment updated successfully')
        return redirect('show')

    return render(request, 'edit.html', {'obj': obj})

def register(request):
     if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            try:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                messages.success(request, "Account created successfully")
                return redirect('/')
            except:
                messages.error(request, "Username already exist")
        else:
            messages.error(request, "Passwords do not match")
        return render(request, 'registration.html')

    

