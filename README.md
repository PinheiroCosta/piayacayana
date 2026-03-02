# Coletivo Piaya Cayana — Monorepo

Monorepo com backend Django (DRF + OpenAPI) e frontend React + TypeScript + Webpack, preparado para desenvolvimento via Docker e deploy com GitHub Actions.

## Estrutura

```txt
/backend
/frontend
/infra
docker-compose.yml
.env.example
README.md
```

## Subir localmente (Docker)

1. Copie variáveis:
```bash
cp .env.example .env
```
2. Execute:
```bash
docker-compose up --build
```

Serviços:
- Backend: http://localhost:8000
- OpenAPI JSON: http://localhost:8000/api/schema/
- Swagger (somente dev): http://localhost:8000/api/docs/
- Frontend: http://localhost:3000
- Postgres: localhost:5432

## Backend (Poetry)

### Rodar sem Docker
```bash
cd backend
poetry install
poetry run python manage.py migrate
poetry run python manage.py runserver
```

### Gerar schema OpenAPI manualmente
```bash
cd backend
poetry run python manage.py spectacular --file ../openapi.json --settings=config.settings.dev
```

## Frontend

### Gerar tipos TypeScript manualmente
```bash
cd frontend
npm install
npx openapi-typescript ../openapi.json --output src/api/types.ts
```

## Fluxo editorial

- **Editor**: cria e edita rascunhos (não publica).
- **Administrador**: cria/edita/publica (`is_published`).
- Conteúdo público retorna somente `is_published=true`.
- Preview de artigo com token assinado em `/api/v1/preview/articles/<slug>/?token=...`.

## R2 (produção)

1. Criar bucket no Cloudflare R2.
2. Gerar credenciais S3 compatíveis.
3. Preencher variáveis `R2_*` e `USE_R2_STORAGE=true` no ambiente de produção.
4. Definir URL pública em `R2_PUBLIC_BASE_URL` (caso use domínio customizado/CDN).

## Deploy

- **Backend (Render)**: usar deploy hook (`RENDER_DEPLOY_HOOK_URL`).
- **Frontend (Cloudflare Pages)**: job usa `wrangler pages deploy`.
- **CI/CD**: workflow único em `.github/workflows/ci-cd.yml` com jobs:
  - `backend-test`
  - `generate-types`
  - `frontend-build`
  - `deploy-backend`
  - `deploy-frontend`

## Segurança

- `DEBUG=false` em produção (`config.settings.prod`).
- Proxy headers habilitados para Render.
- `CSRF_TRUSTED_ORIGINS`, CORS por ambiente.
- Cookies seguros em produção.
- Headers de segurança básicos habilitados.
- Secrets sempre via variáveis de ambiente.
