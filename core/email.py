from django.shortcuts import render
from django.core.mail import EmailMessage
from .forms import WasteReportForm
from .models import WasteReport, session
from django.conf import settings
import os

def report_waste(request):
    if request.method == 'POST':
        form = WasteReportForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # Save data to SQLAlchemy database
                waste = WasteReport(
                    description=form.cleaned_data['description'],
                    location=form.cleaned_data['location'],
                    waste_type=form.cleaned_data['waste_type'],
                    file_path=None  # Will set after saving the file
                )
                session.add(waste)
                session.commit()

                # Ensure the uploads directory exists
                upload_dir = 'uploads'
                if not os.path.exists(upload_dir):
                    os.makedirs(upload_dir)

                # Save file locally
                uploaded_file = request.FILES['file']
                file_path = os.path.join(upload_dir, uploaded_file.name)
                with open(file_path, 'wb') as destination:
                    for chunk in uploaded_file.chunks():
                        destination.write(chunk)

                # Update file path in database
                waste.file_path = file_path
                session.commit()

                # Send email
                try:
                    email = EmailMessage(
                        subject="New Waste Report",
                        body=f"Description: {waste.description}\nLocation: {waste.location}\nWaste Type: {waste.waste_type}",
                        from_email=settings.EMAIL_HOST_USER,
                        to=["rajbanshisoniya88@gmail.com"],
                    )
                    email.attach_file(file_path)
                    email.send(fail_silently=False)
                    print("Email sent successfully")
                except Exception as e:
                    print(f"Email sending failed: {str(e)}")

                return render(request, 'success.html', {'message': 'Report submitted and email sent successfully!'})

            except Exception as e:
                print(f"Error processing form: {str(e)}")
                return render(request, 'report_waste.html', {
                    'form': form,
                    'error': f'Error processing form: {str(e)}'
                })
        else:
            print("Form is not valid")
            print(form.errors)  # Print form errors
            return render(request, 'report_waste.html', {'form': form, 'error': 'Form is not valid'})
    else:
        form = WasteReportForm()
    
    return render(request, 'report_waste.html', {'form': form})
