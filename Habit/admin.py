from django.contrib import admin
from .models import task, TaskProgress, AboutContent, Feature , Social

class taskAdmin(admin.ModelAdmin):
    list_display = ('task_name', 'user', 'created_at')
    search_fields = ('task_name', 'user__username')
    list_filter = ('created_at', 'user')

class TaskProgressAdmin(admin.ModelAdmin):
    list_display = ('task', 'date', 'is_completed', 'updated_at')
    list_filter = ('date', 'is_completed')
    search_fields = ('task__task_name',)

class AboutContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('title', 'description')

class FeatureAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('title', 'description')
 

admin.site.register(task, taskAdmin)
admin.site.register(TaskProgress, TaskProgressAdmin)
admin.site.register(AboutContent, AboutContentAdmin)
admin.site.register(Feature, FeatureAdmin)
admin.site.register(Social)