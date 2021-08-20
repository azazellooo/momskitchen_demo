import json
from django.http import HttpResponse
from django.shortcuts import redirect, render
from KitchenWeb.models import Cart, Offering, Order, OrderOffernig
from accounts.models import Employee, UserToken
from accounts.tasks import create_json_portions


def cart_create(request, *args, **kwargs):
    body = request.body
    if body:
        parse_body = json.loads(body)
        position_in_json = parse_body['position']
        offering_id = parse_body['id']
        offering = Offering.objects.get(id=int(offering_id))
        user_token = UserToken.objects.get(key=request.session['token'])
        user = Employee.objects.get(user_token=user_token)
        try:
            garnish = parse_body['garnish']
        except:
            garnish = None
        try:
            additional = parse_body['additional']
        except:
            additional = None
        ready_json = create_json_portions(position_in_json, garnish, additional)
        if offering.qty_portion != 0:
            offering_portion = float(ready_json['Position']['portion'])
            total_qty_portions = float(offering.qty_portion)
            remainder = total_qty_portions - offering_portion
            offering.qty_portion = remainder
            offering.save()

            total_sum_price = int(ready_json['total_price'])
            ready_json.pop('total_price')
            json_var = ready_json

            try:
                total_sum_sup = 0
                cart = Cart.objects.filter(
                    offering=offering,
                    user=user,
                    portions=json_var,
                    is_confirmed=False
                )[0]
                cart.qty += 1
                for i in offering.supplement.all():
                    total_sum_sup += i.price
                cart.price = total_sum_price * cart.qty
                cart.price = cart.price + (total_sum_sup * cart.qty)
                cart.save()
                return HttpResponse('1')

            except:
                total_sum_sup2 = 0
                for i in offering.supplement.all():
                    total_sum_sup2 += i.price
                Cart.objects.create(
                    offering=offering,
                    user=user,
                    portions=json_var,
                    price=total_sum_price + total_sum_sup2
                )
                return HttpResponse('2')
        else:
            return HttpResponse('Dont have portions!')



def delete_view_cart(request, *args, **kwargs):
    cart = Cart.objects.get(id=kwargs.get('pk'))
    if cart.qty == 1:
        cart.delete()
        return redirect('kitchen:menu')
    else:
        cart.qty = cart.qty - 1
        cart.save()
        return redirect('kitchen:menu')


def search_off_in_cart_and_delete(request, *args, **kwargs):
    body = request.body
    if body:
        parse_body = json.loads(body)
        position = parse_body['position']
        offering = Offering.objects.get(id=int(parse_body['id']))
        try:
            garnish = parse_body['garnish']
        except:
            garnish = None
        try:
            additional = parse_body['additional']
        except:
            additional = None
        ready_json = create_json_portions(position, garnish, additional)
        offering_portion = float(ready_json['Position']['portion'])
        total_qty_portions = float(offering.qty_portion)
        remainder = total_qty_portions + offering_portion
        offering.qty_portion = remainder
        offering.save()
        total_price = int(ready_json['total_price'])
        for i in offering.supplement.all():
            total_price += i.price


        ready_json.pop('total_price')
        json_var = ready_json
        user_token = UserToken.objects.get(key=request.session['token'])
        user = Employee.objects.get(user_token=user_token)
        cart = Cart.objects.filter(
            offering=offering,
            user=user,
            portions=json_var
        )[0]
        if cart.qty > 1:
            cart.qty -= 1
            cart.price -= total_price
            cart.save()
            return HttpResponse('1')
        else:
            cart.delete()
            return HttpResponse('2')



def confirm_cart(request, *args, **kwargs):
    user_token = UserToken.objects.get(key=request.session['token'])
    user = Employee.objects.get(user_token=user_token)
    users_carts = Cart.objects.filter(user=user)
    users_carts.update(is_confirmed=True)
    order = Order.objects.create(
        user=user
    )
    for i in users_carts:
        OrderOffernig.objects.create(
            offering=i.offering,
            portions=i.portions,
            order=order,
            price=i.price,
            qty=i.qty
        )
    return render(request, 'basket/confirm.html')


























