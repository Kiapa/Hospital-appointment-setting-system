from django.core.management.base import BaseCommand
from careapp.models import Department, Doctor
import random

class Command(BaseCommand):
    help = 'Populates the database with sample departments and doctors'

    def handle(self, *args, **kwargs):
        self.stdout.write('Populating database...')

        # Departments
        departments_data = [
            {'name': 'Cardiology', 'description': 'Heart and cardiovascular system care.'},
            {'name': 'Neurology', 'description': 'Disorders of the nervous system.'},
            {'name': 'Pediatrics', 'description': 'Medical care for infants, children, and adolescents.'},
            {'name': 'Orthopedics', 'description': 'Care for the musculoskeletal system.'},
            {'name': 'Dermatology', 'description': 'Skin, hair, and nail conditions.'},
            {'name': 'Psychiatry', 'description': 'Mental health and emotional well-being.'},
            {'name': 'Ophthalmology', 'description': 'Eye and vision care.'},
            {'name': 'Gynecology', 'description': 'Female reproductive health.'},
            {'name': 'Urology', 'description': 'Urinary tract and male reproductive system.'},
            {'name': 'Oncology', 'description': 'Cancer diagnosis and treatment.'},
            {'name': 'ENT', 'description': 'Ear, Nose, and Throat conditions.'},
            {'name': 'Dental', 'description': 'Oral health and dentistry.'},
            {'name': 'General Medicine', 'description': 'Primary care and general health.'},
        ]

        departments = {}
        for dept_data in departments_data:
            dept, created = Department.objects.get_or_create(
                name=dept_data['name'],
                defaults={'description': dept_data['description']}
            )
            departments[dept.name] = dept
            if created:
                self.stdout.write(f'Created department: {dept.name}')
            else:
                self.stdout.write(f'Department already exists: {dept.name}')

        # Doctors
        doctors_data = [
            {'first_name': 'John', 'last_name': 'Doe', 'specialization': 'cardiology', 'dept': 'Cardiology'},
            {'first_name': 'Jane', 'last_name': 'Smith', 'specialization': 'neurology', 'dept': 'Neurology'},
            {'first_name': 'Emily', 'last_name': 'Johnson', 'specialization': 'pediatrics', 'dept': 'Pediatrics'},
            {'first_name': 'Michael', 'last_name': 'Brown', 'specialization': 'orthopedics', 'dept': 'Orthopedics'},
            {'first_name': 'Sarah', 'last_name': 'Davis', 'specialization': 'dermatology', 'dept': 'Dermatology'},
            {'first_name': 'David', 'last_name': 'Wilson', 'specialization': 'psychiatry', 'dept': 'Psychiatry'},
            {'first_name': 'Jennifer', 'last_name': 'Martinez', 'specialization': 'ophthalmology', 'dept': 'Ophthalmology'},
            {'first_name': 'Robert', 'last_name': 'Anderson', 'specialization': 'gynecology', 'dept': 'Gynecology'},
            {'first_name': 'William', 'last_name': 'Taylor', 'specialization': 'urology', 'dept': 'Urology'},
            {'first_name': 'Elizabeth', 'last_name': 'Thomas', 'specialization': 'oncology', 'dept': 'Oncology'},
            {'first_name': 'James', 'last_name': 'Hernandez', 'specialization': 'ent', 'dept': 'ENT'},
            {'first_name': 'Linda', 'last_name': 'Moore', 'specialization': 'dental', 'dept': 'Dental'},
            {'first_name': 'Richard', 'last_name': 'Martin', 'specialization': 'general', 'dept': 'General Medicine'},
            {'first_name': 'Susan', 'last_name': 'Jackson', 'specialization': 'cardiology', 'dept': 'Cardiology'},
            {'first_name': 'Joseph', 'last_name': 'Thompson', 'specialization': 'neurology', 'dept': 'Neurology'},
        ]

        for doc_data in doctors_data:
            email = f"{doc_data['first_name'].lower()}.{doc_data['last_name'].lower()}@example.com"
            if Doctor.objects.filter(email=email).exists():
                self.stdout.write(f'Doctor already exists: {email}')
                continue

            Doctor.objects.create(
                first_name=doc_data['first_name'],
                last_name=doc_data['last_name'],
                specialization=doc_data['specialization'],
                department=departments.get(doc_data['dept']),
                email=email,
                phone=f"555-01{random.randint(10, 99)}",
                bio=f"Dr. {doc_data['last_name']} is a specialist in {doc_data['specialization']}.",
                years_of_experience=random.randint(5, 25),
                is_available=True
            )
            self.stdout.write(f"Created doctor: Dr. {doc_data['first_name']} {doc_data['last_name']}")

        self.stdout.write(self.style.SUCCESS('Successfully populated database'))
