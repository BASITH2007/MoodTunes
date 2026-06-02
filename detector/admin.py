from django.contrib import admin
from .models import Song, MoodDetectionHistory

@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'mood', 'emoji')
    list_filter = ('mood',)
    search_fields = ('title', 'artist')

@admin.register(MoodDetectionHistory)
class MoodDetectionHistoryAdmin(admin.ModelAdmin):
    list_display = ('mood', 'confidence', 'detection_method', 'timestamp')
    list_filter = ('mood', 'detection_method', 'timestamp')
    readonly_fields = ('timestamp',)
