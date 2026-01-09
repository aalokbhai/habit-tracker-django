from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import localdate
from .models import task, TaskProgress


# ➕ ADD NEW HABIT
def addtask(request):
    if request.method == "POST":
        name = request.POST['addtask']
        task.objects.create(
            task_name=name,
            user=request.user  # Add this line
        )
    return redirect("home")


def toggle_today(request, pk):
    today = localdate()
    t = get_object_or_404(task, pk=pk)

    progress, created = TaskProgress.objects.get_or_create(
        task=t,
        date=today
    )
    progress.is_completed = not progress.is_completed
    progress.save()

    # सीधे home page पर redirect
    import time
    return redirect(f"/home/?t={int(time.time())}")

# ❌ DELETE TASK
def mark_delete(request, pk):
    t = get_object_or_404(task, pk=pk)
    t.delete()
    return redirect("home")


# ✏️ EDIT TASK
def edit_task(request, pk):
    t = get_object_or_404(task, pk=pk)

    if request.method == "POST":
        t.task_name = request.POST['edit_task']
        t.save()
        return redirect("home")

    return render(request, 'edit_page.html', {'task5': t})
