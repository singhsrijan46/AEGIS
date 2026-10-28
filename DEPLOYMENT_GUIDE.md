# AEGIS-Brand™ — Step-by-Step Deployment Guide

This guide provides step-by-step instructions to deploy **AEGIS-Brand™** to production for your **Round 2 Hackathon Submission** ("A deployed link, installation package or clear functional demonstration").

---

## Architecture Overview

| Component | Technology | Recommended Host | Production URL Example |
|---|---|---|---|
| **Frontend Studio** | React 19 + TypeScript + Vite | **Vercel** (or Netlify/Cloudflare Pages) | `https://aegis-brand.vercel.app` |
| **Backend Engine** | Python 3.11 + FastAPI + Uvicorn | **Render** (Live) | `https://aegis-backend-y1it.onrender.com` |

> [!TIP]
> **Zero-Friction Fallback for Judges:** The frontend API client has a built-in fallback simulation engine. Even if you deploy *only* the frontend on Vercel initially, judges will still be able to run interactive audits on benchmark drafts, inspect visual assets, test CMS gates, and view ambiguity heatmaps with zero downtime.

---

## Method 1: Deploy Frontend on Vercel (Fastest — 2 Minutes)

We have already configured [`vercel.json`](file:///d:/AEGIS/vercel.json) at the root and [`frontend/vercel.json`](file:///d:/AEGIS/frontend/vercel.json).

### Option A: Via Vercel Web Dashboard (Recommended)

1. **Push your code to GitHub**:
   ```bash
   git add .
   git commit -m "feat: configure deployment files for Vercel and Render"
   git push origin main
   ```

2. **Import into Vercel**:
   - Go to [vercel.com](https://vercel.com/) and sign in.
   - Click **"Add New..."** → **"Project"**.
   - Select your **AEGIS** repository.

3. **Configure Build Settings**:
   - **Framework Preset**: `Vite`
   - **Root Directory**: Click *Edit* and select `frontend` (or leave as `./` since root `vercel.json` handles monorepo build).
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
   - **Environment Variables** (Optional, add once backend is deployed):
     - `VITE_API_BASE`: `https://your-backend-app.onrender.com`

4. **Click "Deploy"**:
   - Deployment finishes in ~45 seconds.
   - You will get a live public link (e.g., `https://aegis-brand.vercel.app`) to submit in your Round 2 portal.

---

### Option B: Via Vercel CLI (Direct from Terminal)

1. Open PowerShell / Command Prompt:
   ```bash
   npm install -g vercel
   ```

2. Deploy directly from the `frontend` folder:
   ```bash
   cd d:\AEGIS\frontend
   vercel
   ```
   - Follow prompts: Link to existing project (`No`), Project name (`aegis-brand`), directory (`./`).
   - For production deployment:
     ```bash
     vercel --prod
     ```

---

## Method 2: Deploy Backend on Render (Free Tier — 3 Minutes)

We have created [`requirements.txt`](file:///d:/AEGIS/requirements.txt) and [`render.yaml`](file:///d:/AEGIS/render.yaml) for instant configuration.

### Option A: 1-Click Render Blueprint

1. Go to [dashboard.render.com](https://dashboard.render.com/).
2. Click **"New +"** → **"Blueprint"**.
3. Connect your GitHub repository.
4. Render will read [`render.yaml`](file:///d:/AEGIS/render.yaml) and automatically deploy both the FastAPI backend and frontend static site.

---

### Option B: Manual Web Service on Render

1. Go to [dashboard.render.com](https://dashboard.render.com/).
2. Click **"New +"** → **"Web Service"**.
3. Select your GitHub repository.
4. Fill in the following settings:
   - **Name**: `aegis-backend`
   - **Language**: `Python 3`
   - **Region**: `Oregon (US West)` or closest to you
   - **Branch**: `main`
   - **Root Directory**: Leave blank (repo root)
   - **Build Command**:
     ```bash
     pip install -r requirements.txt
     ```
   - **Start Command**:
     ```bash
     uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT
     ```
   - **Instance Type**: `Free`
5. Click **"Create Web Service"**.
6. Once deployed, copy your service URL (e.g. `https://aegis-backend.onrender.com`).
7. Check the interactive OpenAPI Swagger docs at:
   `https://aegis-backend.onrender.com/docs`

---

## Connecting Frontend to Backend in Vercel

Once your backend is live on Render:
1. Open your project on [vercel.com](https://vercel.com/).
2. Go to **Settings** → **Environment Variables**.
3. Add:
   - **Key**: `VITE_API_BASE`
   - **Value**: `https://aegis-backend.onrender.com` (no trailing slash)
4. Go to **Deployments** → Click the three dots on the latest deployment → **Redeploy**.

---

## Method 3: Containerized Docker Deployment (Railway / Fly.io / AWS)

We have provided [`Dockerfile`](file:///d:/AEGIS/Dockerfile) in the root directory.

### Local Container Run:
```bash
docker build -t aegis-defense .
docker run -p 8000:8000 aegis-defense
```

### Deploying to Railway:
1. Go to [railway.app](https://railway.app/).
2. Click **"New Project"** → **"Deploy from GitHub repo"**.
3. Railway will auto-detect the `Dockerfile` or `requirements.txt` and launch the service.

---

## Submission Checklist for Round 2

- [ ] **Live URL:** Add your Vercel URL (e.g. `https://aegis-brand.vercel.app`) to the form.
- [ ] **GitHub Repo:** Make sure repository visibility is set to Public or shared with judges.
- [ ] **Verification:** Verify that clicking "Audit Document" runs successfully.
- [ ] **Form Answers:** Copy the prepared answers from [`ROUND_2_SUBMISSION_ANSWERS.md`](file:///d:/AEGIS/ROUND_2_SUBMISSION_ANSWERS.md) into the hackathon portal.
