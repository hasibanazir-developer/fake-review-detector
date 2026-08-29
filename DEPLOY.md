# Deploying to Vercel + Supabase (free tier)

**Steps 1 and 2 are already done** — the Supabase database is live, the schema is
migrated and your data is loaded. What's left is steps 3 and 4.

---

## ✅ 1. Supabase database — DONE

- Project: `dygovygdtwlpigliarsn`, region `ap-northeast-1`, PostgreSQL 17.6
- All 19 migrations applied
- Data loaded: **5 users, 9 products, 11 reviews** (passwords carried over as hashes)
- Verified through the transaction pooler: every page returns 200, and a full
  register → login → post-review flow works, sentiment scoring included

Two things had to be handled in `settings.py`:

- The password contains `#`, which starts the fragment part of a URL, so it is
  percent-encoded as `%23`.
- Supabase's pooler URL ends in `?pgbouncer=true` — a Prisma flag that psycopg
  rejects as an unknown connection option. Settings strips it automatically, so
  you can paste either form of the URL.

---

## ✅ 2. Product images — DONE (no Supabase Storage needed)

Vercel's filesystem is read-only, so uploaded files can't be written at runtime.
Instead of paying that complexity, the 9 existing images are served straight out
of the deployed bundle by **WhiteNoise** — the same library that already serves
the Django admin's CSS. No bucket, no S3 keys, no extra service.

The images moved from `Product_Images/` to **`public/Product_Images/`**, and
`MEDIA_ROOT` now points at `public/`. The URLs are unchanged
(`/Product_Images/<file>`), so no database rows needed updating.

`WHITENOISE_ROOT` is deliberately set to `public/` rather than the project root —
pointing it at the root would publish `settings.py` and the database file too.

> **Trade-off:** adding a product *with a new image* from the live admin panel
> will not work, because nothing can be written to disk on Vercel. Add it locally
> instead, then commit and push — the image ships with the deployment.

---

## 3. Push the code to GitHub

This folder is not a git repo yet:

```bash
git init
git add .
git commit -m "Fake review detector"
git branch -M main
git remote add origin https://github.com/<you>/<repo>.git
git push -u origin main
```

`.gitignore` keeps `db.sqlite3`, `__pycache__` and `.env` out. Two folders **are**
committed on purpose:

- `staticfiles/` — so Vercel needs no build step
- `public/` — the product images

---

## 4. Deploy on Vercel

1. <https://vercel.com> → **Add New → Project** → import the GitHub repo.
2. Framework preset: **Other**. Leave build settings empty — `vercel.json` handles it.
3. Add these **Environment Variables**, then deploy:

| Name | Value |
|---|---|
| `SECRET_KEY` | a long random string (see below) |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `.vercel.app` |
| `CSRF_TRUSTED_ORIGINS` | `https://*.vercel.app` |
| `DATABASE_URL` | `postgresql://postgres.dygovygdtwlpigliarsn:<PASSWORD>@aws-0-ap-northeast-1.pooler.supabase.com:6543/postgres` |

Replace `<PASSWORD>` with your Supabase database password, **percent-encoded**.
Punctuation has to be escaped or the URL parses wrongly — `#` in particular
silently truncates everything after it:

| character | becomes |
|---|---|
| `#` | `%23` |
| `*` | `%2A` |
| `@` | `%40` |
| `$` | `%24` |

To encode it without guessing:

```bash
python -c "from urllib.parse import quote; print(quote(input('password: '), safe=''))"
```

Note the port: **6543** (transaction pooler) for the running site. Port 5432 was
only used for the one-off migration.

Generate the secret key with:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## After deploying

- Site: `https://<project>.vercel.app`
- Admin: `https://<project>.vercel.app/admin/`

**Changed templates or static files?** Re-run collectstatic and push:

```bash
python manage.py collectstatic --noinput
git add -A && git commit -m "update" && git push
```

**Changed models?** Run the migration locally against Supabase first — Vercel
cannot run migrations:

```bash
# Git Bash
export DATABASE_URL="postgresql://postgres.dygovygdtwlpigliarsn:<PASSWORD>@aws-0-ap-northeast-1.pooler.supabase.com:5432/postgres"
python manage.py migrate
```

```powershell
# PowerShell
$env:DATABASE_URL = "postgresql://postgres.dygovygdtwlpigliarsn:<PASSWORD>@aws-0-ap-northeast-1.pooler.supabase.com:5432/postgres"
python manage.py migrate
```

Use port **5432** (session pooler) for migrations. Open a new terminal afterwards
so `DATABASE_URL` is unset and local development goes back to SQLite.

---

## Free-tier notes

- **Supabase** pauses a free project after roughly a week of no activity. Restore
  it from the dashboard when that happens — nothing is lost.
- **Vercel Hobby** is non-commercial use only, which fits a university project.

---

## Security

No password or secret key is written in this file, or in any other file that
gets committed — they live only in Vercel's environment variables. Keep it that
way. After the project is submitted it is still worth resetting the database
password (Supabase → Project Settings → Database → Reset password).

---

## Troubleshooting

| Symptom | Cause |
|---|---|
| `DisallowedHost` | `ALLOWED_HOSTS` missing your domain |
| CSRF failure on login | `CSRF_TRUSTED_ORIGINS` not set to `https://*.vercel.app` |
| `too many connections` | using the direct `5432` URL for the site — switch to `6543` |
| Product images 404 | `public/` folder wasn't committed |
| Admin has no CSS | `staticfiles/` wasn't committed |
| `relation "..." does not exist` | migrations weren't run against Supabase |
