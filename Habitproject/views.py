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



def home(request):
    """Main app page (requires login)"""
    today = localdate()
    
    # Calculate week boundaries
    current_week_start = today - timedelta(days=today.weekday())
    last_week_start = current_week_start - timedelta(days=7)
    
    # Get only current user's tasks
    tasks = task.objects.filter(user=request.user).order_by('-created_at')
    
    # Prepare last 7 days
    last_7_days = []
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        last_7_days.append(day)
    
    # Calculate days for current and last week
    current_week_days = [current_week_start + timedelta(days=i) for i in range(7)]
    last_week_days = [last_week_start + timedelta(days=i) for i in range(7)]
    
    # Prepare data for each task
    total_tasks = tasks.count()
    current_week_completions = [0] * 7
    last_week_completions = [0] * 7
    
    for t in tasks:
        t.completed_today = False
        t.day_status = {}
        
        # Check completion for last 7 days
        for day in last_7_days:
            progress = TaskProgress.objects.filter(task=t, date=day).first()
            is_completed = progress.is_completed if progress else False
            t.day_status[day] = is_completed
            
            if day == today:
                t.completed_today = is_completed
        
        # Check completion for current week
        for i, day in enumerate(current_week_days):
            progress = TaskProgress.objects.filter(task=t, date=day).first()
            is_completed = progress.is_completed if progress else False
            
            if is_completed:
                current_week_completions[i] += 1
        
        # Check completion for last week
        for i, day in enumerate(last_week_days):
            progress = TaskProgress.objects.filter(task=t, date=day).first()
            is_completed = progress.is_completed if progress else False
            
            if is_completed:
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
        current_week_percentages = [0, 0, 0, 0, 0, 0, 0]
        last_week_percentages = [0, 0, 0, 0, 0, 0, 0]
    
    # Calculate overall stats
    if total_tasks > 0:
        today_completed = sum(1 for t in tasks if t.completed_today)
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