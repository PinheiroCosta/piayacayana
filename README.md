# Coletivo Piaya Cayana - Monorepo

Monorepo para site institucional editorial com backend **Django 5 + DRF** e frontend **React + TypeScript + Webpack**.

## Estrutura

```text
/backend
/frontend
/infra
docker-compose.yml
.env.example
README.md
```

## Requisitos

- Docker + Docker Compose

## Setup local (1 comando)

```bash
cp .env.example .env
docker-compose up --build
```

Serviços locais:
- Frontend: http://localhost:3000
- Backend API/Admin: http://localhost:8000
- Admin: http://localhost:8000/admin

> O backend executa `migrate` automaticamente ao subir via Compose.

## Backend

- Python 3.12 / Django 5+
- DRF read-only para API pública
- Settings separados:
  - `config/settings/base.py`
  - `config/settings/dev.py`
  - `config/settings/prod.py`
- CORS por ambiente
- Segurança para proxy (Render):
  - `SECURE_PROXY_SSL_HEADER`
  - `USE_X_FORWARDED_HOST`
- Preview via token HMAC com expiração curta
- Upload com validações:
  - MIME type permitido
  - tamanho máximo
  - sanitização de nome de arquivo
- Produção com Cloudflare R2 via S3 compatible (`django-storages` + `boto3`)

### API pública

- `GET /api/public/pages/<slug>/`
- `GET /api/public/articles/`
- `GET /api/public/articles/<slug>/`
- `GET /api/public/events/`
- `GET /api/public/gallery/`

Preview:
- `GET /api/preview/articles/<slug>/?token=...`

## Frontend

- React 18 + TypeScript + Webpack manual
- React Router com rotas:
  - `/`
  - `/agenda`
  - `/galeria`
  - `/artigos`
  - `/artigos/:slug`
  - `/sobre`
  - `/contato`
  - `/preview/artigos/:slug?token=...`
- Renderização de Markdown com sanitização (`marked` + `dompurify`)
- Embed YouTube apenas por `video_id`
- Fallback SPA para Cloudflare Pages: `frontend/public/_redirects`

## Docker

`docker-compose.yml` inclui:
- `postgres`
- `backend` (runserver + migrate)
- `frontend` (webpack-dev-server + HMR)

## CI/CD (GitHub Actions)

Workflow único: `.github/workflows/ci-cd.yml`

Jobs:
- `backend-test`
- `frontend-build`
- `deploy-backend` (Render Deploy Hook)
- `deploy-frontend` (Cloudflare Pages com Wrangler)

Deploy condicional por mudanças de pasta:
- backend só se `backend/**` mudou
- frontend só se `frontend/**` mudou

## Variáveis de ambiente

Use `.env.example` como referência.

Principais blocos:
- Banco PostgreSQL
- Django (secret, hosts, CORS/CSRF, preview)
- Frontend (`API_BASE_URL`)
- R2 (bucket, endpoint, keys)
- Deploy (`RENDER_DEPLOY_HOOK_URL`, `CLOUDFLARE_*`)

## Cloudflare R2 (produção)

1. Criar bucket no painel Cloudflare R2.
2. Gerar Access Key + Secret.
3. Configurar no ambiente do backend:
   - `R2_BUCKET_NAME`
   - `R2_ENDPOINT_URL`
   - `R2_ACCESS_KEY_ID`
   - `R2_SECRET_ACCESS_KEY`
   - `R2_REGION=auto`
4. Garantir que o bucket possua política de leitura pública para arquivos publicados.

## Render (backend)

- Configure serviço web apontando para `/backend`.
- Build: `pip install -r requirements.txt`
- Start: `gunicorn config.wsgi:application --bind 0.0.0.0:$PORT`
- Variável obrigatória: `DJANGO_SETTINGS_MODULE=config.settings.prod`
- Defina todas as env vars de produção (DB, R2, secret, CSRF/CORS)

## Cloudflare Pages (frontend)

- Projeto apontando para monorepo, diretório `frontend`
- Build command: `npm run build`
- Output: `dist`
- Necessário `_redirects` para fallback SPA.

## Fluxo editorial (admin)

Grupos:
- **Administrador**: publica/despublica (`is_published`)
- **Editor**: cria e edita rascunhos

Conteúdo só entra na API pública quando `is_published=true`.
Galeria é derivada automaticamente de artigos/eventos com `show_in_gallery=true`.
