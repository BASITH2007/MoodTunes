import json
from django.test import TestCase, Client
from django.urls import reverse
from .models import Song, MoodDetectionHistory

class MoodTunesTests(TestCase):
    def setUp(self):
        # Create a test client
        self.client = Client()
        
        # Create some test songs
        self.happy_song = Song.objects.create(
            title="Happy Test",
            artist="Happy Artist",
            mood="happy",
            emoji="☀️",
            youtube_url="https://youtube.com/watch?v=happy"
        )
        self.neutral_song = Song.objects.create(
            title="Neutral Test",
            artist="Neutral Artist",
            mood="neutral",
            emoji="😐",
            youtube_url="https://youtube.com/watch?v=neutral"
        )

    def test_index_view(self):
        """Verify the index page renders successfully"""
        url = reverse('detector:index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'detector/index.html')

    def test_recommend_songs_api(self):
        """Verify the song recommendation API works and returns correct mood songs"""
        url = reverse('detector:recommend_songs')
        
        # Test happy emotion
        response = self.client.get(url, {'emotion': 'happy'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['emotion'], 'happy')
        self.assertEqual(len(data['tracks']), 1)
        self.assertEqual(data['tracks'][0]['title'], 'Happy Test')
        
        # Test nonexistent emotion falls back to neutral
        response = self.client.get(url, {'emotion': 'fearful'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['emotion'], 'neutral')
        self.assertEqual(data['tracks'][0]['title'], 'Neutral Test')

    def test_save_detection_api(self):
        """Verify we can save detections to history"""
        url = reverse('detector:save_detection')
        payload = {
            'mood': 'happy',
            'confidence': 0.95,
            'detection_method': 'camera'
        }
        
        # Make post request
        response = self.client.post(
            url,
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        
        # Check database
        history_records = MoodDetectionHistory.objects.all()
        self.assertEqual(history_records.count(), 1)
        record = history_records.first()
        self.assertEqual(record.mood, 'happy')
        self.assertEqual(record.confidence, 0.95)
        self.assertEqual(record.detection_method, 'camera')

    def test_get_history_api(self):
        """Verify the history listing API returns correct entries"""
        # Save a record
        MoodDetectionHistory.objects.create(
            mood='sad',
            confidence=0.88,
            detection_method='text'
        )
        
        url = reverse('detector:get_history')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        
        self.assertEqual(len(data['history']), 1)
        self.assertEqual(data['history'][0]['mood'], 'sad')
        self.assertEqual(data['history'][0]['confidence'], 0.88)
        self.assertEqual(data['history'][0]['detection_method'], 'text')
