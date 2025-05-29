from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status, generics, permissions, pagination
from rest_framework.views import APIView
from .serializers import ProductSerializer, CartItemSerializer, AddToCartSerializer, UpdateQuantitySerializer, CartTotalSerializer
from cart.models import CartItem, Product
from rest_framework.pagination import PageNumberPagination

# Create your views here.
class ProductListView(generics.ListAPIView):
    """
    View to List all products
    permissions: 
     - AllowAny: Accessible without authentication.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]

class ProductCreateView(generics.CreateAPIView):
    """
    view to create a new product

    permissions:
    - IsAdmin: only admin users can create products
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAdminUser]

class ProductRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """
    View to retrieve, update, or delete a specific product by ID.
    Methods:
        - GET: Retrieve a product by ID.
        - PUT/PATCH: Update a product by ID.
        - DELETE: Delete a product by ID.
    Permissions:
        - IsAdminUser: Only admin users can perform these actions.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = 'id'

class AddViewCart(APIView):
    """
    view to list and add items to cart

    Methods:
        - GET: List cart items for the current user (paginated).
        - POST: Add a product to the cart or increment quantity if already exists.
    
    Permissions:
        - IsAuthenticated: User must be logged in.
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        Retrieve a paginated list of the current user's cart items.

        """
        cart_items = CartItem.objects.filter(user=request.user)

        paginator = PageNumberPagination()
        paginator.page_size = 5
        paginated_items = paginator.paginate_queryset(cart_items, request)

        serializer = CartItemSerializer(paginated_items, many=True)

        return paginator.get_paginated_response(serializer.data)
    
    def post(self, request):
        """
        Add a product to the cart or increment quantity if product already exists.

        Request Body:
            {
                "product_id": <int>
            }

        """
        serializer = AddToCartSerializer(data=request.data)
        

        if serializer.is_valid():
            product_id = serializer.validated_data['product_id']

            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return Response({"error":"Product not found"}, status=status.HTTP_404_NOT_FOUND)
            
            cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)

            if not created:
                cart_item.quantity += 1
                cart_item.save()

            response_serializer = CartItemSerializer(cart_item)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UpdateDeleteCartItemView(APIView):
    """
    View to update quantity or delete a cart item.

    Methods:
        - PUT: Update quantity of a cart item.
        - DELETE: Remove a cart item.

    Permissions:
        - IsAuthenticated: User must be logged in.
    """

    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, id):
        """
        Update the quantity of a specific cart item.

        Path Params:
            id (int): ID of the cart item.

        Request Body:
            {
                "quantity": <int>
            }

        """
        serializer = UpdateQuantitySerializer(data=request.data)

        if serializer.is_valid():
            try:
                cart_item = CartItem.objects.get(id=id, user=request.user)
                cart_item.quantity = serializer.validated_data['quantity']
                cart_item.save()

                response_serializer = CartItemSerializer(cart_item)
                return Response(response_serializer.data, status=status.HTTP_200_OK)
            except CartItem.DoesNotExist:
                return Response({"error": "Cart item not found"}, status=status.HTTP_404_NOT_FOUND)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        """
        Delete a specific cart item by ID.

        Path Params:
            id (int): ID of the cart item.

        """
        try:
            cart_item = CartItem.objects.get(id=id, user=request.user)
            cart_item.delete()

            return Response({"message":"Cart item deleted successfully"}, status=status.HTTP_200_OK)
        except CartItem.DoesNotExist:
            return Response({"error":"Cart item not found"}, status=status.HTTP_404_NOT_FOUND)
        
class ClearCartView(APIView):
    """
    View to clear all items in the user's cart.

    Methods:
        - DELETE: Remove all items from the cart.

    Permissions:
        - IsAuthenticated: User must be logged in.
    """

    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        """
        Clear all items in the user's cart.

        """

        CartItem.objects.filter(user=request.user).delete()

        return Response({"message":"cart cleared"}, status=status.HTTP_204_NO_CONTENT)

class CartTotalView(APIView):
    """
    View to get total cart price and item count.

    Methods:
        - GET: Calculate and return total cart price and number of items.

    Permissions:
        - IsAuthenticated: User must be logged in.
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        Get the total price and number of items in the user's cart.

        """
         
        cart_items = CartItem.objects.filter(user=request.user)

        cart_total = sum(item.total_price() for item in cart_items)
        item_count = cart_items.count()

        serializer = CartTotalSerializer({
            'cart_total': cart_total,
            'item_count': item_count
        }) 

        return Response(serializer.data)      

        
    