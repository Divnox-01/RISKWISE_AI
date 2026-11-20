# RISKWISE AI 2.0 — Windows 11 Step-by-Step Setup Guide

This guide explains how to extract, configure, and execute RISKWISE AI 2.0 on a Windows 11 machine with strict storage constraints (e.g. keeping all virtual environments and project files on `D:\` drive).

---

## Step 1: Download & Extract Archive to D: Drive

1. Download `RISKWISE_AI_2.0.zip`.
2. Open PowerShell as Administrator or standard user.
3. Create target directory on `D:\` drive:
   ```powershell
   New-Item -ItemType Directory -Force -Path "D:\real_projects"
   ```
4. Extract the ZIP into `D:\real_projects\`:
   ```powershell
   Expand-Archive -Path "$HOME\Downloads\RISKWISE_AI_2.0.zip" -DestinationPath "D:\real_projects\RISKWISE_AI_2.0" -Force
   Set-Location -Path "D:\real_projects\RISKWISE_AI_2.0"
   ```

---

## Step 2: Configure Python Virtual Environment on D: Drive

Ensure your virtual environment stays on D: drive to preserve C: drive space:
```powershell
# Create venv on D: drive with site packages
python -m venv .venv --system-site-packages

# Activate venv
.\.venv\Scripts\Activate.ps1

# Install backend dependencies
.\.venv\Scripts\pip install -r backend/requirements.txt
```

---

## Step 3: Initialize Database & Seed Transactions

Run the seeding script to create `riskwise.db` with demo accounts and historical data:
```powershell
$env:PYTHONPATH="backend"
.\.venv\Scripts\python backend/app/database/seed.py
```

---

## Step 4: Start the FastAPI Backend

```powershell
$env:PYTHONPATH="backend"
.\.venv\Scripts\uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```
Leave this PowerShell terminal running. The backend is now serving at `http://127.0.0.1:8000`.

---

## Step 5: Start the React Frontend

Open a second PowerShell window:
```powershell
Set-Location -Path "D:\real_projects\RISKWISE_AI_2.0\frontend"

# Install node modules directly on D: drive
npm install

# Start Vite development server
npm run dev
```
The dashboard is now live at: `http://localhost:5173`.

---

## Step 6: Log In & Explore

Open your browser to `http://localhost:5173/login`:
- Click **"Admin"** (Email: `admin@riskwise.ai`, Pass: `Admin@123`) or **"Analyst"**
- Click **"Sign In to Platform"**
- Navigate to **"Live Inference"** (`/analyze`) and try testing the preset fraud scenarios!
