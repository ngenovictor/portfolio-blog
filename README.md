## Victor Ngeno
This repository contains the source code for my personal site. It has a frontend portfolio holder and a backend blog creater.

Can be accessed through [victorngeno.com](https://www.victorngeno.com)

**_Tech Used_**
1. HTML
2. CSS
3. Bootstrap 3.
4. Django
5. Docker

**_Running_**
- Local: `docker compose -f compose.local.yaml watch` — serves on http://localhost:8000 with the Django dev server and live sync of `./web`.
- Production: `docker compose -f compose.prod.yaml up -d --build` — expects the server's external Traefik on the `traefik-proxy` network (with the `https` entrypoint) and `PORTFOLIO_BLOG_SECRET_KEY` in `.env`. Routes `victorngeno.com` and `www.victorngeno.com`; the SQLite DB lives in the `portfolio_blog_data` volume.
