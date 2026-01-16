# Deployment Guide: Todo App on Render

This guide will walk you through deploying your FastAPI Todo App on Render.com.

## Prerequisites

1. A GitHub account
2. Your code pushed to a GitHub repository
3. A Render account (sign up at [render.com](https://render.com))

---

## Step-by-Step Deployment Instructions

### Step 1: Prepare Your Code

✅ **Already Done:**
- `.gitignore` - Excludes sensitive files
- `render.yaml` - Deployment configuration
- `database.py` - Updated for production database URLs
- `index.html` - Updated to use automatic API URL detection
- `requirements.txt` - All dependencies listed

### Step 2: Push Code to GitHub

1. **Initialize Git** (if not already done):
   ```bash
   git init
   git add .
   git commit -m "Initial commit - ready for deployment"
   ```

2. **Create a GitHub Repository**:
   - Go to [github.com](https://github.com)
   - Click "New repository"
   - Name it (e.g., `todo-app`)
   - Don't initialize with README (you already have files)
   - Click "Create repository"

3. **Push Your Code**:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/todo-app.git
   git branch -M main
   git push -u origin main
   ```
   Replace `YOUR_USERNAME` with your GitHub username.

### Step 3: Create Render Account

1. Go to [render.com](https://render.com)
2. Click "Get Started for Free"
3. Sign up with GitHub (recommended) or email
4. Verify your email if required

### Step 4: Deploy Using render.yaml (Recommended)

This is the easiest method - Render will automatically create both the database and web service.

1. **Go to Render Dashboard**:
   - Click "New +" button
   - Select "Blueprint"

2. **Connect Repository**:
   - Connect your GitHub account if not already connected
   - Select your `todo-app` repository
   - Render will detect `render.yaml`

3. **Review Configuration**:
   - Render will show you what it will create:
     - PostgreSQL Database (free tier)
     - Web Service (free tier)
   - Click "Apply"

4. **Wait for Deployment**:
   - Render will:
     - Create the PostgreSQL database
     - Build your application
     - Deploy the web service
   - This takes 5-10 minutes

5. **Get Your App URL**:
   - Once deployed, you'll see a URL like: `https://todo-app.onrender.com`
   - Click it to test your app!

### Step 5: Manual Deployment (Alternative Method)

If you prefer to set up manually:

#### 5a. Create PostgreSQL Database

1. In Render Dashboard, click "New +"
2. Select "PostgreSQL"
3. Configure:
   - **Name**: `todo-app-db`
   - **Database**: `todoapp`
   - **User**: `todoapp_user`
   - **Plan**: Free
4. Click "Create Database"
5. Wait for it to be ready
6. **Copy the Internal Database URL** (you'll need it later)

#### 5b. Create Web Service

1. In Render Dashboard, click "New +"
2. Select "Web Service"
3. Connect your GitHub repository
4. Configure the service:
   - **Name**: `todo-app`
   - **Environment**: `Python 3`
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Root Directory**: (leave empty)
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free

5. **Add Environment Variables**:
   Click "Advanced" → "Add Environment Variable" and add:
   
   | Key | Value |
   |-----|-------|
   | `DATABASE_URL` | (From PostgreSQL service → Internal Database URL) |
   | `SECRET_KEY` | (Generate a random string, e.g., use: `openssl rand -hex 32`) |
   | `ALGORITHM` | `HS256` |
   | `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` |

6. Click "Create Web Service"
7. Wait for deployment (5-10 minutes)

### Step 6: Verify Deployment

1. **Check Logs**:
   - In your web service dashboard, click "Logs"
   - Look for "Application startup complete"
   - Check for any errors

2. **Test Your App**:
   - Visit your app URL (e.g., `https://todo-app.onrender.com`)
   - Try registering a new user
   - Create a task
   - Test all features

3. **Check Database**:
   - Go to your PostgreSQL service
   - Click "Connect" to see connection info
   - Tables should be created automatically

---

## Environment Variables Reference

Your app needs these environment variables:

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | Auto-provided by Render |
| `SECRET_KEY` | Secret for JWT token signing | Random 32+ character string |
| `ALGORITHM` | JWT algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration time | `30` |

---

## Troubleshooting

### Issue: App won't start

**Solution:**
- Check logs in Render dashboard
- Ensure all environment variables are set
- Verify `requirements.txt` is correct
- Check that `DATABASE_URL` is correct

### Issue: Database connection errors

**Solution:**
- Ensure you're using the **Internal Database URL** (not External)
- Check that database service is running
- Verify `DATABASE_URL` format is correct

### Issue: CORS errors

**Solution:**
- The app is configured to allow all origins (`*`)
- If you need specific origins, update `main.py` line 19

### Issue: 502 Bad Gateway

**Solution:**
- Check if the app is still building
- Review logs for startup errors
- Ensure `startCommand` is correct
- Free tier services spin down after 15 minutes of inactivity - first request may take 30-60 seconds

### Issue: Static files not loading

**Solution:**
- Ensure `index.html` is in the root directory
- Check that FastAPI is serving it correctly (already configured)

---

## Free Tier Limitations

⚠️ **Important Notes:**

1. **Spin Down**: Free tier services spin down after 15 minutes of inactivity
   - First request after spin-down takes 30-60 seconds
   - Consider upgrading to paid tier for always-on service

2. **Database**: Free tier PostgreSQL has:
   - 90 days data retention
   - 1GB storage limit
   - Shared resources

3. **Web Service**: Free tier has:
   - 512MB RAM
   - Shared CPU
   - 750 hours/month (enough for always-on if you upgrade)

---

## Updating Your App

1. **Make Changes Locally**
2. **Commit and Push**:
   ```bash
   git add .
   git commit -m "Your update message"
   git push
   ```
3. **Render Auto-Deploys**: Render automatically detects pushes and redeploys
4. **Monitor**: Watch the logs to ensure successful deployment

---

## Security Recommendations

1. **SECRET_KEY**: Use a strong, random secret key
   ```bash
   # Generate a secure key:
   openssl rand -hex 32
   ```

2. **CORS**: In production, restrict CORS to your domain:
   ```python
   allow_origins=["https://your-app.onrender.com"]
   ```

3. **HTTPS**: Render provides free SSL certificates automatically ✅

---

## Next Steps

- ✅ Your app is now live!
- 🔗 Share your Render URL with others
- 📊 Monitor usage in Render dashboard
- 🔄 Set up automatic deployments from GitHub
- 💰 Consider upgrading if you need always-on service

---

## Support

- **Render Docs**: [render.com/docs](https://render.com/docs)
- **Render Community**: [community.render.com](https://community.render.com)
- **FastAPI Docs**: [fastapi.tiangolo.com](https://fastapi.tiangolo.com)

---

**Congratulations! Your Todo App is now deployed! 🎉**
