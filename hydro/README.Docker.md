### Setup

The app reads its secrets from environment variables. Before the first run,
copy the example file and fill in the values:

```sh
cp .env.example .env
```

| Variable | Purpose |
| --- | --- |
| `DJANGO_SECRET_KEY` | Django secret key. Generate one with `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"` |
| `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` | Postgres connection |

`.env` is git-ignored and excluded from the image by `.dockerignore`; Compose
passes it to the container at runtime. Never commit it.

### Building and running your application

From this folder (`hydro/`), run:
`docker compose up --build`.

This starts two containers: the Django app (gunicorn) and Caddy, which proxies to it
on ports 80/443. With `SITE_ADDRESS` unset, the app is at http://localhost/.
Both restart automatically after a crash or reboot.

To debug from VS Code, run `docker compose -f docker-compose.debug.yml up --build`
and attach a Python debugger to port 5678. The server starts once the debugger attaches.

### Parcel data

The Tulare parcels endpoint serves `divert/data/parcels/ca_tulare_cache.geojson`.
The raw shapefiles it is built from are multi-GB, so they are kept out of both git
and the image. Copy the cache file into place before building.

### Deploying to an AWS Lightsail instance

Build on the instance itself; it is amd64, so no cross-platform build or registry is needed.

1. In the Lightsail console, open ports **80** and **443** (Networking → IPv4 Firewall).
2. Install Docker: `curl -fsSL https://get.docker.com | sudo sh && sudo usermod -aG docker ubuntu`, then reconnect.
3. `git clone https://github.com/mflynn51/taft.git && cd taft/hydro`
4. Create `.env` from `.env.example`. Leave `DJANGO_DEBUG` off and set:
   - Plain HTTP on the instance IP: `DJANGO_ALLOWED_HOSTS=<instance IP>`.
   - HTTPS on a domain: point the domain's DNS A record at the instance's static IP, then set
     `SITE_ADDRESS=<domain>`, `DJANGO_ALLOWED_HOSTS=<domain>` and `DJANGO_HTTPS=True`.
     Caddy gets and renews the certificate itself.
5. Copy `ca_tulare_cache.geojson` into `divert/data/parcels/` (see above).
6. `docker compose up -d --build`

To update: `git pull && docker compose up -d --build`.

If you build elsewhere for an amd64 host, use
`docker build --platform=linux/amd64 -t taft .`. When a host takes environment
variables directly, enter the values without the quote marks used in `.env`.

### References
* [Docker's Python guide](https://docs.docker.com/language/python/)
