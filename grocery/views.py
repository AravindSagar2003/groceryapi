from numbers import Number
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .models import  Category, Login, Registration, Product,Review,Cart,Wishlist,Order,Address
from django.db import transaction
from django.db.models import Q
from django.conf import settings
import cloudinary
import cloudinary.uploader
import cloudinary.api

from .serializers import LoginSerializer, RegisterSerializer,ProductSerializer,CategorySerializer,ReviewSerializer,CartSerializer,WishlistSerializer,OrderSerializer,AddressSerializer


from .models import Registration
from .import models
 



from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView

class registration_api(GenericAPIView):
    serializer_class = RegisterSerializer
    serializer_class_login = LoginSerializer

    def post(self, request):
        name = request.data.get('name')
        email = request.data.get('email')
        password = request.data.get('password')
        role = 'user'

        if Registration.objects.filter(email=email).exists():
            return Response({'message': 'Duplicate email found!'}, status=status.HTTP_400_BAD_REQUEST)

        login_data = {'email': email, 'password': password, 'role': role}
        serializer_login = self.serializer_class_login(data=login_data)
        if serializer_login.is_valid():
            log = serializer_login.save()
            login_id = log.id
        else:
            return Response({'message': 'Login creation failed', 'errors': serializer_login.errors}, status=status.HTTP_400_BAD_REQUEST)

        registration_data = {
            'name': name,
            'email': email,
            'password': password,  
            'login_id': login_id,
            'role': role
        }
        serializer = self.serializer_class(data=registration_data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data, 'message': 'Registration successful', 'success': 1}, status=status.HTTP_201_CREATED)

        return Response({'errors': serializer.errors, 'message': 'Registration failed', 'success': 0}, status=status.HTTP_400_BAD_REQUEST)

class login_api(GenericAPIView):
    serializer_class=LoginSerializer
    def post(self,request):
        email=request.data.get('email')
        password=request.data.get('password')
        log_var=Login.objects.filter(email=email,password=password)
        if log_var.count()>0:
            a=LoginSerializer(log_var,many=True)
            for i in a.data:
                login_id=i['id']
                role=i['role']
                register_data=Registration.objects.filter(login_id=login_id).values()
                print(register_data)
                for i in register_data:
                    id=i['id']

                return Response({'data':{'login_id':login_id,'email':email,'password':password,'role':role,},'success':1,'message':'login successfully' },status=status.HTTP_200_OK)
        else:
                return Response({'data':'user name or password invalid'},status.HTTP_400_BAD_REQUEST)

# Create your views here.
class viewuser_api(GenericAPIView):
     serializer_class = RegisterSerializer
     def get(self,request):
         user=Registration.objects.all()
         if (user.count()>0):
             serializer=RegisterSerializer(user,many=True)
             return Response({'data':serializer.data,'message':'data get','success':True},status=status.HTTP_200_OK)
         else:
             return Response({'data':'No data available'},status=status.HTTP_400_BAD_REQUEST)
         
class viewsingleuser_api(GenericAPIView):
     serializer_class = RegisterSerializer
     def get(self,request,id):
         user=Registration.objects.get(pk=id)
         serializer=RegisterSerializer(user)
         return Response(serializer.data)
     
class deleteuser_api(GenericAPIView):
     serializer_class = RegisterSerializer
     def delete(self,request,id):
         user=Registration.objects.get(pk=id)
         user.delete()
         return Response({'message':'data get','success':True},status=status.HTTP_200_OK)
     
class updateuser_api(GenericAPIView):
     serializer_class = RegisterSerializer
     def put(self,request,id):
         user=Registration.objects.get(pk=id)
         print(user)
         serializer=RegisterSerializer(instance=user,data=request.data,partial=True)
         print(serializer)
         if serializer.is_valid():
             serializer.save()
        
         return Response({'data':serializer.data, 'message':'updated successfully','success':1},status=status.HTTP_200_OK)
cloudinary.config(cloud_name ='dvcfqarqh',api_key='466318431137167',api_secret='aD2oPigfTq57HLKxPKAcq1SPp7A')

