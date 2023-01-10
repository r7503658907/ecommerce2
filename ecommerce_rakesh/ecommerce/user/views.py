from .serializers import *
from rest_framework.views import APIView
from django.http import JsonResponse
from .models import *
import random
import string
from rest_framework.response import Response
import ast
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from pathlib import Path
import requests



class userSignup(APIView):
    def post(self, request):
        serializer = signupSerializer(data=request.data)
        try:
            if serializer.is_valid():
                try:
                    name = serializer.data["name"]
                    mobile = serializer.data["mobile"]
                    password=serializer.data["password"]
                    email = serializer.data['email']

                    User.objects.create_user(
                        username=str(mobile),
                        email=email,
                        first_name = name,
                        password= password)

                    return JsonResponse({
                        'status': 200,
                        'message': 'Registration Successfully',
                    })
                except Exception as e:
                    name = serializer.data['name']
                    mobile = serializer.data['mobile']
                    password = serializer.data["password"]

                    User.objects.create_user(
                        username=str(mobile),
                        first_name=name,
                        password=password
                    )

                    return JsonResponse({
                        'status': 200,
                        'message': 'register successfully',
                    })
            return JsonResponse({
                "status": 400,
                "message": serializer.errors
            })
        except Exception as e:
            print(str(e))
            return JsonResponse({
                'status': 400,
                'message': 'Something Went Wrong',
                'error': str(e)
            })

