from django.contrib import admin
from .models import CustomUser,District,State,PatientRegistration

from accounts.utils import patient_statistics,get_patient_growth_data




from django.contrib import admin
from .models import PatientRegistration, State, District

import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table
from reportlab.platypus import Table, TableStyle

import matplotlib.pyplot as plt
import numpy as np


from django.contrib import admin
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor
from accounts.models import PatientRegistration


# Register your models here.

@admin.register(CustomUser)

class CustomUserAdmin(admin.ModelAdmin):

    list_display = ('email', 'first_name', 'last_name','mobile','password','is_active', 'is_staff', 'date_joined')
    list_filter = ('is_active', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('-date_joined',)



"""Register State and District"""



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

        # print(data)

        # Example implementation for generating a simple PDF
        response = HttpResponse(content_type='application/pdf')

        # response['Content-Disposition'] = 'attachment; filename="patients_data.pdf"'
        response['Content-Disposition'] = 'inline; filename="patients_data.pdf"'


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


        total_patients,total_male,total_female,total_other=patient_statistics()
       

            # Set the initial x-position
        x_start = content_start_x

        # Set font for the text (same font for all)
        p.setFont("Helvetica", 12)

        # Define each part of the content
        content_patients = f"Total Patients: {total_patients}"
        content_male = f"Male: {total_male}"
        content_female = f"Female: {total_female}"
        content_other = f"Other: {total_other}"

        # Calculate the width of each string
        width_patients = p.stringWidth(content_patients, "Helvetica", 12)
        width_male = p.stringWidth(content_male, "Helvetica", 12)
        width_female = p.stringWidth(content_female, "Helvetica", 12)
        width_other = p.stringWidth(content_other, "Helvetica", 12)

        # Add horizontal spacing between each string based on their widths
        space_between =100  # This is the space between the texts (adjust as needed)

        # Draw Total Patients with auto width
        p.setFillColor(HexColor("#1F77B4"))  # Blue color
        p.drawString(x_start, y, content_patients)
        x_start += width_patients + space_between  # Move x-position to the right based on text width

        # Draw Male with auto width
        p.setFillColor(HexColor("#2CA02C"))  # Green color
        p.drawString(x_start, y, content_male)
        x_start += width_male + space_between  # Move x-position to the right

        # Draw Female with auto width
        p.setFillColor(HexColor("#9467BD"))  # Purple color
        p.drawString(x_start, y, content_female)
        x_start += width_female + space_between  # Move x-position to the right

        # Draw Other with auto width
        p.setFillColor(HexColor("#FF5733"))  # Orange color
        p.drawString(x_start, y, content_other)
        y -= 20  # Move down for the next line

  
        # Draw Table
       
        years, patients = get_patient_growth_data(year=False)

        patient_growth = {year: patient for year, patient in zip(years, patients)}
        
        table_data = [['Year', 'Patients']] + [[year, patient_growth[year]] for year in patient_growth]

        print(table_data)

        # Full page width

        content_width = page_width  # Use the full page width (or set content_width if margins are required)
        num_columns = len(table_data[0])  # Number of columns in the table

        column_width = content_width / num_columns*0.9  # Equal width for all columns
       


        table = Table(table_data, colWidths=[column_width] * num_columns)

        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
        ])
        table.setStyle(table_style)
        table.wrapOn(p, page_width, page_height)
        table.drawOn(p, content_start_x, y - len(table_data) * 21)
        


        # Define the top margin and existing header
        margin_top = 100
        # Subheading text
        subheading_text = "Patient number per year:"

        # Set the font for the subheading
        p.setFont("Helvetica-Bold", 12)
        p.setFillColor('green')  # Dark gray color

        # Calculate position for subheading (just below the header)
        y = page_height - margin_top - 20  # You can adjust the value to control spacing from the top

        # Draw subheading
        p.drawString(content_start_x, y, subheading_text)

        # Move y position down after the subheading for the table

        y -= 30  # Space between subheading and table (adjust as needed)
            
       

       # Step 1: Create and Save the Pie Chart as an Image

        fig, ax = plt.subplots(figsize=(6,6), subplot_kw=dict(aspect="equal"))

        recipe = ["375 g flour", "75 g sugar", "250 g butter", "300 g berries"]

        data = [float(x.split()[0]) for x in recipe]
        print(data)

        ingredients = [x.split()[-1] for x in recipe]

        def func(pct, allvals):
            absolute = int(np.round(pct / 100. * np.sum(allvals)))
            return f"{pct:.1f}%\n({absolute:d} g)"

        wedges, texts, autotexts = ax.pie(
            data,
            autopct=lambda pct: func(pct, data),
            textprops=dict(color="w")
        )

        ax.legend(
            wedges,
            ingredients,
            title="Ingredients",
            loc="center left",
            bbox_to_anchor=(1, 0, 0.5, 1)
        )

        plt.setp(autotexts, size=8, weight="bold")
        ax.set_title("Patient Distribution")

        # Save the figure as an image
        chart_path = "pie_chart.png"
        plt.savefig(chart_path, bbox_inches="tight")  # Save the chart with a tight layout
        plt.close()
        
        # Step 2: Draw the Image on the PDF 
        content_start_x = 50  # Horizontal position from the left
        content_start_y = 100  # Vertical position from the bottom

        p.drawImage(chart_path, content_start_x, content_start_y, width=300, height=300)

    


        # p.line(content_start_x, y, content_end_x, y)
        # y -= 20

        p.save()  # Finalize and save the PDF
    
        return response

    actions = ['export_to_excel','export_to_pdf']



# Register models in the admin site

admin.site.register(PatientRegistration, PatientRegistrationAdmin)
admin.site.register(State)
admin.site.register(District)