class addProduct(GenericAPIView):
    serializer_class = ProductSerializer

    def post(self, request):
        productname = request.data.get('productname')
        price = request.data.get('price')
        category_id = request.data.get('category')
        image = request.FILES.get('image')

        if not image:
            return Response({'message': 'Please upload a valid image', 'Error': True}, 
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            upload_data = cloudinary.uploader.upload(image)
            image_url = upload_data['url']

            category = models.Category.objects.get(id=category_id)
        except models.Category.DoesNotExist:
            return Response({'data': {'category': 'Category not found'}, 'message': 'failed', 
                             'success': 0}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': f'Error uploading image: {str(e)}', 'success': 0}, 
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = self.serializer_class(
            data={'image': image_url, 'productname': productname, 'price': price, 'category': category.id}
        )

        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data, 'message': 'Product Added Successfully', 
                             'success': 1}, status=status.HTTP_200_OK)
        
        return Response({'data': serializer.errors, 'message': 'Validation failed', 
                         'success': 0}, status=status.HTTP_400_BAD_REQUEST)
       
class viewProduct(GenericAPIView):
    serializer_class=ProductSerializer

    def get(self, request):
        user =Product.objects.all()
        if(user.count()>0):
            serializer=ProductSerializer(user,many=True)
            return Response({'data':serializer.data,'message':'data get','success':True},status=status.HTTP_200_OK)
        else:
            return Response({'data':'No Data available'},status=status.HTTP_400_BAD_REQUEST)

class viewSingleProduct(GenericAPIView):

    def get(self, request,id):
        queryset=Product.objects.get(pk=id)
        serializer=ProductSerializer(queryset)
        return Response(serializer.data)

class updateProduct(GenericAPIView):
    serializer_class=ProductSerializer
    def put(self,request,id):
        queryset=Product.objects.get(pk=id)
        print(queryset)
        serializer=ProductSerializer(
            instance=queryset,data=request.data,partial=True)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'message':'updated successfully','success':1},status=status.HTTP_200_OK)


class addCategory(GenericAPIView):
    serializer_class = CategorySerializer
    
    def post(self, request):
        category_name = request.data.get('categoryname')
        category_image = request.FILES.get('categoryimage')
        
        # Check if category image is provided
        if not category_image:
            return Response(
                {'message': 'Please upload a valid image', 'Error': True},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Upload the image to Cloudinary
        try:
            upload_data = cloudinary.uploader.upload(category_image)
            image_url = upload_data['url']
            
        except Exception as e:
            return Response(
                {'message': f'Failed to upload image: {str(e)}', 'success': 0},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Prepare the data for the serializer
        serializer = self.serializer_class(data={
            'categoryname': category_name,
            'categoryimage': image_url  # Use the URL from Cloudinary
        })
        
        # Validate and save the serializer
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'data': serializer.data, 'message': 'Category Added Successfully', 'success': 1},
                status=status.HTTP_201_CREATED
            )
        return Response(
            {'data': serializer.errors, 'message': 'failed', 'success': 0},
            status=status.HTTP_400_BAD_REQUEST
        )
class viewCategory(GenericAPIView):
    serializer_class=CategorySerializer

    def get(self, request):
        user =Category.objects.all()
        if(user.count()>0):
            serializer=CategorySerializer(user,many=True)
            return Response({'data':serializer.data,'message':'data get','success':True},status=status.HTTP_200_OK)
        else:
            return Response({'data':'No Data available'},status=status.HTTP_400_BAD_REQUEST)
   


class ViewitembyCategoryAPI(GenericAPIView):
    serializer_class = Product

    def get(self, request, category_id=None):
        if category_id:
            products = Product.objects.filter(category_id=category_id)
            print(f"Filtered products for category_id={category_id}: {products}")
            print(products.query)  # Output the SQL query for debugging
        else:
            products = Product.objects.all()
            print(f"All products: {products}")
            print(products.query)  # Output the SQL query for debugging

        if products.exists():
            serializer = ProductSerializer(products, many=True)
            return Response({'data': serializer.data, 'message': 'data retrieved', 'success': True}, status=status.HTTP_200_OK)

        print("No products found")
        return Response({'data': 'No data available', 'message': 'No items found for the specified category', 'success': False}, status=status.HTTP_400_BAD_REQUEST)

