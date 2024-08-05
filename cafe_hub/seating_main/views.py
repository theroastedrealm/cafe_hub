#seating_main/views.py
from django.shortcuts import render, redirect
from django.contrib import messages

from main.models import Branch


from .models import Seat
from .decorators import allowed_users

def homepage(request):
    branch = request.user.branch
    items = Seat.objects.filter(branch=branch).order_by('id')
    try:
        booked_seats = Seat.objects.filter(user=request.user,branch=branch)
        unavailable_seats = Seat.objects.filter(available=False, branch=branch).exclude(user=request.user)
    except:
        booked_seats = None
        unavailable_seats = None
    
    is_staff = request.user.groups.filter(name__in=['uber-user', 'admin']).exists()


    context = {
        "seats": items,
        "booked_seats": booked_seats,
        "is_staff": is_staff,
        "unavailable_seats": unavailable_seats
    }
    
    return render(request, "seating_main/home.html", context)


def update_seat_availability(request, seat_id):
    if request.user.is_authenticated:    
        if request.method == "POST":
            seat = Seat.objects.get(id=seat_id)
            if seat.available:
                seat.available = False
                seat.user = request.user
            else:
                seat.available = True
                seat.user = None
            seat.save()
            branch = request.user.branch
            items = Seat.objects.filter(branch=branch).order_by('id')
            return render(request, "seating_main/home.html", {"seats": items})
        else:
            messages(request, "You need to be logged in to book a seat")
            return redirect("/")
    branch = request.user.branch
    items = Seat.objects.filter(branch=branch).order_by('id')
    return render(request, "seating_main/home.html", {"seats": items})

@allowed_users(allowed_roles=["uber-user", "admin"])
def staffpage(request):
    branch = request.user.branch
    items = Seat.objects.filter(branch=branch).order_by('id')
    return render(request, "seating_main/staff.html", {"seats": items})

@allowed_users(allowed_roles=["uber-user", "admin"])
def staff_update_seat_availability(request, seat_id):
    branch = request.user.branch
    if request.method == "POST":
        seat = Seat.objects.get(id=seat_id)
        if seat.available:
            seat.available = False
            seat.user = None
        else:
            seat.available = True
            seat.user = None
        seat.save()
        items = Seat.objects.filter(branch=branch).order_by('id')
        return redirect("/seating/staff/")
    items = Seat.objects.filter(branch=branch).order_by('id')
    return render(request, "seating_main/staff.html", {"seats": items})


@allowed_users(allowed_roles=["uber-user", "admin"])
def staff_add_seat(request):
    branch = request.user.branch
    if request.method == "POST":
        seat_name = request.POST.get("seat_name")
        new_seat = Seat(name=seat_name, available=True, branch=branch)
        new_seat.save()
        items = Seat.objects.filter(branch=branch).order_by('id')
        return redirect("/seating/staff/")
    items = Seat.objects.filter(branch=branch).order_by('id')
    return render(request, "seating_main/staff.html", {"seats": items})

@allowed_users(allowed_roles=["uber-user", "admin"])
def staff_delete_seat(request, seat_id):
    branch = request.user.branch
    if request.method == "POST":
        seat = Seat.objects.get(id=seat_id)
        seat.delete()
        items = Seat.objects.filter(branch=branch).order_by('id')
        return redirect("/seating/staff/")
    
    items = Seat.objects.filter(branch=branch).order_by('id')
    return render(request, "seating_main/staff.html", {"seats": items})