# CricSQL Deployment Guide

This guide provides step-by-step instructions to deploy the CricSQL AI Analytics Platform to production.

## Architecture Summary
* **Database**: MySQL on **Railway**
* **Backend**: FastAPI (Python) on **Render**
* **Frontend**: React (Vite) on **Netlify**

---

## Step 1: Deploy MySQL Database on Railway

1. **Create a Database**:
   * Go to [Railway](https://railway.app/) and sign in.
   * Click **New Project** -> **Provision MySQL**.
2. **Retrieve Connection Details**:
   * Click on the MySQL service in your Railway dashboard.
   * Go to the **Variables** tab or **Connect** tab.
   * Copy the **Private TCP Connection URL** (or External Connection URL if connecting from your local machine). It looks like:
     `mysql://root:password@host:port/railway`
3. **Format for SQLAlchemy**:
   * Change the prefix from `mysql://` to `mysql+pymysql://`.
   * For example, if Railway gives you:
     `mysql://root:abc123xyz@junction.proxy.rlwy.net:12345/railway`
   * Your `DATABASE_URL` should be:
     `mysql+pymysql://root:abc123xyz@junction.proxy.rlwy.net:12345/railway`
4. **Ingest Datasets (Run Ingestion Locally)**:
   * Temporarily update the `DATABASE_URL` in your local `.env` file with the Railway connection URL.
   * Run the ingestion script in your local terminal:
     ```powershell
     python backend/import_data.py
     ```
   * This will connect to your remote Railway database, create the necessary database schema, and upload all the IPL cricket datasets (over 50MB of data) from your local machine to Railway.
   * *Once completed, you can change your local `.env` database URL back to localhost if you wish.*

---

## Step 2: Deploy FastAPI Backend on Render

1. **Create Web Service**:
   * Go to [Render](https://render.com/) and sign in.
   * Click **New +** -> **Web Service**.
   * Connect your GitHub Repository: `https://github.com/Thomas09022006/NLP2SQL`.
2. **Configure Settings**:
   * **Name**: `cricsql-backend` (or similar)
   * **Region**: Choose one closest to you.
   * **Branch**: `main`
   * **Root Directory**: *Leave blank* (this lets Render run commands from the project root directory).
   * **Runtime**: `Python 3` (or Python 3.12/latest)
   * **Build Command**:
     ```bash
     pip install -r backend/requirements.txt
     ```
   * **Start Command**:
     ```bash
     python -m uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT
     ```
3. **Configure Environment Variables**:
   Click on **Advanced** or **Environment** and add the following variables:
   * `DATABASE_URL`: Your Railway MySQL connection URL (formatted with `mysql+pymysql://`).
   * `GEMINI_API_KEY`: Your Google AI Studio/Gemini API key.
   * `JWT_SECRET`: A long secure random string (e.g. `c22ea36f74a00bc7bbff62883b2fb7b65345a30fe539b4b9b6e8a4a39031c26b`).
   * `JWT_ALGORITHM`: `HS256`
   * `ACCESS_TOKEN_EXPIRE_MINUTES`: `60`
4. **Deploy**:
   * Click **Create Web Service**.
   * Render will build and deploy the backend. Copy the deployed service URL (e.g., `https://cricsql-backend.onrender.com`).

---

## Step 3: Deploy React Frontend on Netlify

1. **Create Site**:
   * Go to [Netlify](https://www.netlify.com/) and sign in.
   * Click **Add new site** -> **Import from Git**.
   * Select your GitHub account and choose the `NLP2SQL` repository.
2. **Configure Build Settings**:
   Netlify will automatically read the `netlify.toml` file in the root directory to configure the base directory and build commands, but verify they are:
   * **Base directory**: `frontend`
   * **Build command**: `npm run build`
   * **Publish directory**: `dist` (relative to the base directory `frontend`, resulting in `frontend/dist`)
3. **Configure Environment Variables**:
   Under **Site configuration** -> **Environment variables**, add:
   * `VITE_API_URL`: The URL of your deployed Render backend (e.g., `https://cricsql-backend.onrender.com`). Do not add a trailing slash.
4. **Deploy**:
   * Click **Deploy site**.
   * Netlify will build the app and provide a live URL (e.g., `https://cricsql.netlify.app`).

---

## Step 4: Verify Deployment

1. Open your Netlify frontend URL.
2. Register a new user account (this tests database connectivity and auth).
3. Try running a search query (e.g. *"Show Virat Kohli's average against spin in IPL 2024"*). This tests the Gemini SQL generator and MySQL executor.
