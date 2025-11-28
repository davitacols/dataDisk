# 🚀 Deploy Test Suite Online (No-Code for Clinics)

## Option 1: Streamlit Cloud (FREE - Recommended)

### Step 1: Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/davitacols/dataDisk.git
git push -u origin main
```

### Step 2: Deploy on Streamlit Cloud
1. Go to https://share.streamlit.io
2. Sign in with GitHub
3. Click "New app"
4. Select:
   - Repository: `davitacols/dataDisk`
   - Branch: `main`
   - Main file: `app_healthcare.py`
5. Click "Deploy"

**Result:** You get a public URL like:
`https://datadisk-healthcare.streamlit.app`

**Share with clinics:**
```
Test dataDisk Healthcare (no installation required):
https://datadisk-healthcare.streamlit.app

1. Click "Load Sample Dataset" or upload your CSV
2. Click "De-identify Data"
3. Download results

Questions? Email support@datadisk.io
```

---

## Option 2: Heroku (FREE Tier)

### Step 1: Create Procfile
```bash
echo "web: streamlit run app_healthcare.py --server.port=$PORT" > Procfile
```

### Step 2: Deploy
```bash
heroku login
heroku create datadisk-healthcare
git push heroku main
```

**URL:** `https://datadisk-healthcare.herokuapp.com`

---

## Option 3: Railway (FREE)

1. Go to https://railway.app
2. Click "New Project" → "Deploy from GitHub"
3. Select your repo
4. Add start command: `streamlit run app_healthcare.py`
5. Deploy

**URL:** Auto-generated Railway URL

---

## Option 4: Replit (Easiest - No Git Required)

1. Go to https://replit.com
2. Click "Create Repl"
3. Import from GitHub: `davitacols/dataDisk`
4. Click "Run"

**URL:** `https://datadisk-healthcare.username.repl.co`

---

## Recommended: Streamlit Cloud

**Why:**
- ✅ FREE forever
- ✅ Auto-updates from GitHub
- ✅ Custom domain support
- ✅ Built for Streamlit apps
- ✅ No credit card required

**Setup time:** 5 minutes

---

## After Deployment

### Update Landing Page
Add test link to `landing_page.html`:

```html
<a href="https://datadisk-healthcare.streamlit.app" class="btn btn-black">
    Try Live Demo
</a>
```

### Update Email Templates
```
Subject: Test dataDisk Healthcare (No Installation)

Hi [Name],

Try dataDisk Healthcare in your browser (no installation):
👉 https://datadisk-healthcare.streamlit.app

1. Upload your CSV or use sample data
2. Click "De-identify Data"
3. Download results

Takes 2 minutes. No credit card required.

Questions? Just reply.

Best,
[Your Name]
```

### Add to All Marketing
- Landing page CTA
- Email signatures
- LinkedIn posts
- Reddit comments
- Product Hunt

---

## Security Note

For production/paid customers:
- Deploy on private infrastructure
- Add authentication
- Use HTTPS
- Enable audit logging
- Add rate limiting

For free trial/demo:
- Public Streamlit Cloud is fine
- Add disclaimer: "Demo only - not for PHI"
- Limit file size to 1MB
- Clear data after processing

---

## Quick Deploy Now

```bash
# 1. Push to GitHub
git init
git add .
git commit -m "Healthcare de-identification platform"
git push

# 2. Go to share.streamlit.io
# 3. Deploy app_healthcare.py
# 4. Get URL: https://datadisk-healthcare.streamlit.app

# 5. Share with clinics!
```

**Done in 5 minutes!**
