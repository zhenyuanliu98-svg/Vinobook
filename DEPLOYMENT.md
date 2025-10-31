# 🚀 Complete Deployment Guide

## Overview
We'll deploy your Wine Notes app so your friends can use it online:
- **Backend** → Railway (with PostgreSQL database)
- **Frontend** → Vercel
- **Total time:** ~30 minutes
- **Cost:** FREE (both have generous free tiers)

---

## Part 1: Push to GitHub (5 minutes)

### 1. Create GitHub Repository

1. Go to [github.com](https://github.com)
2. Click "+" → "New repository"
3. Name it: `wine-notes-app`
4. Make it Public (or Private if you prefer)
5. Don't initialize with README (we have one)
6. Click "Create repository"

### 2. Push Your Code

Open Terminal in your `wine-notes-production` folder:

```bash
git init
git add .
git commit -m "Initial commit - Production ready wine notes app"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/wine-notes-app.git
git push -u origin main
```

Replace `YOUR-USERNAME` with your GitHub username.

✅ **Done!** Your code is now on GitHub.

---

## Part 2: Deploy Backend to Railway (10 minutes)

### 1. Sign Up for Railway

1. Go to [railway.app](https://railway.app)
2. Click "Login" → "Login with GitHub"
3. Authorize Railway

### 2. Create New Project

1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Choose your `wine-notes-app` repository
4. Railway will detect Python and start deploying!

### 3. Add PostgreSQL Database

1. In your project, click "New"
2. Select "Database"
3. Choose "Add PostgreSQL"
4. Railway automatically connects it to your app!

### 4. Configure Environment Variables

1. Click on your backend service
2. Go to "Variables" tab
3. Click "Raw Editor"
4. Add these variables:

```
SECRET_KEY=generate-a-long-random-string-here-at-least-32-characters
ALLOWED_ORIGINS=http://localhost:5173
```

(We'll update ALLOWED_ORIGINS after deploying frontend)

5. Click "Add" or "Update Variables"

### 5. Get Your Backend URL

1. Go to "Settings" tab
2. Find "Domains" section
3. Click "Generate Domain"
4. Copy your URL (looks like: `https://wine-notes-production.up.railway.app`)

✅ **Backend is live!** Test it by visiting `https://your-url.railway.app` - you should see:
```json
{"message": "Wine Notes API - Production Ready", "version": "2.0"}
```

---

## Part 3: Deploy Frontend to Vercel (10 minutes)

### 1. Sign Up for Vercel

1. Go to [vercel.com](https://vercel.com)
2. Click "Sign Up"
3. Choose "Continue with GitHub"
4. Authorize Vercel

### 2. Import Your Project

1. Click "Add New..." → "Project"
2. Find your `wine-notes-app` repository
3. Click "Import"

### 3. Configure Build Settings

1. Framework Preset: **Vite**
2. Root Directory: `frontend`
3. Build Command: `npm run build`
4. Output Directory: `dist`
5. Install Command: `npm install`

### 4. Add Environment Variable

1. Click "Environment Variables"
2. Add:
   - Name: `VITE_API_URL`
   - Value: `https://your-railway-url.up.railway.app` (from Part 2, step 5)
3. Click "Add"

### 5. Deploy!

1. Click "Deploy"
2. Wait 2-3 minutes
3. Vercel gives you a URL (like: `https://wine-notes-app.vercel.app`)

✅ **Frontend is live!**

---

## Part 4: Connect Frontend & Backend (5 minutes)

### Update Backend CORS

1. Go back to Railway
2. Click your backend service
3. Go to "Variables"
4. Update `ALLOWED_ORIGINS` to:
```
https://your-vercel-url.vercel.app,http://localhost:5173
```
(Use your actual Vercel URL)

5. Save - Railway will redeploy automatically

---

## Part 5: Test Everything! (5 minutes)

1. Visit your Vercel URL
2. Enter an email to sign in
3. Add a wine note
4. Upload a photo
5. Create a second account (different email) - verify notes are separate

✅ **Everything works!**

---

## Share with Friends

Give your friends the Vercel URL:
```
https://your-wine-notes-app.vercel.app
```

Each friend:
1. Visits the URL
2. Enters their email
3. Gets their own private wine collection

---

## Monitoring & Management

### Railway Dashboard
- View logs: Railway → Your service → "Logs"
- View database: Railway → PostgreSQL → "Data"
- Monitor usage: Railway → "Usage"

### Vercel Dashboard
- View deployments: Vercel → Your project → "Deployments"
- View analytics: "Analytics" tab
- Check errors: "Logs" tab

---

## Updating Your App

When you want to add features:

```bash
# Make your changes locally
# Test them

# Push to GitHub
git add .
git commit -m "Add new feature"
git push

# That's it! Auto-deploys to Railway & Vercel
```

---

## Free Tier Limits

**Railway (Free):**
- $5 credit per month
- ~500 hours of runtime
- PostgreSQL database included
- Perfect for personal projects

**Vercel (Free):**
- Unlimited deployments
- 100GB bandwidth per month
- Perfect for frontend apps

Both are more than enough for you and your friends!

---

## Troubleshooting

**Backend not starting:**
- Check Railway logs
- Verify DATABASE_URL is set (automatic)
- Check SECRET_KEY is set

**Frontend can't connect:**
- Check VITE_API_URL environment variable
- Verify ALLOWED_ORIGINS in backend includes your Vercel URL
- Check browser console for errors

**Database errors:**
- Railway provides PostgreSQL automatically
- Check "Database" tab in Railway for connection string

**Photo uploads not working:**
- Railway has ephemeral file system
- For production, consider AWS S3 (or upgrade Railway plan)
- For now, works great for testing

---

## Cost Estimates

**If you exceed free tiers:**
- Railway: ~$5-10/month for hobby project
- Vercel: Usually stays free
- Total: **$0-10/month** for unlimited users

---

## Next Steps

### Add Google OAuth

1. Get credentials from Google Cloud Console
2. Add to Railway environment variables
3. Update frontend to use Google button
4. Documentation in README.md

### Custom Domain

**Vercel:**
1. Buy domain (Namecheap, Google Domains, etc.)
2. Vercel → Settings → Domains
3. Add your domain
4. Update DNS records

**Railway:**
1. Railway → Settings → Domains
2. Add custom domain
3. Update DNS records

---

## 🎉 You Did It!

Your Wine Notes app is now:
- ✅ Live on the internet
- ✅ Has user accounts
- ✅ Has a real database
- ✅ Supports photo uploads
- ✅ Ready for your friends to use
- ✅ Easy to update with new features

**Share the URL and enjoy!** 🍷

---

## Need Help?

Common issues and solutions in the troubleshooting section above.

For new features, just describe what you want and I can help you build it!
