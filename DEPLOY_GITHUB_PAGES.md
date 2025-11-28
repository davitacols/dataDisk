# Deploy Landing Page to GitHub Pages

## Quick Setup (5 minutes)

### Step 1: Push to GitHub
```bash
git add .
git commit -m "Add landing page for GitHub Pages"
git push origin main
```

### Step 2: Enable GitHub Pages
1. Go to your GitHub repo: https://github.com/davitacols/dataDisk
2. Click **Settings** tab
3. Scroll to **Pages** section (left sidebar)
4. Under **Source**, select:
   - Branch: `main`
   - Folder: `/docs`
5. Click **Save**

### Step 3: Wait 2-3 minutes
GitHub will build and deploy your site automatically.

### Step 4: Access Your Site
Your landing page will be live at:
```
https://davitacols.github.io/dataDisk/
```

---

## Update Landing Page

To update the landing page:

1. Edit `landing_page.html`
2. Copy to docs folder:
   ```bash
   copy landing_page.html docs\index.html
   ```
3. Push changes:
   ```bash
   git add .
   git commit -m "Update landing page"
   git push
   ```

GitHub Pages will auto-update in 1-2 minutes.

---

## Custom Domain (Optional)

### Add Custom Domain:
1. Buy domain (e.g., datadisk.io from Namecheap)
2. In GitHub Settings → Pages → Custom domain
3. Enter: `datadisk.io`
4. Add DNS records at your domain provider:
   ```
   Type: A
   Name: @
   Value: 185.199.108.153
   
   Type: A
   Name: @
   Value: 185.199.109.153
   
   Type: A
   Name: @
   Value: 185.199.110.153
   
   Type: A
   Name: @
   Value: 185.199.111.153
   
   Type: CNAME
   Name: www
   Value: davitacols.github.io
   ```
5. Wait 24-48 hours for DNS propagation

---

## Update Streamlit App Link

Once deployed, update the landing page to link to your Streamlit app:

In `docs/index.html`, find and update:
```html
<a href="https://datadisk-healthcare.streamlit.app" class="btn btn-black">
    Try Live Demo
</a>
```

---

## Verify Deployment

Check if your site is live:
```
https://davitacols.github.io/dataDisk/
```

You should see:
- ✅ Landing page loads
- ✅ Images display correctly
- ✅ Buttons work
- ✅ Responsive on mobile

---

## Troubleshooting

### Site not loading?
- Wait 5 minutes after enabling GitHub Pages
- Check Settings → Pages shows green checkmark
- Verify `docs/index.html` exists in repo

### 404 Error?
- Make sure branch is `main` and folder is `/docs`
- Check file is named `index.html` (not `landing_page.html`)

### Images not loading?
- Use absolute URLs for images
- Or add images to `docs/` folder

---

## Next Steps

1. ✅ Deploy landing page to GitHub Pages
2. ✅ Deploy Streamlit app to Streamlit Cloud
3. ✅ Link landing page to Streamlit app
4. ✅ Share landing page URL in all marketing
5. ✅ Add Google Analytics (optional)

**Your landing page URL:**
```
https://davitacols.github.io/dataDisk/
```

**Your Streamlit app URL:**
```
https://datadisk-healthcare.streamlit.app
```

Share these links with prospects!
