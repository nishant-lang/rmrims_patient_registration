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
        data = queryset.values('name', 'gender', 'age', 'department', 'consultation_type', 'state__name', 'district__name', 'appointment_date', 'registered_by')
        df = pd.DataFrame(data)
        df.rename(columns={
            'state__name': 'State',
            'district__name': 'District',
            'registered_by__username': 'Registered By'
        }, inplace=True)

        # Generate Excel response
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="patients_data.xlsx"'
        df.to_excel(response, index=False, engine='openpyxl')
        return response

    actions = ['export_to_excel','export_to_pdf']


    # def get_urls(self):
    #     """Override get_urls to add custom URL patterns for the admin interface."""
    #     urls = super().get_urls()

    #     custom_urls = [
    #         path(
    #             'load_districts/', self.admin_site.admin_view(self.load_districts),name='load_districts'
    #         ),
    #     ]

    #     return custom_urls + urls


    # def load_districts(self, request):
    #     """
    #     AJAX endpoint to fetch districts for a given state.
    #     """
    #     state_id = request.GET.get('state')

    #     if not state_id:
    #         print({'error': 'State ID is required'})
    #         return JsonResponse({'error': 'State ID is required'}, status=400)

    #     try:
    #         districts = District.objects.filter(state_id=state_id).values('id', 'name')
    #         return JsonResponse(list(districts), safe=False)
        
    #     except District.DoesNotExist:
    #         print({'error': 'No districts found for the given state'})
    #         return JsonResponse({'error': 'No districts found for the given state'}, status=404)





# Register models in the admin site

admin.site.register(PatientRegistration, PatientRegistrationAdmin)
admin.site.register(State)
admin.site.register(District)
