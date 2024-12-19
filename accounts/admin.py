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



class PatientRegistrationAdmin(admin.ModelAdmin):

    list_display = ('name', 'gender','age','state', 'district', 'department','appointment_date','contact_number','aadhar_number','registered_by','registration_date_time')
    
    search_fields = ('name', 'last_name')

    class Media:
        js = ('account/js/custom.js',)  # Inject custom JavaScript for dynamic functionality



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
