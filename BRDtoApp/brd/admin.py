from django.contrib import admin
from .models import BRDVarity , BRDReview, brdcertificate

# Register your models here.

class BRDReviewInline(admin.TabularInline):
    model = BRDReview
    extra = 2

class BRDVarityAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'date_added')
    inlines = [BRDReviewInline]

class BRDcertificateAdmin(admin.ModelAdmin):
    list_display = ('BRD', 'certificate_number', 'issued_date', 'valid_until')

admin.site.register(BRDReview)
admin.site.register(brdcertificate,BRDcertificateAdmin)

admin.site.register(BRDVarity)


