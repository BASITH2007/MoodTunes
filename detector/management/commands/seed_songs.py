from django.core.management.base import BaseCommand
from detector.models import Song

class Command(BaseCommand):
    help = 'Seeds the database with initial mood songs'

    def handle(self, *args, **kwargs):
        songs_data = {
            "happy": [
                {"title": "Happy", "artist": "Pharrell Williams", "emoji": "☀️", "url": "https://www.youtube.com/watch?v=ZbZSe6N_BXs"},
                {"title": "Can't Stop the Feeling", "artist": "Justin Timberlake", "emoji": "🕺", "url": "https://www.youtube.com/watch?v=ru0K8uYEZWw"},
                {"title": "Uptown Funk", "artist": "Bruno Mars", "emoji": "🎸", "url": "https://www.youtube.com/watch?v=OPf0YbXqDm0"},
                {"title": "Good as Hell", "artist": "Lizzo", "emoji": "💃", "url": "https://www.youtube.com/watch?v=SmbmeOgWsqE"},
                {"title": "Walking on Sunshine", "artist": "Katrina & Waves", "emoji": "🌞", "url": "https://www.youtube.com/watch?v=iPUmE-tne5U"},
                {"title": "Shake It Off", "artist": "Taylor Swift", "emoji": "🎤", "url": "https://www.youtube.com/watch?v=nfWlot6h_JM"},
            ],
            "sad": [
                {"title": "Someone Like You", "artist": "Adele", "emoji": "💙", "url": "https://www.youtube.com/watch?v=hLQl3WQQoQ0"},
                {"title": "Fix You", "artist": "Coldplay", "emoji": "🌧️", "url": "https://www.youtube.com/watch?v=k4V3Mo61fJM"},
                {"title": "The Night We Met", "artist": "Lord Huron", "emoji": "🌙", "url": "https://www.youtube.com/watch?v=KtlgYxa6BMU"},
                {"title": "Skinny Love", "artist": "Bon Iver", "emoji": "🍂", "url": "https://www.youtube.com/watch?v=ssdgFoHLwnk"},
                {"title": "Let Her Go", "artist": "Passenger", "emoji": "🚂", "url": "https://www.youtube.com/watch?v=RBumgq5yVrA"},
                {"title": "All I Want", "artist": "Kodaline", "emoji": "❄️", "url": "https://www.youtube.com/watch?v=v-J8KkYXo5s"},
            ],
            "angry": [
                {"title": "In The End", "artist": "Linkin Park", "emoji": "💢", "url": "https://www.youtube.com/watch?v=eVTXPUF4Oz4"},
                {"title": "Numb", "artist": "Linkin Park", "emoji": "🌋", "url": "https://www.youtube.com/watch?v=kXYiU_JCYtU"},
                {"title": "Given Up", "artist": "Linkin Park", "emoji": "😤", "url": "https://www.youtube.com/watch?v=0xyzoFn0Huk"},
                {"title": "Radioactive", "artist": "Imagine Dragons", "emoji": "☢️", "url": "https://www.youtube.com/watch?v=ktvTqknDobU"},
                {"title": "Believer", "artist": "Imagine Dragons", "emoji": "🔥", "url": "https://www.youtube.com/watch?v=7wtfhZwyrcc"},
                {"title": "Monster", "artist": "Imagine Dragons", "emoji": "👹", "url": "https://www.youtube.com/watch?v=whyXfPzQYVA"},
            ],
            "surprised": [
                {"title": "Bohemian Rhapsody", "artist": "Queen", "emoji": "👑", "url": "https://www.youtube.com/watch?v=fJ9rUzIMcZQ"},
                {"title": "Mr. Brightside", "artist": "The Killers", "emoji": "🌟", "url": "https://www.youtube.com/watch?v=gGdGFtwCNBE"},
                {"title": "Take On Me", "artist": "A-ha", "emoji": "🎹", "url": "https://www.youtube.com/watch?v=djV11Xbc914"},
                {"title": "Africa", "artist": "Toto", "emoji": "🌍", "url": "https://www.youtube.com/watch?v=FTQbiNvZqaY"},
                {"title": "Don't Stop Me Now", "artist": "Queen", "emoji": "⚡", "url": "https://www.youtube.com/watch?v=HgzGwKwLmgM"},
                {"title": "Somebody That I Used to Know", "artist": "Gotye", "emoji": "🎭", "url": "https://www.youtube.com/watch?v=8UVNT4wvIGY"},
            ],
            "fearful": [
                {"title": "Breathe Me", "artist": "Sia", "emoji": "🌿", "url": "https://www.youtube.com/watch?v=ghPcYqn0p4Y"},
                {"title": "Holocene", "artist": "Bon Iver", "emoji": "❄️", "url": "https://www.youtube.com/watch?v=TWcyIpul8OE"},
                {"title": "Yellow", "artist": "Coldplay", "emoji": "⭐", "url": "https://www.youtube.com/watch?v=yKNxeF4KMsY"},
                {"title": "Weightless", "artist": "Marconi Union", "emoji": "🎐", "url": "https://www.youtube.com/watch?v=UfcAVejslrU"},
                {"title": "Mad World", "artist": "Gary Jules", "emoji": "🌀", "url": "https://www.youtube.com/watch?v=4N3N1MlvVc4"},
                {"title": "Clair de Lune", "artist": "Debussy", "emoji": "🌙", "url": "https://www.youtube.com/watch?v=CvFH_6DNRCY"},
            ],
            "disgusted": [
                {"title": "Dog Days Are Over", "artist": "Florence + Machine", "emoji": "🌸", "url": "https://www.youtube.com/watch?v=iWOyfLBYtuU"},
                {"title": "Stronger", "artist": "Kanye West", "emoji": "💪", "url": "https://www.youtube.com/watch?v=PsO6ZnUZI0g"},
                {"title": "Good Riddance", "artist": "Green Day", "emoji": "✌️", "url": "https://www.youtube.com/watch?v=CnQ8N1KacJc"},
                {"title": "Clocks", "artist": "Coldplay", "emoji": "🕰️", "url": "https://www.youtube.com/watch?v=d020hcWA_Wg"},
                {"title": "Shake It Out", "artist": "Florence + Machine", "emoji": "🎊", "url": "https://www.youtube.com/watch?v=wiTQUHGsM7U"},
                {"title": "Leave Out All the Rest", "artist": "Linkin Park", "emoji": "🌈", "url": "https://www.youtube.com/watch?v=zDR7-MkQMcQ"},
            ],
            "neutral": [
                {"title": "Chasing Cars", "artist": "Snow Patrol", "emoji": "☁️", "url": "https://www.youtube.com/watch?v=GemKqzILV4w"},
                {"title": "Budapest", "artist": "George Ezra", "emoji": "🏙️", "url": "https://www.youtube.com/watch?v=VHrLPs3_1Fs"},
                {"title": "Ho Hey", "artist": "The Lumineers", "emoji": "🎵", "url": "https://www.youtube.com/watch?v=zvCBSSwgtg4"},
                {"title": "Float On", "artist": "Modest Mouse", "emoji": "🌊", "url": "https://www.youtube.com/watch?v=CTAud5O7Qqk"},
                {"title": "Intro", "artist": "The XX", "emoji": "◻️", "url": "https://www.youtube.com/watch?v=xMV6D0f6C0Q"},
                {"title": "Pumped Up Kicks", "artist": "Foster The People", "emoji": "👟", "url": "https://www.youtube.com/watch?v=SDTZ7iX4vTQ"},
            ]
        }

        # Clear existing songs to prevent duplicates
        Song.objects.all().delete()
        self.stdout.write("Cleared existing songs database.")

        count = 0
        for mood, playlist in songs_data.items():
            for song in playlist:
                Song.objects.create(
                    title=song["title"],
                    artist=song["artist"],
                    mood=mood,
                    emoji=song["emoji"],
                    youtube_url=song["url"]
                )
                count += 1
        
        self.stdout.write(self.style.SUCCESS(f"Successfully seeded {count} songs into the database!"))
