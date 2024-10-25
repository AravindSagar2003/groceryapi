
from django.urls import path

from .import views


urlpatterns = [
    path('registration/',views.registration_api.as_view(),name='registration'),
    path('login/',views.login_api.as_view(),name='login'),
    path('viewuser/',views.viewuser_api.as_view(),name='viewuser'),
    path('viewsingleuser/<int:id>',views.viewsingleuser_api.as_view(),name='viewsingleuser'),
    path('deleteuser/<int:id>',views.deleteuser_api.as_view(),name='deleteuser'),
    path('updateuser/<int:id>',views.updateuser_api.as_view(),name='updateuser'),
    path('addProduct/',views.addProduct.as_view(),name='addProduct'),
    path('viewProduct/',views.viewProduct.as_view(),name='viewProduct'),
    path('viewSingleProduct/<int:id>',views.viewSingleProduct.as_view(),name='viewSingleProduct'),
    path('updateProduct/<int:id>',views.updateProduct.as_view(),name='updateProduct'),
    path('addCategory/',views.addCategory.as_view(),name='addCategory'),
    path('viewCategory/',views.viewCategory.as_view(),name='viewCategory'),
    path('items/Category/<int:category_id>',views.ViewitembyCategoryAPI.as_view(),name='viewSingleProduct'),
    path('addReview/',views.addReview.as_view(),name='addReview'),
    path('viewReview/',views.viewReview.as_view(),name='viewReview'),
    path('deleteReview/<int:id>',views.deletereview_api.as_view(),name='deleteReview'),
    path('updateReview/<int:id>',views.updateReview.as_view(),name='updateReview'),
    path('addCart/',views.addCart.as_view(),name='addCart'),
    path('viewCart/',views.viewCart.as_view(),name='viewCart'),
    path('viewSingleCart/<int:userid>',views.viewSingleCart.as_view(),name='viewSingleCart'),
    path('deleteCart/<int:id>',views.deleteCart.as_view(),name='deleteCart'),

    path('wishlist/',views.wishList.as_view(),name='wishList'),
    path('viewWishlist/<int:userid>/', views.viewWishlist.as_view(), name='viewWishlist'),

    path('order/<int:userid>',views.order.as_view(),name='order'),
    path('viewOrder/<int:userid>',views.viewOrder.as_view(),name='viewOrder'),

    path('addaddress/',views.Addaddress_api.as_view(),name='addaddress'),
    path('viewalladdress/',views.viewalladdress_api.as_view(),name='viewalladdress'),
    path('updateaddress/<int:userid>',views.UpdateAddress_api.as_view(),name='updateaddress'),
    path('deleteaddress/<int:userid>',views.DeleteAddress_api.as_view(),name='deleteaddress'),  
    path('search/',views.search_api.as_view(),name='search'),   
    path('changepassword/<int:id>',views.change_pass_api.as_view(),name='changepassword'), 

]