class PostaddressData(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = AddressTableSerializer(data=request.data)
        try:
            if serializer.is_valid():
                address = serializer.data['address']
                nikeName= serializer.data["nikeName"]

                data =User.objects.filter(username=request.user).values()[0]["id"]
                AddressTable.objects.create(
                    user_id = data,
                    address= address,
                    nikeName=nikeName,
                )

                return JsonResponse({
                    'status': 200,
                    'message': 'Address create successfully',
                })
            return JsonResponse({
                "status": 400,
                "message": serializer.errors
            })
        except Exception as e:
            print(str(e))
            return JsonResponse({
                'status': 400,
                'message': 'Something Went Wrong',
                'error': str(e)
            })

class getAddressData(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            data =AddressTable.objects.filter().values()
            print(data)

            return Response({
                'status': 200,
                'data': data
            })

        except Exception as e:
            return Response({
                'status': 400,
                'message': 'Something went wrong',
                'errors': str(e)
            })

class getAddressDataID(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request,addressId):
        try:
            data =AddressTable.objects.filter(addressId=addressId).values()
            print(data)

            return Response({
                'status': 200,
                'data': data
            })

        except Exception as e:
            return Response({
                'status': 400,
                'message': 'Something went wrong',
                'errors': str(e)
            })


class postAddressDelete(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = DeleteAddressTableSerializer(data=request.data)
        try:
            if serializer.is_valid():
                addressId = serializer.data['addressId']

                data =User.objects.filter(username=request.user).values()[0]["id"]
                AddressTable.objects.filter(
                    user_id = data,
                    addressId= addressId,
                ).delete()

                return JsonResponse({
                    'status': 200,
                    'message': 'Address delete successfully',
                })
            return JsonResponse({
                "status": 400,
                "message": serializer.errors
            })
        except Exception as e:
            print(str(e))
            return JsonResponse({
                'status': 400,
                'message': 'Something Went Wrong',
                'error': str(e)
            })

class updateAddress(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = UpdateAddressTableSerializer(data=request.data)
        try:
            if serializer.is_valid():
                addressType = serializer.data['addressType']
                address = serializer.data['address']
                addressId=serializer.data['addressId']
                data =User.objects.filter(username=request.user).values()[0]["id"]
                AddressTable.objects.filter(
                    user_id = data,
                    addressId=addressId,
                ).update(address=address,addressType=addressType)

                return JsonResponse({
                    'status': 200,
                    'message': 'Address update successfully',
                })
            return JsonResponse({
                "status": 400,
                "message": serializer.errors
            })
        except Exception as e:
            print(str(e))
            return JsonResponse({
                'status': 400,
                'message': 'Something Went Wrong',
                'error': str(e)
            })

class PostOrderData(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = OrderTableSerializer(data=request.data)
        try:
            if serializer.is_valid():
                orderData = serializer.data['orderData']
                totalAmount = serializer.data["totalAmount"]

                data =User.objects.filter(username=request.user).values()[0]["id"]

                orderId = 'order' + ''.join(
                    random.choices(string.digits + string.ascii_letters, k=random.randint(10, 14)))

                OrderTable.objects.create(
                    orderId=orderId,
                    user_id = data,
                    orderData=orderData,
                    totalAmount=totalAmount,
                )

                return JsonResponse({
                    'status': 200,
                    'message': 'order create successfully',
                })
            return JsonResponse({
                "status": 400,
                "message": serializer.errors
            })
        except Exception as e:
            print(str(e))
            return JsonResponse({
                'status': 400,
                'message': 'Something Went Wrong',
                'error': str(e)
            })


class getOrderData(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            data =OrderTable.objects.filter().values()
            print(data)

            return Response({
                'status': 200,
                'data': data
            })

        except Exception as e:
            return Response({
                'status': 400,
                'message': 'Something went wrong',
                'errors': str(e)
            })


class postCategory(APIView):
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        try:
            if serializer.is_valid():
                category_name = serializer.data['category_name']

                Category.objects.create(
                    category_name=category_name
                )
                return JsonResponse({
                    'status': 200,
                    'message': 'Category  create successfully',
                })
            return JsonResponse({
                "status": 400,
                "message": serializer.errors
            })

        except Exception as e:
            print(str(e))
            return JsonResponse({
                'status': 400,
                'message': 'Something Went Wrong',
                'error': str(e)
            })

class getCategorys(APIView):
    def get(self, request, ):
        try:
            data = list(Category.objects.filter().values())
            return Response({
                'status': 200,
                'data': data
            })

        except Exception as e:
            return Response({
                'status': 400,
                'message': 'Something went wrong',
                'errors': str(e)
            })

class postSubCategory(APIView):
    def post(self, request):
        serializer = SubCategorySerializer(data=request.data)
        try:
            if serializer.is_valid():
                subCategoryName= serializer.data["subCategoryName"]
                category_name=serializer.data["category_name"]

                data = Category.objects.filter(category_name=category_name).values()[0]["categoryId"]

                SubCategory.objects.create(
                    categoryId_id=data,
                    subCategoryName=subCategoryName
                )
                return JsonResponse({
                    'status': 200,
                    'message': 'subCategory  create successfully',
                })
            return JsonResponse({
                "status": 400,
                "message": serializer.errors
            })

        except Exception as e:
            print(str(e))
            return JsonResponse({
                'status': 400,
                'message': 'Something Went Wrong',
                'error': str(e)
            })

class getSubCategory(APIView):
    def get(self, request, ):
        try:
            data = list(SubCategory.objects.filter().values())
            return Response({
                'status': 200,
                'data': data
            })

        except Exception as e:
            return Response({
                'status': 400,
                'message': 'Something went wrong',
                'errors': str(e)
            })

class postProduct(APIView):
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        try:
            if serializer.is_valid():
                subCategoryName = serializer.data["subCategoryName"]
                productName= serializer.data["productName"]
                productPrice = serializer.data["productPrice"]
                brand = serializer.data["brand"]
                productImage = serializer.data["productImage"]
                productImage1 = serializer.data["productImage1"]
                productImage2 = serializer.data["productImage2"]
                productImage3 = serializer.data["productImage3"]
                productImage4 = serializer.data["productImage4"]
                productImage5 = serializer.data["productImage5"]
                productDescription= serializer.data["productDescription"]


                data = SubCategory.objects.filter(subCategoryName=subCategoryName).values()[0]["subCategoryId"]
                print(data)

                productId = 'product' + ''.join(
                    random.choices(string.digits + string.ascii_letters, k=random.randint(10, 14)))

                Product.objects.create(
                    productId=productId,
                    subCategoryId_id=data,
                    productName=productName,
                    productPrice=productPrice,
                    brand=brand,
                    productImage=productImage,
                    productImage1=productImage1,
                    productImage2=productImage2,
                    productImage3=productImage3,
                    productImage4=productImage4,
                    productImage5=productImage5,
                    productDescription=productDescription

                )
                return JsonResponse({
                    'status': 200,
                    'message': 'product  create successfully',
                })
            return JsonResponse({
                "status": 400,
                "message": serializer.errors
            })

        except Exception as e:
            print(str(e))
            return JsonResponse({
                'status': 400,
                'message': 'Something Went Wrong',
                'error': str(e)
            })

class getProduct(APIView):
    def get(self, request, ):
        try:
            data = list(Product.objects.filter().values())
            return Response({
                'status': 200,
                'data': data
            })

        except Exception as e:
            return Response({
                'status': 400,
                'message': 'Something went wrong',
                'errors': str(e)
            })
class postProfile(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = ProfileSerializer(data=request.data)
        try:
            if serializer.is_valid():
                name = serializer.data["name"]
                mobile = serializer.data["mobile"]
                email = serializer.data["email"]
                password = serializer.data["password"]

                data = User.objects.filter(username = request.user).values()[0]["id"]
                print(data)

                Profile.objects.create(
                    user_id=data,
                    name=name,
                    mobile=mobile,
                    email=email,
                    password=password,

                )
                return JsonResponse({
                    'status': 200,
                    'message': 'profile create successfully',
                })
            return JsonResponse({
                "status": 400,
                "message": serializer.errors
            })

        except Exception as e:
            print(str(e))
            return JsonResponse({
                'status': 400,
                'message': 'Something Went Wrong',
                'error': str(e)
            })
class getProfile(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, ):
        try:
            data = list(Profile.objects.filter().values())
            return Response({
                'status': 200,
                'data': data
            })

        except Exception as e:
            return Response({
                'status': 400,
                'message': 'Something went wrong',
                'errors': str(e)
            })


class updateProfile(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = UpdateProfileSerializer(data=request.data)
        try:
            if serializer.is_valid():
                name = serializer.data['name']
                mobile = serializer.data['mobile']
                password=serializer.data['password']
                data =User.objects.filter(username=request.user).values()[0]["id"]
                Profile.objects.filter(
                    user_id = data,
                ).update(name=name,mobile=mobile,password=password)

                return JsonResponse({
                    'status': 200,
                    'message': 'Profile update successfully',
                })
            return JsonResponse({
                "status": 400,
                "message": serializer.errors
            })
        except Exception as e:
            print(str(e))
            return JsonResponse({
                'status': 400,
                'message': 'Something Went Wrong',
                'error': str(e)
            })

class postWishlist(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = WishlistSerializer(data=request.data)
        try:
            if serializer.is_valid():
                wishlistData = serializer.data["wishlistData"]
                data = User.objects.filter(username = request.user).values()[0]["id"]
                print(data)

                Wishlist.objects.create(
                    user_id=data,
                    wishlistData=wishlistData,
                    status=0,
                )
                return JsonResponse({
                    'status': 200,
                    'message': 'Wishlist create successfully',
                })
            return JsonResponse({
                "status": 400,
                "message": serializer.errors
            })

        except Exception as e:
            print(str(e))
            return JsonResponse({
                'status': 400,
                'message': 'Something Went Wrong',
                'error': str(e)
            })

class StatusUpdateWishlist(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        serializer = StatusUpadateWishlistSerializer(data=data)
        if serializer.is_valid():
            wishlist = serializer.data['wishlist']
            status=serializer.data["status"]
            Wishlist.objects.filter(wishlist=wishlist).update(status=status)

            return Response({
                'status': 200,
                'message': "Status update WishList"
            })
        return Response({
            'status': 400,
            'message': 'Something went wrong',
            'data': serializer.errors
        })


class DeleteWishlist(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        serializer = StatusDeleteAddToCartSerializer(data=data)
        if serializer.is_valid():
            wishlist = serializer.data['wishlist']
            Wishlist.objects.filter(wishlist=wishlist).delete()

            return Response({
                'status': 200,
                'message': "Status Delete Product WishList"
            })
        return Response({
            'status': 400,
            'message': 'Something went wrong',
            'data': serializer.errors
        })


class getWishlist(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, ):
        try:
            data = list(Wishlist.objects.filter().values())
            return Response({
                'status': 200,
                'data': data
            })

        except Exception as e:
            return Response({
                'status': 400,
                'message': 'Something went wrong',
                'errors': str(e)
            })



class postAddToCart(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = AddToCartSerializer(data=request.data)
        try:
            if serializer.is_valid():
                AddToCartData = serializer.data["AddToCartData"]
                data = User.objects.filter(username = request.user).values()[0]["id"]
                print(data)

                AddToCart.objects.create(
                    user_id=data,
                    AddToCartData=AddToCartData,
                    status=0,
                )
                return JsonResponse({
                    'status': 200,
                    'message': 'Save Cart successfully',
                })
            return JsonResponse({
                "status": 400,
                "message": serializer.errors
            })

        except Exception as e:
            print(str(e))
            return JsonResponse({
                'status': 400,
                'message': 'Something Went Wrong',
                'error': str(e)
            })

class getAddToCart(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, ):
        try:
            data = list(AddToCart.objects.filter().values())
            return Response({
                'status': 200,
                'data': data
            })

        except Exception as e:
            return Response({
                'status': 400,
                'message': 'Something went wrong',
                'errors': str(e)
            })

class StatusUpdateAddToCart(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        serializer = StatusUpadateAddToCartSerializer(data=data)
        if serializer.is_valid():
            AddToCartId = serializer.data['AddToCartId']
            status=serializer.data["status"]
            AddToCart.objects.filter(AddToCartId=AddToCartId).update(status=status)

            return Response({
                'status': 200,
                'message': "Status update Add to cart"
            })
        return Response({
            'status': 400,
            'message': 'Something went wrong',
            'data': serializer.errors
        })

class DeleteAddToCart(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        serializer = StatusdeleteAddToCartSerializer(data=data)
        if serializer.is_valid():
            AddToCartId = serializer.data['AddToCartId']
            AddToCart.objects.filter(AddToCartId=AddToCartId).delete()

            return Response({
                'status': 200,
                'message': " Delete Product Add To Cart"
            })
        return Response({
            'status': 400,
            'message': 'Something went wrong',
            'data': serializer.errors
        })

class postRatingAndReview(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = RatingAndReviewSerializer(data=request.data)
        try:
            if serializer.is_valid():
                productName = serializer.data["productName"]
                rating = serializer.data["rating"]
                review = serializer.data["review"]
                data = User.objects.filter(username = request.user).values()[0]["id"]
                orderData = OrderTable.objects.filter(user_id= data).values()[0]["orderId"]

                RatingAndReview.objects.create(
                    user_id=data,
                    orderId_id=orderData,
                    productName=productName,
                    rating=rating,
                    review=review,

                )
                return JsonResponse({
                    'status': 200,
                    'message': 'rating and review create successfully',
                })
            return JsonResponse({
                "status": 400,
                "message": serializer.errors
            })

        except Exception as e:
            print(str(e))
            return JsonResponse({
                'status': 400,
                'message': 'Something Went Wrong',
                'error': str(e)
            })

class getRatingAndReview(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, ):
        try:
            data = list(RatingAndReview.objects.filter().values())
            return Response({
                'status': 200,
                'data': data
            })

        except Exception as e:
            return Response({
                'status': 400,
                'message': 'Something went wrong',
                'errors': str(e)
            })


class postProductDetail(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = ProductDetailSerializer(data=request.data)
        try:
            if serializer.is_valid():
                productId = serializer.data["productId"]
                productFeature=serializer.data["productFeature"]

                Data = Product.objects.filter(productId= productId).values()[0]["productId"]
                print(Data)

                ProductDetail.objects.create(

                    productId_id=Data,
                    productFeature=productFeature,

                )
                return JsonResponse({
                    'status': 200,
                    'message': 'product Detail successfully',
                })
            return JsonResponse({
                "status": 400,
                "message": serializer.errors
            })

        except Exception as e:
            print(str(e))
            return JsonResponse({
                'status': 400,
                'message': 'Something Went Wrong',
                'error': str(e)
            })

class getProductDetail(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, ):
        try:
            data = list(ProductDetail.objects.filter().values())
            for var in data:
                var["productFeature"] = ast.literal_eval(var["productFeature"])
            return Response({
                'status': 200,
                'data': data
            })

        except Exception as e:
            return Response({
                'status': 400,
                'message': 'Something went wrong',
                'errors': str(e)
            })



class searchfilter(APIView):
    def get(self, request,productName):
        try:

                data =list( Product.objects.filter(productName__icontains=productName).values())
                return JsonResponse({
                    'status': 200,
                    'data': data,
                })


        except Exception as e:
            print(str(e))
            return JsonResponse({
                'status': 400,
                'message': 'Something Went Wrong',
                'error': str(e)
            })





