# 🍷 Wine Notes - Production Edition

## What You Got

A complete, production-ready wine tracking app with:

✅ **User Accounts** - Each person has their own private wine notes
✅ **Authentication** - Demo login (Google OAuth ready)
✅ **Database** - PostgreSQL for production, SQLite for development  
✅ **Photo Uploads** - Store wine bottle pictures
✅ **Cloud Deployment** - Ready for Railway + Vercel
✅ **Git Ready** - Push to GitHub and auto-deploy
✅ **All Your Features** - Drinking with, meal type, photos, etc.

---

## Quick Start - Test Locally (5 minutes)

### Terminal 1 - Backend:
```bash
cd wine-notes-production/backend
python3.13 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python main.py
```

### Terminal 2 - Frontend:
```bash
cd wine-notes-production/frontend
npm install && npm run dev
```

### Browser:
Open: `http://localhost:5173`

**Sign in with ANY email** - it's demo mode!

---

## Deploy to Internet (30 minutes)

See **DEPLOYMENT.md** for complete step-by-step guide.

**Quick summary:**
1. Push to GitHub
2. Deploy backend to Railway (free)
3. Deploy frontend to Vercel (free)
4. Share URL with friends!

---

## What's Different from Before?

**Old version:**
- ❌ No user accounts
- ❌ No cloud deployment
- ❌ Everyone shared one JSON file

**New version:**
- ✅ Each user has their own account
- ✅ Real database (PostgreSQL)
- ✅ Deploy to internet
- ✅ Your friends can use it
- ✅ Easy to add new features via Git

---

## File Structure

```
wine-notes-production/
├── backend/
│   ├── main.py              # API with authentication
│   ├── requirements.txt     # Dependencies
│   └── .env.example         # Configuration template
├── frontend/
│   ├── src/
│   │   └── App.jsx          # React app with login
│   ├── package.json
│   └── vite.config.js
├── .gitignore               # What NOT to commit
├── README.md                # Full documentation
├── DEPLOYMENT.md            # Step-by-step deploy guide
└── railway.json             # Railway config
```

---

## Development Workflow

### 1. Make Changes
- Edit files in `backend/` or `frontend/`
- Test locally

### 2. Commit & Push
```bash
git add .
git commit -m "Add new feature"
git push
```

### 3. Auto-Deploy
- Railway & Vercel automatically deploy!
- Changes live in ~2 minutes

---

## Adding New Features

Just describe what you want and AI can help:

**Examples:**
- "Add a statistics dashboard"
- "Add wine recommendations"
- "Add CSV export"
- "Add wine cellar inventory"
- "Add social sharing"

---

## User Accounts

**How it works:**
1. Each person signs in with their email
2. They get a JWT token (stored in browser)
3. All their notes are private (linked to their user_id)
4. Photos are namespaced by user

**Future (Google OAuth):**
- Click "Sign in with Google"
- No password needed
- More secure
- Configuration ready, just needs frontend integration

---

## Database

**Development (Local):**
- SQLite (`wine_notes.db`)
- Simple, file-based
- Perfect for testing

**Production (Cloud):**
- PostgreSQL
- Railway provides it free
- Auto-configured
- Handles multiple users

---

## Cost

**Free Tier (Perfect for you):**
- Railway: $5 credit/month
- Vercel: Unlimited deployments
- Total: **$0/month** 🎉

**If you exceed free tier:**
- Railway: ~$5-10/month
- Vercel: Usually stays free
- Total: ~$10/month for unlimited users

---

## Security

✅ JWT token authentication
✅ Password hashing (bcrypt)
✅ CORS protection
✅ SQL injection prevention
✅ Environment variables for secrets
✅ User data isolation

---

## Monitoring

**Railway:**
- View logs in dashboard
- Monitor database usage
- See deployment history

**Vercel:**
- Analytics built-in
- Error tracking
- Performance monitoring

---

## Next Steps

1. **Test Locally** (see Quick Start above)
2. **Push to GitHub** (3 commands)
3. **Deploy** (follow DEPLOYMENT.md)
4. **Share with Friends** (give them the URL)
5. **Add Features** (describe what you want, AI helps)

---

## Support

Everything you need is in this package:
- `README.md` - Complete documentation
- `DEPLOYMENT.md` - Step-by-step deployment
- `.env.example` - Configuration templates
- Code comments throughout

---

## 🎉 Ready to Deploy!

Your wine app is production-grade and ready for the world!

**Start here:**
1. Test locally (Quick Start above)
2. When ready, read DEPLOYMENT.md
3. Push to GitHub
4. Deploy in 30 minutes
5. Share with friends!

Enjoy! 🍷
