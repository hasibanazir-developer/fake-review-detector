from django.contrib import admin
from .models import Product, Review
#this line is used to import html formate to display image on admin page
from django.utils.html import format_html
# Custom ModelAdmin for Review to disable adding and editing
class ReviewAdmin(admin.ModelAdmin):
    #this line is used to diplay the review list in tabuler form 
    list_display=('product','user','review_text','is_duplicate','sentiment_score','sentiment_label','is_fake', 'ip_address', 'created_at')
    
    def has_add_permission(self, request):
        return True  # Disable add permission

    def has_change_permission(self, request, obj=None):
        return True  # Disable edit permission

    def has_delete_permission(self, request, obj=None):
        return True  # Allow delete permission (by default, this is True, but it's included for clarity)
# thir class is used to view products in admin page with display imges in tabule form 
class ProductAdmin(admin.ModelAdmin):
    list_display=('display_image','Product_Name','Category','Description','Added_At')
      
    def display_image(self, obj):
        if obj.Image:  # assuming `Image` is an ImageField
            return format_html('<img src="{}" width="60" height="60" style="object-fit: cover;" />', obj.Image.url)
        return "No Image"

    display_image.short_description = 'Image'
    
    def has_add_permission(self, request):
        return True  # Disable add permission
    def has_change_permission(self, request, obj=None):
        return True  # Disable edit permission

    def has_delete_permission(self, request, obj=None):
        return True  # Allow delete permission (by default, this is True, but it's included for clarity)
    
# Register the Product model normally (no restrictions)
admin.site.register(Product,ProductAdmin)

# Register the Review model with custom permissions
admin.site.register(Review, ReviewAdmin)
