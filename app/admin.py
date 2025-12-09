from django.contrib import admin
from app.models import (Customer,
                        Product,
                        Cart,
                        OrderPlaced,ContactUs)

# Register your models here.
@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display=('id','user','name','locality','city','zipcode','state')

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display=('id','title','selling_price','discounted_price','description','brand','category','product_image')

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display=('id','user','product','quantity')

@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display=('id','user','customer','product','quantity','ordered_date','status')

@admin.register(ContactUs)
class ContactUsModelAdmin(admin.ModelAdmin):
    list_display=('id','your_name','email_address','message')