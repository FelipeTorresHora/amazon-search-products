# 🛒 Amazon Search Products - SaaS Platform

[![Backend CI/CD](https://github.com/FelipeTorresHora/amazon-search-products/actions/workflows/backend-ci.yml/badge.svg)](https://github.com/FelipeTorresHora/amazon-search-products/actions)
[![Frontend CI/CD](https://github.com/FelipeTorresHora/amazon-search-products/actions/workflows/frontend-ci.yml/badge.svg)](https://github.com/FelipeTorresHora/amazon-search-products/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> Plataforma SaaS B2B para análise de produtos da Amazon Brasil, com insights em tempo real, alertas inteligentes e inteligência de mercado para empreendedores digitais.

---

## 📋 Índice

- [Visão Geral](#-visão-geral)
- [Features](#-features)
- [Stack Tecnológico](#-stack-tecnológico)
- [Arquitetura](#-arquitetura)
- [Quick Start](#-quick-start)
- [Desenvolvimento](#-desenvolvimento)
- [Deploy](#-deploy)
- [API Documentation](#-api-documentation)
- [Planos e Preços](#-planos-e-preços)
- [Contribuindo](#-contribuindo)
- [License](#-license)

---

## 🎯 Visão Geral

**Amazon Search Products** é uma plataforma SaaS completa que ajuda empreendedores, vendedores marketplace e analistas de e-commerce a:

- 🔍 **Buscar e analisar** milhares de produtos da Amazon Brasil
- 📊 **Identificar oportunidades** de mercado com dados em tempo real
- 🔔 **Receber alertas** automáticos de mudanças de preço e estoque
- 📈 **Visualizar tendências** com dashboards interativos
- 💡 **Tomar decisões** baseadas em dados concretos

### Problema que Resolvemos

Encontrar produtos viáveis para vender online é difícil. Nossa plataforma centraliza dados da Amazon Brasil e oferece insights acionáveis para acelerar decisões de negócio.

---

## ✨ Features

### Core Features
- ✅ Busca avançada com múltiplos filtros (preço, categoria, rating)
- ✅ Dashboard interativo com métricas em tempo real
- ✅ Análise de 5 categorias principais (Eletrônicos, Beleza, Pet, Brinquedos, Construção)
- ✅ Exportação de dados (CSV, Excel)
- ✅ Histórico de preços e tendências

### Pro Features
- 🔔 Alertas de preço e estoque (email + webhook)
- 📊 Análise competitiva avançada
- 📈 Relatórios personalizados
- 🔄 Atualizações em tempo real

### Business+ Features
- 🚀 API REST completa
- 🔗 Webhooks customizados
- 👥 Multi-usuário (em breve)
- 🎨 White-label (Enterprise)

---

## 🛠️ Stack Tecnológico

### Backend
- **Framework:** FastAPI (Python 3.11+)
- **Database:** PostgreSQL 15
- **Cache:** Redis 7
- **Task Queue:** Celery + Redis
- **ORM:** SQLAlchemy 2.0 (async)
- **Auth:** JWT (PyJWT)

### Frontend
- **Framework:** Streamlit 1.31
- **Visualização:** Plotly, Pandas
- **UI:** Custom Streamlit Components

### DevOps
- **Containerização:** Docker + Docker Compose
- **CI/CD:** GitHub Actions
- **Cloud:** AWS (ECS/EKS)
- **Monitoring:** Sentry, Prometheus, Grafana

### Integrações
- Amazon Real-Time Data API (RapidAPI)
- Stripe (pagamentos)
- SendGrid (emails)
- AWS S3 (storage)

---

## 🏗️ Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                         NGINX                               │
│                    (Reverse Proxy)                          │
└───────────────────┬─────────────────────────────────────────┘
                    │
        ┌───────────┴───────────┐
        │                       │
┌───────▼────────┐    ┌────────▼────────┐
│   Frontend     │    │    Backend      │
│  (Streamlit)   │◄───┤   (FastAPI)     │
└────────────────┘    └────────┬────────┘
                               │
            ┌──────────────────┼──────────────────┐
            │                  │                  │
    ┌───────▼───────┐  ┌──────▼──────┐  ┌───────▼────────┐
    │  PostgreSQL   │  │    Redis    │  │  Celery Worker │
    │   (Database)  │  │   (Cache)   │  │  (Background)  │
    └───────────────┘  └─────────────┘  └────────────────┘
```

Para arquitetura detalhada, veja [SAAS_ARCHITECTURE.md](./SAAS_ARCHITECTURE.md).

---

## 🚀 Quick Start

### Pré-requisitos

- Docker & Docker Compose
- Python 3.11+ (para desenvolvimento local)
- Git

### Instalação Rápida

```bash
# 1. Clone o repositório
git clone https://github.com/FelipeTorresHora/amazon-search-products.git
cd amazon-search-products

# 2. Configure variáveis de ambiente
cp .env.example .env
# Edite .env com suas credenciais

# 3. Inicie todos os serviços
docker-compose up -d

# 4. Acesse a aplicação
# Frontend: http://localhost:8501
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/api/v1/docs
# Flower (Celery): http://localhost:5555
```

### Verificar Status

```bash
# Ver logs de todos os serviços
docker-compose logs -f

# Verificar health
curl http://localhost:8000/health

# Parar todos os serviços
docker-compose down
```

---

## 💻 Desenvolvimento

### Setup Local (sem Docker)

#### Backend

```bash
cd backend

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Configurar banco de dados
# Certifique-se que PostgreSQL está rodando
alembic upgrade head

# Rodar servidor
uvicorn app.main:app --reload --port 8000
```

#### Frontend

```bash
cd frontend

# Instalar dependências
pip install -r requirements.txt

# Rodar Streamlit
streamlit run app.py
```

### Estrutura do Projeto

```
amazon-search-products/
├── backend/              # API FastAPI
│   ├── app/
│   │   ├── api/          # Endpoints
│   │   ├── core/         # Core logic
│   │   ├── models/       # Database models
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── services/     # Business logic
│   │   └── tasks/        # Celery tasks
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/             # Streamlit Dashboard
│   ├── pages/            # Multi-page app
│   ├── components/       # Custom components
│   └── utils/            # Helper functions
├── worker/               # Celery worker config
├── nginx/                # Reverse proxy
├── docs/                 # Documentation
├── scripts/              # Utility scripts
├── .github/workflows/    # CI/CD
└── docker-compose.yml
```

### Comandos Úteis

```bash
# Backend
make test                  # Run tests
make lint                  # Run linters
make format                # Format code
make migrate              # Run migrations

# Frontend
streamlit run app.py --server.port 8501

# Docker
docker-compose up -d                    # Start all
docker-compose logs -f backend          # View logs
docker-compose exec backend bash        # SSH into container
docker-compose down -v                  # Stop and remove volumes
```

### Testes

```bash
# Backend tests
cd backend
pytest app/tests/ -v --cov=app

# Com coverage report
pytest --cov=app --cov-report=html

# Frontend tests (smoke tests)
cd frontend
python -m py_compile app.py
```

---

## 🚢 Deploy

### Variáveis de Ambiente Necessárias

```bash
# Essenciais
DATABASE_URL=postgresql://...
REDIS_URL=redis://...
SECRET_KEY=your-secret-key
RAPIDAPI_KEY=your-rapidapi-key

# Pagamentos
STRIPE_SECRET_KEY=sk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...

# Email
SENDGRID_API_KEY=SG...

# Monitoring
SENTRY_DSN=https://...
```

### Deploy na AWS (ECS)

```bash
# 1. Build e push das imagens
docker build -t amazon-search-backend:latest ./backend
docker tag amazon-search-backend:latest <account>.dkr.ecr.us-east-1.amazonaws.com/backend:latest
docker push <account>.dkr.ecr.us-east-1.amazonaws.com/backend:latest

# 2. Deploy via GitHub Actions (automático)
git push origin main  # Triggers deploy pipeline

# 3. Ou manualmente via AWS CLI
aws ecs update-service --cluster prod --service backend --force-new-deployment
```

### Deploy no Heroku (alternativa simples)

```bash
# Backend
heroku create amazon-search-api
heroku addons:create heroku-postgresql:standard-0
heroku addons:create heroku-redis:premium-0
git subtree push --prefix backend heroku main

# Frontend
heroku create amazon-search-app
git subtree push --prefix frontend heroku main
```

---

## 📚 API Documentation

### Base URL
```
Production: https://api.amazonanalytics.com.br/api/v1
Staging: https://staging-api.amazonanalytics.com.br/api/v1
Local: http://localhost:8000/api/v1
```

### Autenticação

```bash
# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "senha123"}'

# Resposta
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer"
}

# Usar token
curl -X GET http://localhost:8000/api/v1/products/search?q=notebook \
  -H "Authorization: Bearer eyJhbGc..."
```

### Endpoints Principais

#### Produtos
- `GET /products/search` - Buscar produtos
- `GET /products/{asin}` - Detalhes do produto
- `GET /products/{asin}/history` - Histórico de preço

#### Alertas
- `GET /alerts` - Listar alertas
- `POST /alerts` - Criar alerta
- `DELETE /alerts/{id}` - Remover alerta

#### Analytics
- `GET /analytics/dashboard` - Métricas do dashboard
- `GET /analytics/trends` - Tendências de mercado

Documentação completa: http://localhost:8000/api/v1/docs

---

## 💰 Planos e Preços

| Plano | Preço/mês | Buscas | Alertas | Histórico | API | Suporte |
|-------|-----------|---------|---------|-----------|-----|---------|
| **Free** | R$ 0 | 50 | 5 | 30 dias | ❌ | Community |
| **Pro** | R$ 97 | 1.000 | 50 | 6 meses | ❌ | Email (48h) |
| **Business** | R$ 297 | 5.000 | 200 | Ilimitado | ✅ | Email (24h) |
| **Enterprise** | Custom | ♾️ | ♾️ | Ilimitado | ✅ | Phone (4h) |

[Saiba mais sobre os planos →](https://amazonanalytics.com.br/pricing)

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor, leia [CONTRIBUTING.md](./docs/CONTRIBUTING.md) para detalhes.

### Como Contribuir

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

### Code Style

- Python: PEP 8, Black formatter, type hints
- Commits: [Conventional Commits](https://www.conventionalcommits.org/)
- Tests: Obrigatório para novas features (coverage > 80%)

---

## 📝 Documentação Adicional

- [Arquitetura SaaS Completa](./SAAS_ARCHITECTURE.md)
- [API Reference](./docs/API.md)
- [Deployment Guide](./docs/DEPLOYMENT.md)
- [Security Policy](./SECURITY.md)
- [Changelog](./CHANGELOG.md)

---

## 📞 Suporte

- **Email:** suporte@amazonanalytics.com.br
- **Discord:** [Join our community](https://discord.gg/amazonanalytics)
- **Issues:** [GitHub Issues](https://github.com/FelipeTorresHora/amazon-search-products/issues)
- **Status:** [status.amazonanalytics.com.br](https://status.amazonanalytics.com.br)

---

## 📄 License

Este projeto está licenciado sob a licença MIT - veja [LICENSE](./LICENSE) para detalhes.

---

## 🎉 Roadmap

### Q1 2025
- [x] Arquitetura SaaS planejada
- [x] Backend FastAPI MVP
- [ ] Sistema de autenticação completo
- [ ] Integração Stripe

### Q2 2025
- [ ] Launch Beta
- [ ] API Pública v1
- [ ] React Dashboard (migração do Streamlit)
- [ ] Mobile App (React Native)

### Q3 2025
- [ ] Integração com Zapier/Make
- [ ] White-label para Enterprise
- [ ] Multi-marketplace (Mercado Livre, Shopee)

---

## 👏 Agradecimentos

- [FastAPI](https://fastapi.tiangolo.com/) - Framework incrível
- [Streamlit](https://streamlit.io/) - Dashboard rápido
- [RapidAPI](https://rapidapi.com/) - API Amazon
- Comunidade Python Brasil

---

<div align="center">

**Feito com ❤️ por [Felipe Torres](https://github.com/FelipeTorresHora)**

⭐ Star este projeto se ele te ajudou!

</div>
