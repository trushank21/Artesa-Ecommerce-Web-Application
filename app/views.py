from django.shortcuts import redirect, render
from django.views import View
from app.models import (Customer,
                        Product,
                        Cart,
                        OrderPlaced,ContactUs)
from app.forms import CustomerRegistrationForm,CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# def home(request):
#     return render(request, 'app/home.html')
class ProductView(View):
    def get(self,request):
        all=Product.objects.all()
        topwears=Product.objects.filter(category='TW')
        bottomwears=Product.objects.filter(category='BW')
        mobiles=Product.objects.filter(category='M')
        category_classes = {
            'TW': 'topwears',
            'M': 'mobiles',
            'BW': 'bottomwears',
        }
        hm="bg-danger text-light p-2 card"
        return render(request,'app/home.html',{'all':all,'topwears':topwears,'bottomwears':bottomwears,'mobiles':mobiles,'category_classes': category_classes,'hm':hm})


def contact(request):
    if request.method=='POST':
        your_name=request.POST['your_name']
        email_address=request.POST['email_address']
        message=request.POST['message']

        usr=ContactUs(your_name=your_name,email_address=email_address,message=message)
        usr.save()
        save='save'
        return JsonResponse({'status':save})
    ct="bg-danger text-light p-2 card"
    return render(request,'app/contact.html',{'ct':ct})

# def product_detail(request):
#     return render(request, 'app/productdetail.html')

class ProductDetailView(View):
    def get(self,request,pk):
        product=Product.objects.get(pk=pk)
        item_already_in_cart=False
        if request.user.is_authenticated:
            item_already_in_cart=Cart.objects.filter(product=product,user=request.user).exists()
        return render(request,'app/productdetail.html',{'product':product,'item_already_in_cart':item_already_in_cart})

@login_required
def add_to_cart(request):
    user=request.user
    product_id=request.GET.get('prod_id')
    product=Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect('/cart')

@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user=request.user
        cart=Cart.objects.filter(user=user)
        amount=0.0
        shipping_amount=70.0

        if cart:
            for p in cart:
                amount+=p.quantity*p.product.discounted_price
            total_amount=amount+shipping_amount
            return render(request, 'app/addtocart.html',{'carts':cart,'total_amount':total_amount,'amount':amount})
        else:
            return render(request,'app/emptycart.html')
        
# def empty_cart(request):
#     return render(request,'app/emptycart.html')

def plus_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()

        cart=Cart.objects.filter(user=request.user)
        amount=0.0
        shipping_amount=70.0
        
        for p in cart:
            amount+=p.quantity*p.product.discounted_price
        total_amount=amount+shipping_amount

        data={'quantity':c.quantity,'amount':amount,'total_amount':total_amount}
        return JsonResponse(data)


def minus_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        # c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c = Cart.objects.get(Q(product_id=prod_id) & Q(user=request.user))

        c.quantity-=1
        c.save()

        cart=Cart.objects.filter(user=request.user)
        amount=0.0
        shipping_amount=70.0
        
        for p in cart:
            amount+=p.quantity*p.product.discounted_price
        total_amount=amount+shipping_amount

        visibility="block"
        if amount==0:
            visibility="none"

        data={'quantity':c.quantity,'amount':amount,'total_amount':total_amount,'visi':visibility}
        return JsonResponse(data)

def remove_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()

        cart = Cart.objects.filter(user=request.user)
        amount = sum(p.quantity * p.product.discounted_price for p in cart)
        shipping_amount = 70.0
        total_amount = amount + shipping_amount

        cart_count = cart.count()

        data = {
            'amount': amount,
            'total_amount': total_amount,
            'cart_count': cart_count
        }
        return JsonResponse(data)







@login_required
def buy_now(request, pk):
    product = Product.objects.get(id=pk)
    add = Customer.objects.filter(user=request.user)

    amount = product.discounted_price
    shipping_amount = 70
    total_amount = amount + shipping_amount

    return render(request, 'app/buynow.html', {
        'product': product,
        'add': add,
        'amount': amount,
        'shipping_amount': shipping_amount,
        'total_amount': total_amount
    })

