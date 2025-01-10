from django.contrib import admin
from .models import CustomUser,District,State,PatientRegistration

# Register your models here.


@admin.register(CustomUser)

class CustomUserAdmin(admin.ModelAdmin):

    list_display = ('email', 'first_name', 'last_name','mobile','password','is_active', 'is_staff', 'date_joined')
    list_filter = ('is_active', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('-date_joined',)



"""Register State and District"""

from django.contrib import admin
from .models import PatientRegistration, State, District

import pandas as pd
from reportlab.pdfgen import canvas

from django.contrib import admin
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor
from accounts.models import PatientRegistration


class PatientRegistrationAdmin(admin.ModelAdmin):


    list_display = ('name', 'gender', 'age', 'department', 'consultation_type', 'state', 'district', 'appointment_date', 'registered_by')
    
    list_filter = ('gender', 'department', 'consultation_type', 'state')  # Add filters

    search_fields = ('name', 'last_name')

    class Media:
        js = ('account/js/custom.js',)  # Inject custom JavaScript for dynamic functionality



    # Action to export to Excel
    @admin.action(description="Export to Excel")
    def export_to_excel(self, request, queryset):

        data = queryset.values('name', 'gender', 'age', 'department', 'consultation_type', 'state', 'district', 'appointment_date', 'registered_by')

        df = pd.DataFrame(data)

        df.rename(columns={
            'name':'Name',
            'gender':'Gender',
            'age':'Age',
            'department':'Department',
            'consultation_type':'Consultation Type',
            'state': 'State',
            'district': 'District',
            'appointment_date':'Appointment Date',      
            'registered_by': 'Registered By',

        }, inplace=True)

        # Generate Excel response
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="patients_data.xlsx"'
        df.to_excel(response, index=False, engine='openpyxl')
        return response
    

     # Action to export to Excel
    @admin.action(description="Export to Pdf")

    def export_to_pdf(self, request, queryset):

        data=queryset.values()

        # Example implementation for generating a simple PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="patients_data.pdf"'


        # Generate PDF using ReportLab
        page_width, page_height = letter  # Letter page size (612x792 points)
        content_width = page_width * 0.9  # 90% of the page width
        content_start_x = (page_width - content_width) / 2  # Left margin
        content_end_x = content_start_x + content_width  # Right margin



        # Generate PDF using ReportLab
        p = canvas.Canvas(response, pagesize=letter)
        y = 750  # Starting Y position for the text

        p.setFont("Helvetica-Bold", 16)

       # Set text color (for example, blue)
        # p.setFillColorRGB(0, 0, 1)  # RGB values for blue
        p.setFillColor(HexColor("#FF5733"))  # Set the color to orange using hex

        # Calculate the width of the text and center it
        pdf_header = 'Patient Registration Data'

        text_width = p.stringWidth(pdf_header, "Helvetica-Bold", 16)
        x = (612 - text_width) / 2  # 612 is the page width for letter size

        # Draw the header text centered
        p.drawString(x, y, pdf_header)

        y -= 20  # Move down for the next line


        # Draw a centered line (90% width)
        page_width = 612  # Standard letter size width
        line_width = page_width * 0.9  # 90% of the page width
        line_x_start = (page_width - line_width) / 2  # Center the line horizontally
        line_x_end = line_x_start + line_width
        p.setLineWidth(1)  # Set line thickness
        p.line(line_x_start, y, line_x_end, y)
        y -= 20  # Move down after the line


        # Add example content, ensuring it's within the 90% width area
        p.setFont("Helvetica", 12)
        example_text = "This is an example of content restricted to 90% of the page width."
        p.drawString(content_start_x, y, example_text)
        y -= 20

        # Additional content can also respect the boundaries
        additional_text = "All content is horizontally centered and restricted to 90% width."
        p.drawString(content_start_x, y, additional_text)
        y -= 20

        # Draw another horizontal line to separate sections
        p.line(content_start_x, y, content_end_x, y)
        y -= 20

        p.save()  # Finalize and save the PDF
    
        return response

    actions = ['export_to_excel','export_to_pdf']



# Register models in the admin site

admin.site.register(PatientRegistration, PatientRegistrationAdmin)
admin.site.register(State)
admin.site.register(District)
