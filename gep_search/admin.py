from django.contrib import admin
import gep_search.models as models

# Register your models here.
class PublisherAdmin(admin.ModelAdmin):
    list_display = ('id','file_name', 'col_name')
    readonly_fields = ['id', 'vec']

# Register your models here.
admin.site.register(models.gep,PublisherAdmin)