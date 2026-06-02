# 🎵 Emotion Sync Music Engine (Django AI Edition)

A full-stack Django web application that detects user emotions in real-time (via face detection in the camera feed or text-based feelings analysis) and recommends a music playlist matching their mood.

This project is built using **Django** for the backend, database, and templates, and uses **face-api.js** to run AI-powered face emotion detection directly in the browser.

---

## ✨ Features

- 📸 **Camera Mode**: Real-time camera face expression tracking (detects Happy, Sad, Angry, Surprised, Fearful, Disgusted, Neutral).
- ✍️ **Text Mode**: Input custom text describing how you feel to determine your mood via keyword mapping.
- 📊 **Confidence Tracking**: Live charts showing confidence percentages for all emotions.
- 💾 **Session History Logs**: Saves your detection history to the SQLite database and displays a log of recent moods in the UI in real-time.
- 🎵 **SQLite Playlist Database**: Serves playlists from a relational database model (`Song`), manageable directly through the Django Admin panel.
- ⚡ **Local Static Models**: Hosts face-api weights locally on Django's static server, making model loading ultra-fast and independent of CDNs.

---

## 🛠️ Technology Stack

- **Backend**: Python, Django 5.0
- **Database**: SQLite3
- **Frontend**: HTML5 (Django Templates), CSS3 (neon-dark styling theme), Vanilla JavaScript
- **AI/ML Engine**: TinyFaceDetector & FaceExpressionNet (`face-api.js` client-side library)

---

## 🚀 How to Run Locally

### 1. Clone the repository and navigate inside:
```bash
git clone <your-repository-url>
cd moodtunes_django
```

### 2. Install dependencies:
Ensure you have Python installed, then run:
```bash
pip install -r requirements.txt
```

### 3. Run database migrations:
Create the SQLite database and generate required tables:
```bash
python manage.py migrate
```

### 4. Seed the playlist database:
Add the default 42 songs categorized by emotions into the database:
```bash
python manage.py seed_songs
```

### 5. Launch the server:
```bash
python manage.py runserver
```
Visit **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)** in your web browser.

---

## 👨‍💼 Managing Playlists (Django Admin)

You can manage the songs database using Django's admin interface:

1. Create a superuser account:
   ```bash
   python manage.py createsuperuser
   ```
2. Follow the prompts to set your username, email, and password.
3. Start the server and navigate to: **[http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)**
4. Log in to add, edit, or delete songs and associate them with different emotions!

---

## 📁 Repository Structure
```
moodtunes_django/
├── manage.py
├── requirements.txt          ← Python dependencies
├── .gitignore                ← Files excluded from git
├── README.md                 ← Project documentation
├── moodtunes_django/         ← Project settings and urls configuration
└── detector/
    ├── models.py             ← Song & MoodDetectionHistory database models
    ├── views.py              ← HTML rendering and JSON endpoint APIs
    ├── urls.py               ← App URL mapping
    ├── templates/            ← HTML templates
    └── static/               ← Stylesheets, client scripts, and face-api weights
```