@login_required
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    buy_prod = request.GET.get('buyprod')

    customer = Customer.objects.get(id=custid)

    # ---------------------------
    # BUY NOW FLOW
    # ---------------------------
    if buy_prod:
        product = Product.objects.get(id=buy_prod)

        OrderPlaced.objects.create(
            user=user,
            customer=customer,
            product=product,
            quantity=1
        )
        return redirect('orders')

    # ---------------------------
    # NORMAL CART CHECKOUT
    # ---------------------------
    cart_items = Cart.objects.filter(user=user)
    for c in cart_items:
        OrderPlaced.objects.create(
            user=user,
            customer=customer,
            product=c.product,
            quantity=c.quantity
        )
        c.delete()

    return redirect('orders')



# def profile(request):
#     return render(request, 'app/profile.html')

@login_required
def address(request):
    add=Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html',{'add':add,'active':'btn-primary'})

@login_required
def orders(request):
    od="bg-danger text-light p-2 card"
    op=OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html',{'order_placed':op,'od':od})


# def change_password(request):
#     return render(request, 'app/changepassword.html')





# def login(request):
#     return render(request, 'app/login.html')


# def customerregistration(request):
#     return render(request, 'app/customerregistration.html')


class CustomerRegistrationView(View):
    def get(self,request):
        form=CustomerRegistrationForm()
        return render(request,'app/customerregistration.html',{'form':form})
    def post(self,request):
        form=CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request,'Registration Successfull')
            form.save()
        return render(request,'app/customerregistration.html',{'form':form})

@login_required
def checkout(request):
    user=request.user
    add=Customer.objects.filter(user=user)
    print(add)
    cart_items=Cart.objects.filter(user=user)
    amount=0.0
    shipping_amount=70.0
    
    for p in cart_items:
        amount+=p.quantity*p.product.discounted_price
    total_amount=amount+shipping_amount
    return render(request, 'app/checkout.html',{'add':add,'total_amount':total_amount,'cart_items':cart_items})

# @login_required
# def payment_done(request):
#     user=request.user
#     custid=request.GET.get('custid')
#     customer=Customer.objects.get(id=custid)
#     cart=Cart.objects.filter(user=user)
#     for c in cart:
#         OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity).save()
#         c.delete()
#     return redirect("orders")


@method_decorator(login_required,name='dispatch')
class ProfileView(View):
    def get(self,request):
        form=CustomerProfileForm()
        return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})
    def post(self,request):
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            usr=request.user
            name=form.cleaned_data['name']
            locality=form.cleaned_data['locality']
            city=form.cleaned_data['city']
            state=form.cleaned_data['state']
            zipcode=form.cleaned_data['zipcode']
            reg=Customer(user=usr,name=name,locality=locality,city=city,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,'Profile Updated Successfully')
        return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})
            
@login_required
def shop(request):
    all=Product.objects.all()
    topwears=Product.objects.filter(category='TW')
    bottomwears=Product.objects.filter(category='BW')
    mobiles=Product.objects.filter(category='M')
    category_classes = {
            'TW': 'topwears',
            'M': 'mobiles',
            'BW': 'bottomwears',
        }
    sp="bg-danger text-light p-2 card"
    return render(request,'app/shop.html',{'all':all,'sp':sp,'topwears':topwears,'bottomwears':bottomwears,'mobiles':mobiles,'category_classes':category_classes})


@login_required
def topwears(request):
    tp="bg-danger text-light p-2 card"
    topwears=Product.objects.filter(category='TW')
    category_classes = {
            'TW': 'topwears',
        }
    return render(request,'app/topwears.html',{'tp':tp,'category_classes':category_classes,'topwears':topwears})

@login_required
def mobile(request,data=None):
    m="bg-danger text-light p-2 card"
    mobiles=Product.objects.filter(category='M')
    category_classes = {
            'M': 'mobiles',
        }
    return render(request,'app/mobile.html',{'m':m,'category_classes':category_classes,'mobiles':mobiles})

@login_required
def bottomwears(request,data=None):
    bw="bg-danger text-light p-2 card"
    bottomwears=Product.objects.filter(category='BW')
    category_classes = {
            'M': 'bottomwears',
        }
    return render(request,'app/bottomwears.html',{'bw':bw,'category_classes':category_classes,'bottomwears':bottomwears})



