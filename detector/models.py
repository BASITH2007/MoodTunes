from django.db import models

class Song(models.Model):
    MOOD_CHOICES = [
        ('happy', 'Happy'),
        ('sad', 'Sad'),
        ('angry', 'Angry'),
        ('surprised', 'Surprised'),
        ('fearful', 'Fearful'),
        ('disgusted', 'Disgusted'),
        ('neutral', 'Neutral'),
    ]
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    mood = models.CharField(max_length=20, choices=MOOD_CHOICES)
    emoji = models.CharField(max_length=10, default="🎵")
    youtube_url = models.URLField()

    def __str__(self):
        return f"{self.title} - {self.artist} ({self.mood})"

class MoodDetectionHistory(models.Model):
    mood = models.CharField(max_length=20)
    confidence = models.FloatField()
    detection_method = models.CharField(max_length=10)  # 'camera' or 'text'
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.mood} ({self.detection_method}) at {self.timestamp}"
