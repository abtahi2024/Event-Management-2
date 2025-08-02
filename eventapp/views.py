from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Count, Q
from django.contrib.auth.decorators import login_required, permission_required
from eventapp.models import *
from eventapp.forms import CreateEvent, CreateCategory
from users.views import *

# Role-Based Dashboard
@login_required
def dashboard(request):
    if is_admin(request.user):
        return redirect('admin-dashboard')
    elif is_organizer(request.user):
        return redirect('organizer-dashboard')
    elif is_participant(request.user):
        return redirect('participant-dashboard')

# Event Creation View
@permission_required("eventapp.create_event", 'no-access')
def create_event(request):
    categories = Category.objects.all()
    form = CreateEvent(categories=categories)
    if request.method == "POST":
        form = CreateEvent(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "New Event Created Successfully.")
    context = {'form': form}
    return render(request, "create_event.html", context)

# Category Creation View
@permission_required("eventapp.create_category", 'no-access')
def create_category(request):
    form = CreateCategory()
    if request.method == "POST":
        form = CreateCategory(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Category Created Successfully.")
        else:
            messages.error(request, "Category already exist.")
    context = {'form': form}
    return render(request, 'create_category.html', context)

# All Event Viewing View
def view_events(request):
    base_q = Event.objects.annotate(partice_count=Count('participants')).select_related('category')
    categories = Category.objects.all()
    if request.GET.get('search', 'all') == 'all' or request.GET.get('search', 'all')== '':
        events = base_q.all()
    else:
        events = base_q.filter(Q(name__icontains=request.GET.get('search', 'all')) | Q(location__icontains=request.GET.get('search', 'all')))
    if request.GET.get('category', 'all') == 'all':
        events = events.all()
    else:
        events = events.filter(category__name__contains=request.GET.get('category', 'all'))
    if request.GET.get('start_date', '2025-7-27') == '':
        events = events.all()
    else:
        events = events.filter(date__range=[request.GET.get('start_date', '2025-7-27'), request.GET.get('end_date', '2030-12-31')])
    return render(request, 'view_events.html', {'events': events, 'categories': categories})

# All Category Viewing View
@permission_required("eventapp.view_category", 'no-access')
def view_categories(request):
    categories = Category.objects.all()
    return render(request, 'view_categories.html', {'categories': categories})

# Event Updating View
@permission_required("eventapp.update_event", 'no-access')
def update_event(request, id):
    event = Event.objects.get(id=id)
    categories = Category.objects.all()
    form = CreateEvent(categories=categories, instance=event)
    if request.method == "POST":
        form = CreateEvent(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Event Updated Successfully.")
    context = {'form': form}
    return render(request, "create_event.html", context)

@permission_required("eventapp.update_category", 'no-access')
#* Category Updating View
def update_category(request, id):
    category = Category.objects.get(id=id)
    form = CreateCategory(instance=category)
    if request.method == "POST":
        form = CreateCategory(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Category Updated Successfully.")
        else:
            messages.error(request, "Category with that Name already exist.")
    context = {'form': form}
    return render(request, 'create_category.html', context)

# Event Deleting View
@permission_required("eventapp.delete_event", 'no-access')
def delete_event(request, id):
    if request.method == 'POST':
        event = Event.objects.get(id=id)
        event.delete()
        messages.success(request, "Delete Successfully")
        return redirect('view-event')
    else:
        messages.error(request, "Something went Wrong!")

# Category Deleting View
@permission_required("eventapp.delete_category", 'no-access')
def delete_category(request, id):
    if request.method == 'POST':
        category = Category.objects.get(id=id)
        category.delete()
        messages.success(request, "Category Delete successfully")
        return redirect('view-category')
    else:
        messages.error(request, "Something went Wrong!")

#* Event Details View
def event_details(request, id):
    event = Event.objects.annotate(partice_count=Count('participants')).get(id=id)
    participants = event.participants.all()
    return render(request, "event_details.html", {'event': event, 'participants': participants})

#Event RSVP View
@login_required
def rsvp(request, user_id, event_id):
    event = Event.objects.filter(id=event_id).first()
    if not event.participants.filter(id=user_id).exists():
        event.participants.add(user_id)
        return redirect('view-event')
    else:
        return redirect('no-access')

