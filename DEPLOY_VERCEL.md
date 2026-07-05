# Deploying to Vercel

This project can run on Vercel as a Python serverless function. Two files
make this work, already included:

- `api/index.py` — re-exports the Flask `app` object so Vercel's Python
  runtime can find it.
- `vercel.json` — tells Vercel to route every request to that function and
  to bundle the `templates/` folder along with it.

## ⚠️ Important limitation: upload size

Vercel serverless functions **reject request bodies larger than ~4.5 MB**
(this is a hard platform limit, not something `MAX_CONTENT_LENGTH` in
`app.py` controls, and it applies on every plan, including Pro). That's
fine for images, but most videos are bigger than that — a post with a
video attached will fail with a `413`/timeout on Vercel even though the
exact same code works locally or on PythonAnywhere/Render/Railway.

If you need real video uploads to work reliably, you have two options:

1. **Don't use Vercel for this app.** Deploy the Flask app as-is to a host
   that runs a normal long-lived server process (Render, Railway, Fly.io,
   a VPS, or PythonAnywhere — see `DEPLOY_PYTHONANYWHERE.md`). No code
   changes needed.
2. **Keep Vercel, but upload directly to storage from the browser**
   (e.g. request a signed upload URL and have the phone upload the video
   straight to S3/Cloudflare R2/etc., then send Vercel just that file's
   URL). This is a bigger change to `app.py` and `index.html` — ask if you
   want this built out.

This guide covers option 1 style deployment onto Vercel for testing with
images/small clips; just know that large videos won't go through.

## Steps

1. **Push this project to a GitHub repo** (Vercel deploys from Git).

   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

2. **Import the repo in Vercel**

   - Go to https://vercel.com/new
   - Select your repo
   - Framework preset: choose "Other" (Vercel will detect the Python
     function automatically from `vercel.json`)

3. **Set environment variables**

   In the Vercel project's Settings → Environment Variables, add:

   | Name               | Value                          |
   |--------------------|---------------------------------|
   | `ZERNIO_API_KEY`   | your real Zernio API key        |
   | `FLASK_SECRET_KEY` | any long random string          |

   (Don't upload your `.env` file — Vercel injects these directly.)

4. **Deploy**

   Click Deploy. Vercel will install `requirements.txt` and build the
   function. Once it finishes, you'll get a URL like
   `https://your-project.vercel.app`.

5. **Test**

   Open the URL on your Android phone, try both "📷 Choose Image" and
   "🎥 Choose Video" buttons, and confirm both open the correct picker and
   show a preview. Send a post with a small image first before trying a
   video, given the size limit above.

## Redeploying after changes

Any `git push` to the connected branch triggers a new Vercel deployment
automatically — no manual steps needed.
