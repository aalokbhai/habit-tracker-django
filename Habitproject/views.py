from django.shortcuts import render, redirect
from django.utils.timezone import localdate, now
from datetime import timedelta
from Habit.models import task, TaskProgress, AboutContent, Feature
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required

def about_page(request):
    """Main about page - accessible to all"""
    about_contents = AboutContent.objects.filter(is_active=True)
    features = Feature.objects.filter(is_active=True)
    
    context = {
        'about_contents': about_contents,
        'features': features,
        'total_users': 1000,  # You can make this dynamic
        'total_habits': 5000,  # You can make this dynamic
    }
    return render(request, 'about.html', context)

@login_required
def custom_logout(request):
    auth_logout(request)
    return redirect('about')



@login_required
def home(request):
    """Main app page (requires login)"""
    today = localdate()
    
    # Calculate week boundaries
    current_week_start = today - timedelta(days=today.weekday())
    last_week_start = current_week_start - timedelta(days=7)
    
    # Get only current user's tasks
    tasks = list(task.objects.filter(user=request.user).order_by('-created_at'))
    task_ids = [t.id for t in tasks]
    total_tasks = len(task_ids)
    
    # Prepare dates
    last_7_days = [today - timedelta(days=i) for i in range(6, -1, -1)]
    current_week_days = [current_week_start + timedelta(days=i) for i in range(7)]
    last_week_days = [last_week_start + timedelta(days=i) for i in range(7)]
    
    # Collect all unique dates we need to query
    all_dates = set(last_7_days + current_week_days + last_week_days)
    
    # Fetch all relevant TaskProgress records in a single query!
    progress_records = TaskProgress.objects.filter(
        task_id__in=task_ids,
        date__in=all_dates
    )
    
    # Create an optimized lookup dictionary: (task_id, date) -> is_completed
    progress_lookup = {(p.task_id, p.date): p.is_completed for p in progress_records}
    
    current_week_completions = [0] * 7
    last_week_completions = [0] * 7
    
    for t in tasks:
        t.completed_today = progress_lookup.get((t.id, today), False)
        t.day_status = {}
        
        # Check completion for last 7 days
        for day in last_7_days:
            t.day_status[day] = progress_lookup.get((t.id, day), False)
        
        # Check completion for current week
        for i, day in enumerate(current_week_days):
            if progress_lookup.get((t.id, day), False):
                current_week_completions[i] += 1
        
        # Check completion for last week
        for i, day in enumerate(last_week_days):
            if progress_lookup.get((t.id, day), False):
                last_week_completions[i] += 1
                
    # Calculate percentages
    current_week_percentages = []
    last_week_percentages = []
    
    if total_tasks > 0:
        for i in range(7):
            current_percent = (current_week_completions[i] / total_tasks) * 100
            current_week_percentages.append(round(current_percent))
            
            last_percent = (last_week_completions[i] / total_tasks) * 100
            last_week_percentages.append(round(last_percent))
    else:
        current_week_percentages = [0] * 7
        last_week_percentages = [0] * 7
    
    # Calculate overall stats
    if total_tasks > 0:
        today_completed = sum(1 for t in tasks if getattr(t, 'completed_today', False))
        today_percentage = (today_completed / total_tasks) * 100
        
        current_week_avg = sum(current_week_percentages) / 7
        last_week_avg = sum(last_week_percentages) / 7
        
        if last_week_avg > 0:
            week_change = ((current_week_avg - last_week_avg) / last_week_avg) * 100
        else:
            week_change = 100 if current_week_avg > 0 else 0
    else:
        today_percentage = 0
        current_week_avg = 0
        last_week_avg = 0
        week_change = 0
    
    # Day names for chart
    day_names = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    
    context = {
        'tasks': tasks,
        'today': today,
        'last_7_days': last_7_days,
        'current_week_days': current_week_days,
        'last_week_days': last_week_days,
        'current_week_percentages': current_week_percentages,
        'last_week_percentages': last_week_percentages,
        'current_week_avg': current_week_avg,
        'last_week_avg': last_week_avg,
        'week_change': week_change,
        'today_percentage': today_percentage,
        'day_names': day_names,
        'total_tasks': total_tasks,
        'current_week_completions': current_week_completions,
        'last_week_completions': last_week_completions,
    }
    return render(request, "home.html", context)

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    
    return render(request, 'signup.html', {'form': form})