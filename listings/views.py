


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from categories.models import Category
from locations.models import Location
from .models import Listing, ListingImage 
from django.core.paginator import Paginator
from django.http import HttpResponse



@login_required
def create_listing(request):
    if request.user.role != 'customer':
        messages.error(request, 'Подавать объявления могут только покупатели.')
        return redirect('pages:home')

    categories = Category.objects.all()
    regions = Location.objects.filter(level=1).order_by('name')

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        price = request.POST.get('price')
        category_id = request.POST.get('category')
        location_id = request.POST.get('location')
        phone = request.POST.get('phone')

        if not location_id:
            messages.error(request, 'Выберите район.')
            return render(request, 'listings/create.html', {'categories': categories, 'regions': regions})

        listing = Listing.objects.create(
            user=request.user,
            title=title,
            description=description,
            price=price,
            category_id=category_id,
            location_id=location_id,
            phone=phone,
        )

        for image in request.FILES.getlist('images'):
            ListingImage.objects.create(listing=listing, image=image)

        messages.success(request, 'Объявление отправлено на проверку.')
        return redirect('listings:my_listings')

    return render(request, 'listings/create.html', {'categories': categories, 'regions': regions})



def listing_list(request):
    location_id = request.GET.get('location')
    category_id = request.GET.get('category')
    page_number = request.GET.get('page', 1)

    listings_qs = Listing.objects.filter(status=Listing.STATUS_APPROVED, is_active=True)

    if location_id:
        location = Location.objects.filter(id=location_id).first()
        if location:
            ids = [location.id]
            for child in location.children.all():
                ids.append(child.id)
                ids += list(child.children.values_list('id', flat=True))
            listings_qs = listings_qs.filter(location_id__in=ids)

    if category_id:
        listings_qs = listings_qs.filter(category_id=category_id)

    paginator = Paginator(listings_qs, 20)
    page_obj = paginator.get_page(page_number)

    if request.GET.get('ajax') == '1':
        if int(page_number) > paginator.num_pages:
            return HttpResponse('')
        return render(request, 'listings/_listing_cards.html', {'listings': page_obj.object_list})

    return render(request, 'listings/list.html', {
        'listings': page_obj.object_list,
        'page_obj': page_obj,
        'location_id': location_id or '',
        'category_id': category_id or '',
    })


@login_required
def my_listings(request):
    listings = Listing.objects.filter(user=request.user)
    return render(request, 'listings/my_listings.html', {'listings': listings, 'active_tab': 'listings'})