class addReview(GenericAPIView):
    serializer_class=ReviewSerializer
    def post(self, request):
        
        productid=request.data.get('productid')
        userid=request.data.get('userid')
        productname=""
        username=""
        description=request.data.get('description')


        product_data=Product.objects.filter(id=productid).values()
        for i in product_data:
            productname=i['productname']
            print(productname)

        user_data=Registration.objects.filter(login_id=userid).values()
        for i in user_data:
            username=i['name']
            print(username)

        serializer=self.serializer_class(
            data={'productid':productid,'userid':userid,'description':description})
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'message':'Successfully review added','success':1},status=status.HTTP_200_OK)
        return Response({'data':serializer.errors,'message':'failed','success':0},status=status.HTTP_400_BAD_REQUEST)

class viewReview(GenericAPIView):
    serializer_class=ReviewSerializer

    def get(self, request):
        user =Review.objects.all()
        if(user.count()>0):
            serializer=ReviewSerializer(user,many=True)
            return Response({'data':serializer.data,'message':'data get','success':True},status=status.HTTP_200_OK)
        else:
            return Response({'data':'No Data available'},status=status.HTTP_400_BAD_REQUEST)
        
class deletereview_api(GenericAPIView):
  def delete(self,request,id):
    result=Review.objects.get(pk=id)
    result.delete()
    return Response({"message": "User deleted successfully"}, status=status.HTTP_200_OK)
  
class updateReview(GenericAPIView):
    serializer_class=ReviewSerializer
    def put(self,request,id):
        queryset=Review.objects.get(pk=id)
        print(queryset)
        serializer=ReviewSerializer(
            instance=queryset,data=request.data,partial=True)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
 
            return Response({'data':serializer.data,'message':'updated successfully','success':1},status=status.HTTP_200_OK)
        


class addCart(GenericAPIView):
    serializer_class=CartSerializer

    def post(self, request):
        
        productid=request.data.get('productid')
        userid=request.data.get('userid')
        quantity=1
        cartstatus=0


        cart=Cart.objects.filter(productid=productid,userid=userid)
        if cart.exists():
            return Response({'message':'Item already exists','success':False},status=status.HTTP_400_BAD_REQUEST)
        

        productdata=Product.objects.filter(id=productid).first()
        if not productdata:
            return Response({'message':'Product not found','success':False},status=status.HTTP_400_BAD_REQUEST)
        

        productname=productdata.productname
        price=productdata.price
        image=productdata.image
        totalprice=price*quantity


        print(f"total price:{totalprice}")

        serializer=self.serializer_class(
            data={'productid':productid,'userid':userid,'productname':productname,'price':price, 'quantity':quantity,'cartstatus':cartstatus,'image':image})
        

        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'message':'added to cart successfully','success':True},status=status.HTTP_200_OK)
        return Response({'data':serializer.errors},status=status.HTTP_200_OK)
    

class viewCart(GenericAPIView):
    serializer_class=CartSerializer

    def get(self,request):
        cart=Cart.objects.all()
        if (cart.count()>0):
            serializer=CartSerializer(cart,many=True)
            return Response({'data':serializer.data,'message':'cart viewed','success':True},status=status.HTTP_200_OK)
        else:
            return Response({'data':'no data available'},status=status.HTTP_400_BAD_REQUEST)
     
class viewSingleCart(GenericAPIView):
    
    def get(self, request, userid):
        queryset = Cart.objects.filter(userid=userid, cartstatus=0)  
        if queryset.exists():
            serializer = CartSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No items found in the cart'}, status=status.HTTP_404_NOT_FOUND)

