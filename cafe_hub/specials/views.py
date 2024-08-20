from django.shortcuts import render, redirect
from .models import Special

# Create your views here.
def homepage(request):
    branch=request.user.branch
    specials = Special.objects.filter(branch=branch)
    is_staff = request.user.groups.filter(name__in=['uber-user', 'admin']).exists()
    context = {
        "specials": specials,
        "is_staff": is_staff,
    }
    return render(request, "home.html", context)


def create_special(request):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        price = request.POST.get("price")
        image = request.FILES.get("image")

        branch=request.user.branch
        if branch:
            special = Special.objects.create(
                name=name,
                description=description,
                price=price,
                image=image,
                branch=branch
            )
            special.save()
    return redirect('/specials/')

def delete_special(request, special_id):
    branch=request.user.branch
    special = Special.objects.get(id=special_id,branch=branch)

    special.delete()
    return redirect('/specials/')