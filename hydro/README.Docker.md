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

Your application will be available at http://localhost:8000.

To debug from VS Code, run `docker compose -f docker-compose.debug.yml up --build`
and attach a Python debugger to port 5678. The server starts once the debugger attaches.

### Parcel data

The Tulare parcels endpoint serves `divert/data/parcels/ca_tulare_cache.geojson`.
The raw shapefiles it is built from are multi-GB, so they are kept out of both git
and the image. Copy the cache file into place before building.

### Deploying your application to the cloud

Cloud hosts such as AWS Lightsail run amd64 (x86_64) machines. If you build on an
Apple Silicon Mac, build for that platform:
`docker build --platform=linux/amd64 -t taft .`.

Then push it to your registry, e.g. `docker push myregistry.com/taft`.

Set the variables from `.env` in the host's environment settings, entered without
the quote marks used in `.env`.

Consult Docker's [getting started](https://docs.docker.com/go/get-started-sharing/)
docs for more detail on building and pushing.

### References
* [Docker's Python guide](https://docs.docker.com/language/python/)
