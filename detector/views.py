import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Song, MoodDetectionHistory

def index(request):
    """Renders the main dashboard template"""
    # Fetch recent history
    history = MoodDetectionHistory.objects.all()[:10]
    context = {
        'history': history,
    }
    return render(request, 'detector/index.html', context)

def recommend_songs_api(request):
    """API endpoint to get recommended songs for a specific emotion"""
    emotion = request.GET.get('emotion', '').lower().strip()
    if not emotion:
        return JsonResponse({'error': 'No emotion specified'}, status=400)
    
    songs = Song.objects.filter(mood=emotion)
    # If no songs match this mood, fall back to neutral
    if not songs.exists():
        songs = Song.objects.filter(mood='neutral')
        emotion = 'neutral'
        
    tracks_list = []
    for song in songs:
        tracks_list.append({
            'title': song.title,
            'artist': song.artist,
            'emoji': song.emoji,
            'url': song.youtube_url
        })
        
    return JsonResponse({
        'emotion': emotion,
        'tracks': tracks_list
    })

@csrf_exempt
def save_detection_api(request):
    """API endpoint to save a new mood detection entry"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
        
    try:
        data = json.loads(request.body)
        mood = data.get('mood', '').lower().strip()
        confidence = float(data.get('confidence', 0))
        detection_method = data.get('detection_method', 'camera').lower().strip()
        
        if not mood:
            return JsonResponse({'error': 'Mood is required'}, status=400)
            
        # Create and save detection record
        record = MoodDetectionHistory.objects.create(
            mood=mood,
            confidence=confidence,
            detection_method=detection_method
        )
        
        return JsonResponse({
            'status': 'success',
            'id': record.id,
            'mood': record.mood,
            'confidence': record.confidence,
            'detection_method': record.detection_method,
            'timestamp': record.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        })
        
    except (ValueError, json.JSONDecodeError) as e:
        return JsonResponse({'error': 'Invalid request data'}, status=400)

def get_history_api(request):
    """API endpoint to fetch the last 10 detections"""
    history = MoodDetectionHistory.objects.all()[:10]
    history_list = []
    for item in history:
        history_list.append({
            'mood': item.mood,
            'confidence': item.confidence,
            'detection_method': item.detection_method,
            'timestamp': item.timestamp.strftime('%b %d, %Y, %I:%M %p')
        })
    return JsonResponse({'history': history_list})
