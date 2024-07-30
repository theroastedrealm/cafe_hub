from django.shortcuts import render, redirect
from django.contrib import messages


from .models import Seat
from .decorators import allowed_users

def homepage(request, branch_id):
    items = Seat.objects.filter(branch=branch_id)
    try:
        booked_seats = Seat.objects.filter(user=request.user)
        unavailable_seats = Seat.objects.filter(available=False, branch=branch_id).exclude(user=request.user)
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
            return redirect("/seating")
        else:
            messages(request, "You need to be logged in to book a seat")
            return redirect("/")
    return render(request, "seating_main/home.html", {"seats": Seat.objects.all()})

@allowed_users(allowed_roles=["uber-user", "admin"])
def staffpage(request):
    items = Seat.objects.all()
    return render(request, "seating_main/staff.html", {"seats": items})

@allowed_users(allowed_roles=["uber-user", "admin"])
def staff_update_seat_availability(request, seat_id):
    if request.method == "POST":
        seat = Seat.objects.get(id=seat_id)
        if seat.available:
            seat.available = False
            seat.user = None
        else:
            seat.available = True
            seat.user = None
        seat.save()
        return redirect("/seating/staff/")
    return render(request, "seating_main/staff.html", {"seats": Seat.objects.all()})


@allowed_users(allowed_roles=["uber-user", "admin"])
def staff_add_seat(request):
    if request.method == "POST":
        seat_name = request.POST.get("seat_name")
        new_seat = Seat(name=seat_name, available=True)
        new_seat.save()
        return redirect("/seating/staff/")
    return render(request, "seating_main/staff.html", {"seats": Seat.objects.all()})

@allowed_users(allowed_roles=["uber-user", "admin"])
def staff_delete_seat(request, seat_id):
    if request.method == "POST":
        seat = Seat.objects.get(id=seat_id)
        seat.delete()
    
    
    return redirect("/seating/staff/")