class deleteCart(GenericAPIView):
    def delete(self, request,id):
        queryset=Cart.objects.get(pk=id)
        queryset.delete()
        return Response({'message':'deleted cart','success':True},status=status.HTTP_200_OK)
    
class wishList(GenericAPIView):
    serializer_class = WishlistSerializer

    def post(self, request):
        productid = request.data.get('productid')
        userid = request.data.get('userid')
        wishliststatus=1

        wishlist = Wishlist.objects.filter(productid=productid, userid=userid)

        if wishlist.exists():
            wishlist.delete()
            return Response({'message': 'item already exits', 'success': True}, status=status.HTTP_200_OK)
        productdata = Product.objects.filter(id=productid).first()
        if not productdata:
            return Response({'message': 'Product not found', 'success': False}, status=status.HTTP_400_BAD_REQUEST)

        productname = productdata.productname
        price = productdata.price
        image = productdata.image

        serializer = self.serializer_class(data={
            'productid': productid,
            'userid': userid,
            'productname': productname,
            'wishliststatus':wishliststatus,
            'price': price,
            'image': image
            
        })

        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data, 'message': 'Added to wish list successfully', 'success': True}, status=status.HTTP_200_OK)

        return Response({'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    

class viewWishlist(GenericAPIView):
    serializer_class = WishlistSerializer

    def get(self, request, userid):
        wishlist_items = Wishlist.objects.filter(userid=userid, Wishliststatus=1)

        if wishlist_items.exists():
            serializer = self.serializer_class(wishlist_items, many=True)
            return Response({'data': serializer.data, 'success': True}, status=status.HTTP_200_OK)

        return Response({'message': 'No items in wishlist', 'success': False}, status=status.HTTP_200_OK)


class order(GenericAPIView):
    serializer_class = OrderSerializer

    def post(self, request, userid):
        cart_items = Cart.objects.filter(userid=userid, cartstatus=0)

        if cart_items.exists():
            orders = []
            with transaction.atomic():
                for item in cart_items:
                    # Ensure image is taken from request.FILES for file handling
                    image = request.FILES.get('image') if 'image' in request.FILES else item.image

                    order_data = {
                        'productid': item.productid,
                        'productname': item.productname,
                        'image': image,  # Image file or previous image URL
                        'userid': item.userid,
                        'price': item.price,
                        'quantity': item.quantity
                    }

                    serializer = self.serializer_class(data=order_data)
                    if serializer.is_valid():
                        serializer.save()
                        orders.append(serializer.data)
                    else:
                        return Response({'data': serializer.errors, 'message': 'Error saving order'}, status=status.HTTP_400_BAD_REQUEST)

                cart_items.delete()

            return Response({'orders': orders, 'message': 'Order placed successfully', 'success': True}, status=status.HTTP_200_OK)

        else:
            return Response({'message': 'No items in the cart', 'success': False}, status=status.HTTP_400_BAD_REQUEST)
        

class viewOrder(GenericAPIView):
    serializer_class=OrderSerializer

    def get(self,request,userid):
        order=Order.objects.filter(userid=userid)
        if (order.count()>0):
            serializer=OrderSerializer(order,many=True)
            return Response({'data':serializer.data,'message':'order viewed','success':True},status=status.HTTP_200_OK)
        else:
            return Response({'data':'no data available'},status=status.HTTP_400_BAD_REQUEST)
        
class Addaddress_api(GenericAPIView):
    serializer_class = AddressSerializer    

    def post(self, request):
        # Extracting data from the request
        userid = request.data.get('userid')
        name = request.data.get('name')
        street = request.data.get('street')
        city = request.data.get('city')
        state = request.data.get('state')
        country = request.data.get('country')
        postal_code = request.data.get('postal_code')

        # Check if an address already exists for the given userid
        if Address.objects.filter(userid=userid).exists():
            return Response({'error': 'Address already exists for this user'}, status=status.HTTP_400_BAD_REQUEST)

        # Creating an address instance
        address_data = {
            'userid': userid,
            'name': name,
            'street': street,
            'city': city,
            'state': state,
            'country': country,
            'postal_code': postal_code,
        }

        # Serialize the data
        serializer = self.serializer_class(data=address_data)

        # Validate the serializer
        if serializer.is_valid():
            # Save the new address
            serializer.save()
            return Response({'data': serializer.data, 'message': 'Address added successfully', 'success': True}, status=status.HTTP_201_CREATED)
        else:
            # If serializer is invalid, return errors
            return Response({'errors': serializer.errors, 'success': False}, status=status.HTTP_400_BAD_REQUEST)

class viewalladdress_api(GenericAPIView):
    serializer_class = AddressSerializer

    def get(self, request):
        
            # Fetch the address for the given userid
        address = Address.objects.all()
        if (address.count()>0):
              serializer=AddressSerializer(address,many=True)
              return Response({'data': serializer.data, 'message': 'Address retrieved successfully', 'success': True}, status=status.HTTP_200_OK)
        return Response({'error': 'Address not found for this user', 'success': False}, status=status.HTTP_404_NOT_FOUND)

        
class UpdateAddress_api(GenericAPIView):
 
    serializer_class=AddressSerializer
    def put(self,request,userid):
      result=Address.objects.get(userid=userid)
      serializer=AddressSerializer(instance = result,data=request.data,partial=True)
      if serializer.is_valid():
        serializer.save()
        return Response({'data':serializer.data,'message':'updated successfully'},status=status.HTTP_200_OK)
      else:
        return Response({'data':'not uodated'})
      
class DeleteAddress_api(GenericAPIView):
  def delete(self,request,userid):
    result=Address.objects.get(pk=userid)
    result.delete()
    return Response({"message": "User deleted successfully"}, status=status.HTTP_200_OK)
  
class search_api(GenericAPIView):
    serializer_class = ProductSerializer

    def post(self, request):
        search_query = request.data.get('search_query', '')
        if search_query:
        
            products = Product.objects.filter(Q(productname__exact=search_query))
            if not products:
                return Response({'message': 'No products found'}, status=status.HTTP_404_NOT_FOUND)
            
            serializer = self.serializer_class(products, many=True)
            for product in serializer.data:
                if product['image']:
                    product['image'] = settings.MEDIA_URL + product['image']
            
            return Response({'data': serializer.data, 'message': 'Image fetched successfully'}, status=status.HTTP_200_OK)
        
        return Response({'message': 'No query found'}, status=status.HTTP_400_BAD_REQUEST)
    

    def get(self, request):
     search_query = request.query_params.get('search_query', '')
     print(search_query)  
     if search_query:
        products = Product.objects.filter(
            Q(productname__icontains=search_query)
        ).values('productname').distinct()[:10]

        if not products.exists(): 
            return Response({'Message': 'no suggestions found'}, status=status.HTTP_400_BAD_REQUEST)

        suggestion_list = [{'product_name': product['productname']} for product in products]

        return Response({'suggestion': suggestion_list, 'message': 'suggestions fetched successfully', 'success': True}, status=status.HTTP_200_OK)

     return Response({'error': 'no search query provided', 'success': False}, status=status.HTTP_400_BAD_REQUEST)
    
class change_pass_api(GenericAPIView):
   serializer_class=LoginSerializer
   def put(self,request,id):
      try:
         user=Login.objects.get(pk=id)
      except Login.DoesNotExist:
         return Response({'message':'user not found'},status=status.HTTP_400_BAD_REQUEST)
      serializer=self.serializer_class(user,data=request.data,partial=True)
      if serializer.is_valid():
         new_password=serializer.validated_data.get('password')
         if new_password:
            user.password=new_password
            user.save()
            return Response({'Message':'password updated successfully'},status=status.HTTP_200_OK)
         else:
            return Response({'Message':'no password provided'},status=status.HTTP_400_BAD_REQUEST) 
      return Response({'Message':'password updated successfully','errors':serializer.errors},status=status.HTTP_400_BAD_REQUEST)  