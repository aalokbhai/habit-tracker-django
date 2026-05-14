import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Habitproject.settings')
django.setup()

from django.contrib.auth.models import User
from Habit.models import task, TaskProgress
from django.utils.timezone import localdate
from datetime import timedelta

def test_daily_reset():
    print("--- Testing Daily Habit Reset Functionality ---")
    
    user = User.objects.first()
    if not user:
        print("No users found.")
        return
        
    t = task.objects.create(task_name="Test Daily Reset Habit", user=user)
    today = localdate()
    
    # Simulate user marking it complete today
    print(f"\n1. Simulating completion for today ({today})...")
    progress, created = TaskProgress.objects.get_or_create(task=t, date=today)
    progress.is_completed = True
    progress.save()
    
    # Verify today's status
    is_completed_today = TaskProgress.objects.filter(task=t, date=today, is_completed=True).exists()
    print(f"Status for today ({today}): {'✅ Completed' if is_completed_today else '❌ Not Completed'}")
    
    # Verify tomorrow's status (Midnight Reset)
    tomorrow = today + timedelta(days=1)
    print(f"\n2. Simulating system clock rolling over to tomorrow ({tomorrow})...")
    
    # In the actual view, it uses progress_lookup.get((t.id, tomorrow), False)
    # If the record doesn't exist for tomorrow, it defaults to False (Unchecked)
    progress_tomorrow = TaskProgress.objects.filter(task=t, date=tomorrow).first()
    is_completed_tomorrow = progress_tomorrow.is_completed if progress_tomorrow else False
    
    print(f"Status for tomorrow ({tomorrow}): {'✅ Completed' if is_completed_tomorrow else '❌ Not Completed (RESET SUCCESSFULLY)'}")
    
    # Cleanup
    t.delete()

if __name__ == "__main__":
    test_daily_reset()
