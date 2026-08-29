from django.db import models

class Product(models.Model):
    product_id =models.AutoField(primary_key=True)
    Image = models.ImageField(upload_to='Product_Images/')
    Product_Name =models.CharField (max_length=100)
    Category = models.CharField (max_length=100, null=False)
    Description = models.TextField (max_length=300, null=False)
    Added_At = models.DateTimeField(auto_now_add=True)
# this line must be inline with the code apply tabs for correct name of the products
    def __str__(self):
        return self.Product_Name

from django.contrib.auth.models import User


# these lines are for the prototype 
#class Review(models.Model):
 #   review_id = models.AutoField(primary_key=True)
  #  product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
   # user = models.ForeignKey(User, on_delete=models.CASCADE)
    #review_text = models.TextField()
    #is_duplicate = models.BooleanField(default=False)
    #created_at = models.DateTimeField(auto_now_add=True)
    
   #def __str__(self):
    #    return f'Review for {self.product.Product_Name} by {self.user.username}'


#Now model is updated for tracking IP and fake reviews using vader 
class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review_text = models.TextField()
    is_duplicate = models.BooleanField(default=False)
    #these four line are added 
    sentiment_score = models.FloatField(null=True, blank=True)
    sentiment_label = models.CharField(max_length=10, null=True, blank=True)  # NEW FIELD
    is_fake = models.BooleanField(default=False) # NEW FIELD
    ip_address = models.GenericIPAddressField(null=True, blank=True) # NEW FIELD
    
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review for {self.product.Product_Name} by {self.user.username}'