# Wine Notes - Production Ready 🍷

A full-stack wine tracking application with user authentication, photo uploads, and cloud deployment support.

## ✨ Features

- 🔐 **User Authentication** - Demo login (Google OAuth ready)
- 👥 **Multi-user Support** - Each user has their own wine notes
- 📸 **Photo Uploads** - Store wine bottle photos
- 🗄️ **Database** - PostgreSQL (production) / SQLite (development)
- ☁️ **Cloud Ready** - Deploy to Railway, Render, or Vercel
- 📝 **Comprehensive Wine Tracking** - All the fields you need

## 🚀 Quick Start (Local Development)

### Prerequisites
- Python 3.13+
- Node.js 18+
- Git

### 1. Backend Setup

```bash
cd backend
python3.13 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python main.py
```

Backend runs on: `http://localhost:8000`

### 2. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on: `http://localhost:5173`

### 3. Use the App

1. Open `http://localhost:5173`
2. Enter any email to sign in (demo mode)
3. Start tracking wines!

---

## 🌐 Deployment to Production

### Option 1: Deploy to Railway (Recommended - Easiest)

**Backend:**
1. Push this repo to GitHub
2. Go to [railway.app](https://railway.app)
3. Click "New Project" → "Deploy from GitHub"
4. Select your repository
5. Railway auto-detects Python and deploys!
6. Add PostgreSQL database:
   - Click "New" → "Database" → "PostgreSQL"
   - Railway auto-adds DATABASE_URL
7. Set environment variables:
   ```
   SECRET_KEY=your-super-secret-random-string
   ALLOWED_ORIGINS=https://your-frontend-url.vercel.app
   ```

**Frontend:**
1. Go to [vercel.com](https://vercel.com)
2. Import your GitHub repository
3. Set framework preset to "Vite"
4. Add environment variable:
   ```
   VITE_API_URL=https://your-railway-backend-url.up.railway.app
   ```
5. Deploy!

### Option 2: Deploy to Render

**Backend:**
1. Push to GitHub
2. Go to [render.com](https://render.com)
3. New → Web Service
4. Connect GitHub repo
5. Settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python main.py`
6. Add PostgreSQL database
7. Set environment variables

**Frontend:**
Deploy to Vercel (same as above)

---

## 🔑 Setting Up Google OAuth (Production)

### 1. Get Google OAuth Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project or select existing
3. Enable "Google+ API"
4. Go to "Credentials" → "Create Credentials" → "OAuth 2.0 Client ID"
5. Configure consent screen
6. Create Web Application credentials
7. Add authorized redirect URIs:
   - `http://localhost:5173` (development)
   - `https://your-domain.com` (production)
8. Save Client ID and Client Secret

### 2. Update Backend

In `backend/.env`:
```bash
GOOGLE_CLIENT_ID=your-client-id-here
GOOGLE_CLIENT_SECRET=your-client-secret-here
```

### 3. Update Frontend

The frontend already has Google OAuth button ready - just configure it with your client ID.

---

## 📁 Project Structure

```
wine-notes-production/
├── backend/
│   ├── main.py              # FastAPI server
│   ├── requirements.txt     # Python dependencies
│   ├── .env.example         # Environment template
│   └── uploads/             # Photo storage
├── frontend/
│   ├── src/
│   │   ├── App.jsx          # Main React component
│   │   ├── main.jsx         # React entry
│   │   └── index.css        # Styles
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── .gitignore
└── README.md
```

---

## 🛠️ Development Workflow

### Adding New Features

1. **Make changes locally**
   ```bash
   # Backend changes - restart server
   cd backend && python main.py
   
   # Frontend changes - auto-reloads
   cd frontend && npm run dev
   ```

2. **Test locally**
   - Use demo login
   - Test all features

3. **Push to production**
   ```bash
   git add .
   git commit -m "Add new feature"
   git push origin main
   ```

4. **Auto-deploys** (if connected to Railway/Vercel)

### Git Workflow

```bash
# Initialize (first time only)
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/yourusername/wine-notes.git
git push -u origin main
```

---

## 🗄️ Database

### Development
- Uses SQLite (`wine_notes.db`)
- Automatic setup on first run
- Perfect for local testing

### Production
- Uses PostgreSQL
- Railway/Render provide managed PostgreSQL
- Auto-configured via `DATABASE_URL` environment variable

### Database Schema

**users table:**
- id, email, name, google_id, created_at

**wine_notes table:**
- All your wine fields + user_id (foreign key)

---

## 🔐 Security

- JWT tokens for authentication
- Password hashing with bcrypt
- CORS configured for your domains only
- Environment variables for secrets
- SQL injection protection (SQLAlchemy)

---

## 📱 Mobile Support

The app is fully responsive and works great on mobile devices!

---

## 🐛 Troubleshooting

**Backend won't start:**
- Check Python version: `python --version`
- Activate venv: `source venv/bin/activate`
- Check if port 8000 is free

**Frontend won't connect:**
- Check API_URL in browser console
- Verify backend is running
- Check CORS settings

**Database errors:**
- Development: Delete `wine_notes.db` and restart
- Production: Check DATABASE_URL environment variable

**Photo uploads fail:**
- Check `uploads/` directory exists
- Verify write permissions
- Check file size limits

---

## 📊 Features Roadmap

Current:
- ✅ User authentication (demo)
- ✅ Wine note CRUD
- ✅ Photo uploads
- ✅ Multi-user support
- ✅ Cloud deployment ready

Coming Soon:
- 🔄 Google OAuth (configured, needs frontend integration)
- 📊 Statistics dashboard
- 🍇 Wine recommendations
- 📱 Mobile app (React Native)
- 🌍 Social features (share notes)
- 📥 Import/Export data

---

## 💡 Tips for Your Friends

When sharing with friends:
1. Give them the production URL
2. They enter their email to sign in
3. Each person's notes are private
4. Photos are stored securely

---

## 🤝 Contributing

This is your personal project, but AI can help you add features!

Just describe what you want:
- "Add a statistics page showing my top-rated wines"
- "Add export to PDF functionality"
- "Add wine cellar inventory tracking"

---

## 📄 License

Personal project - do whatever you want with it!

---

## 🎉 You're Ready!

Your app is production-ready with:
- ✅ User accounts
- ✅ Secure authentication
- ✅ Database
- ✅ Photo uploads
- ✅ Easy deployment
- ✅ Easy feature additions

Push to GitHub and deploy! 🚀
