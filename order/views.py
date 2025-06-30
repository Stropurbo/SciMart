from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from order.models import Cart, CartItem, Order, OderItem
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from order import serializers as Allsz
from rest_framework.decorators import action
from order.services import OrderServices
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from sslcommerz_lib import SSLCOMMERZ
from django.conf import settings as projectsetting
from rest_framework.views import APIView
class CartViewSet(CreateModelMixin,RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    serializer_class = Allsz.CartSerializer
    permission_classes = [IsAuthenticated]
        
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Cart.objects.none()
        return Cart.objects.prefetch_related('items__product').filter(user = self.request.user)
    
    def create(self, request, *args, **kwargs):
        existing_cart = Cart.objects.filter(user= request.user).first()
        if existing_cart:
            serializer = self.get_serializer(existing_cart)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return super().create(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        serializer.save(user = self.request.user)
        
class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch','delete']
    def get_serializer_class(self):
        if self.request.method == "POST":
            return Allsz.AddCartItemSerializer
        elif self.request.method == "PATCH":
            return Allsz.UpdateCartItemSerializer
        return Allsz.CartItemSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        if getattr(self, 'swagger_fake_view', False):
            return context
        return {'cart_id' : self.kwargs.get('cart_pk')}

    def get_queryset(self):
        return CartItem.objects.select_related('product').filter(cart_id = self.kwargs.get('cart_pk'))

class OrderViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        order = self.get_object()
        OrderServices.cancel_order(order=order, user=request.user)
        return Response({'status': 'Order Canceled'})
    
    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        order = self.get_object()
        serializer = Allsz.UpdateOrderSerializer(order, data = request.data, partial= True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'status': f'Order Status Updated to {request.data['status']}'})
            
    def get_permissions(self):
        if self.action in ['update_status', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action == "cancel":
            return Allsz.EmptySerializer
        if self.action == "create":
            return Allsz.CreateOrderSerializer
        elif self.action == "update_status":
            return Allsz.UpdateOrderSerializer
        return Allsz.OrderSerializer
    
    def get_serializer_context(self):
        return {'user_id': self.request.user.id, "user": self.request.user}

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Order.objects.none()
        if self.request.user.is_staff:
            return Order.objects.prefetch_related('items__product').all()
        return Order.objects.prefetch_related('items__product').filter(user = self.request.user)
    

class HasOrderProduct(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, product_id):
        user = request.user
        has_ordered = OderItem.objects.filter(order__user=user, product_id=product_id).exists()
        return Response({"hasOrder": has_ordered})
    

@api_view(['POST'])
def initiate_payment(request): 
    print(request.data)

    user = request.user
    amount = request.data.get('amount')
    order_id = request.data.get('orderId')
    num_item = request.data.get('numItem')

    print("user", user)

    settings = { 'store_id': 'scima681483cc6db1a', 
                'store_pass': 'scima681483cc6db1a@ssl', 
                'issandbox': True 
                }
    sslcz = SSLCOMMERZ(settings)
    post_body = {}
    post_body['total_amount'] = amount
    post_body['currency'] = "BDT"
    post_body['tran_id'] = f"txn_{order_id}"
    post_body['success_url'] = f"{projectsetting.BACKEND_URL}/api/v1/payment/success/"
    post_body['fail_url'] = f"{projectsetting.BACKEND_URL}/api/v1/payment/fail/"
    post_body['cancel_url'] = f"{projectsetting.BACKEND_URL}/api/v1/payment/cancel/"
    post_body['emi_option'] = 0
    post_body['cus_name'] = f"{user.first_name} {user.last_name}"
    post_body['cus_email'] = user.email
    post_body['cus_phone'] = user.phone_number
    post_body['cus_add1'] = user.address
    post_body['cus_city'] = "Dhaka"
    post_body['cus_country'] = "Bangladesh"
    post_body['shipping_method'] = "NO"
    post_body['multi_card_name'] = ""
    post_body['num_of_item'] = num_item
    post_body['product_name'] = "E-Commarce"
    post_body['product_category'] = "General"
    post_body['product_profile'] = "general"

    response = sslcz.createSession(post_body) # API response
    print(response)

    if response.get("status") == 'SUCCESS':
        return Response({'payment_url': response['GatewayPageURL']})
    return Response({'error': 'payment initiate failed.'})

@api_view(["POST"])
def payment_success(request):
    try:
        tran_id = request.data.get("tran_id")  

        if not tran_id or "_" not in tran_id:
            return redirect(f"/dashboard/orders")

        order_id = tran_id.split('_')[1]  

        order = Order.objects.get(id=order_id)
        order.status = "Ready To Ship"  
        order.save()

    except Order.DoesNotExist:
        print("Order not found")

    return redirect(f"{projectsetting.FRONTEND_URL}/dashboard/orders")

@api_view(["POST"])
def payment_cancel(request):
    return redirect(f"{projectsetting.FRONTEND_URL}/dashboard/orders")

@api_view(["POST"])
def payment_fail(request):
    return redirect(f"{projectsetting.FRONTEND_URL}/dashboard/orders")
