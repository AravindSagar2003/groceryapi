from django.contrib import admin
from .models import Login,Registration,Product,Review,Cart,Order,Address,addCategory
# Register your models here.
admin.site.register(Registration)
admin.site.register(Login)
admin.site.register(Product)
admin.site.register(Review)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(Address)
admin.site.register(addCategory)


