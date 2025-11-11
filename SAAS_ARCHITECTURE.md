# 🏗️ Amazon Search Products - Arquitetura SaaS

## 📋 Visão Geral

Transformação do projeto atual em um **SaaS B2B completo** para análise de produtos da Amazon Brasil, com foco em empreendedores, vendedores marketplace e analistas de e-commerce.

---

## 🎯 Proposta de Valor

**Para quem:** Empreendedores digitais, vendedores Amazon, analistas de mercado
**Problema:** Dificuldade em encontrar produtos viáveis, analisar concorrência e identificar oportunidades de mercado
**Solução:** Plataforma SaaS com análise de dados em tempo real, alertas inteligentes, e insights acionáveis

---

## 📊 Modelo de Negócio

### Planos de Assinatura

| Plano | Preço/mês | Limites | Features |
|-------|-----------|---------|----------|
| **Free** | R$ 0 | 50 buscas/mês, 5 alertas | Dashboard básico, 2 categorias |
| **Pro** | R$ 97 | 1000 buscas/mês, 50 alertas | Todas categorias, exportação CSV, histórico 6 meses |
| **Business** | R$ 297 | 5000 buscas/mês, 200 alertas | API access, webhooks, histórico ilimitado, suporte prioritário |
| **Enterprise** | Custom | Ilimitado | White-label, SLA dedicado, customizações, multi-users |

---

## 🏛️ Arquitetura Técnica

### Stack Tecnológico

#### Backend
- **Framework:** FastAPI 0.110+ (async, high performance)
- **ORM:** SQLAlchemy 2.0+ (async)
- **Autenticação:** JWT (PyJWT) + OAuth2
- **Validação:** Pydantic V2
- **Task Queue:** Celery + Redis
- **Cache:** Redis 7+
- **Database:** PostgreSQL 15+

#### Frontend
- **Dashboard:** Streamlit (atual) + React (futuro)
- **Visualização:** Plotly + Chart.js
- **UI Components:** Streamlit Components customizados

#### Infraestrutura
- **Containerização:** Docker + Docker Compose
- **Orquestração:** Kubernetes (produção)
- **CI/CD:** GitHub Actions
- **Monitoramento:** Prometheus + Grafana
- **Logs:** ELK Stack (Elasticsearch, Logstash, Kibana)
- **Error Tracking:** Sentry
- **Cloud:** AWS (ou GCP/Azure)

---

## 📐 Estrutura do Projeto

```
amazon-search-products/
├── backend/                          # API REST FastAPI
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                   # FastAPI app
│   │   ├── config.py                 # Configurações
│   │   ├── dependencies.py           # DI containers
│   │   │
│   │   ├── api/                      # API routes
│   │   │   ├── v1/
│   │   │   │   ├── auth.py          # Login, register, JWT
│   │   │   │   ├── users.py         # User management
│   │   │   │   ├── products.py      # Product search & analysis
│   │   │   │   ├── subscriptions.py # Plans & billing
│   │   │   │   ├── alerts.py        # Price/stock alerts
│   │   │   │   ├── webhooks.py      # Webhook management
│   │   │   │   └── analytics.py     # Usage analytics
│   │   │   └── deps.py              # API dependencies
│   │   │
│   │   ├── core/                     # Core business logic
│   │   │   ├── security.py          # JWT, hashing, permissions
│   │   │   ├── rate_limiter.py      # Rate limiting
│   │   │   ├── stripe_client.py     # Payment integration
│   │   │   └── amazon_scraper.py    # Amazon API wrapper
│   │   │
│   │   ├── models/                   # Database models
│   │   │   ├── user.py
│   │   │   ├── subscription.py
│   │   │   ├── product.py
│   │   │   ├── alert.py
│   │   │   ├── search_history.py
│   │   │   └── webhook.py
│   │   │
│   │   ├── schemas/                  # Pydantic schemas
│   │   │   ├── user.py
│   │   │   ├── subscription.py
│   │   │   ├── product.py
│   │   │   └── alert.py
│   │   │
│   │   ├── services/                 # Business logic
│   │   │   ├── auth_service.py
│   │   │   ├── product_service.py
│   │   │   ├── subscription_service.py
│   │   │   ├── alert_service.py
│   │   │   └── analytics_service.py
│   │   │
│   │   ├── tasks/                    # Celery tasks
│   │   │   ├── scraper_tasks.py     # Background scraping
│   │   │   ├── alert_tasks.py       # Alert checking
│   │   │   └── report_tasks.py      # Report generation
│   │   │
│   │   ├── db/                       # Database
│   │   │   ├── base.py
│   │   │   ├── session.py
│   │   │   └── migrations/          # Alembic migrations
│   │   │
│   │   └── tests/                    # Unit & integration tests
│   │       ├── test_auth.py
│   │       ├── test_products.py
│   │       └── test_subscriptions.py
│   │
│   ├── Dockerfile
│   ├── requirements.txt
│   └── pytest.ini
│
├── frontend/                         # Streamlit Dashboard
│   ├── pages/
│   │   ├── 1_🏠_Dashboard.py
│   │   ├── 2_🔍_Buscar_Produtos.py
│   │   ├── 3_📊_Analise_Mercado.py
│   │   ├── 4_🔔_Alertas.py
│   │   ├── 5_⚙️_Configuracoes.py
│   │   └── 6_💳_Assinatura.py
│   ├── components/                   # Custom components
│   │   ├── auth_component.py
│   │   ├── charts.py
│   │   └── filters.py
│   ├── utils/
│   │   ├── api_client.py            # Backend API client
│   │   └── session_manager.py       # Auth session
│   ├── app.py                        # Main app
│   ├── Dockerfile
│   └── requirements.txt
│
├── worker/                           # Celery worker
│   ├── Dockerfile
│   └── celery_config.py
│
├── nginx/                            # Reverse proxy
│   ├── nginx.conf
│   └── Dockerfile
│
├── scripts/                          # Utility scripts
│   ├── init_db.py
│   ├── seed_data.py
│   └── migrate.sh
│
├── data/                             # Data storage (migrar para S3)
│   └── produtos/
│
├── docs/                             # Documentation
│   ├── API.md
│   ├── DEPLOYMENT.md
│   └── CONTRIBUTING.md
│
├── .github/
│   └── workflows/
│       ├── backend-ci.yml
│       ├── frontend-ci.yml
│       └── deploy.yml
│
├── docker-compose.yml                # Local development
├── docker-compose.prod.yml           # Production
├── .env.example
├── .gitignore
├── README.md
└── LICENSE
```

---

## 🔐 Sistema de Autenticação

### Fluxo de Auth
1. **Registro:** Email + senha → confirmação por email
2. **Login:** JWT access token (15min) + refresh token (7 dias)
3. **OAuth2:** Google, LinkedIn (futuro)
4. **2FA:** TOTP (planos Business+)

### Permissões (RBAC)
- `user`: Acesso básico ao dashboard
- `pro`: Recursos avançados
- `business`: API access
- `admin`: Painel administrativo

---

## 💾 Modelo de Dados

### Entidades Principais

#### Users
```python
- id: UUID (PK)
- email: String (unique)
- password_hash: String
- full_name: String
- company: String (nullable)
- subscription_id: FK
- is_active: Boolean
- email_verified: Boolean
- created_at: DateTime
- updated_at: DateTime
```

#### Subscriptions
```python
- id: UUID (PK)
- user_id: FK
- plan: Enum (free, pro, business, enterprise)
- status: Enum (active, canceled, past_due)
- current_period_start: DateTime
- current_period_end: DateTime
- stripe_subscription_id: String
- api_key: String (hashed)
```

#### Products (Cache)
```python
- id: UUID (PK)
- asin: String (indexed)
- title: String
- price: Decimal
- rating: Float
- num_ratings: Integer
- category: String
- sales_volume: Integer
- data_snapshot: JSONB
- fetched_at: DateTime
- expires_at: DateTime
```

#### Alerts
```python
- id: UUID (PK)
- user_id: FK
- product_asin: String
- alert_type: Enum (price_drop, stock, new_seller)
- threshold_value: Decimal
- is_active: Boolean
- last_triggered: DateTime
```

#### SearchHistory
```python
- id: UUID (PK)
- user_id: FK
- query: String
- filters: JSONB
- results_count: Integer
- searched_at: DateTime
```

---

## 🚀 APIs e Integrações

### API REST Endpoints

#### Autenticação
```
POST   /api/v1/auth/register
POST   /api/v1/auth/login
POST   /api/v1/auth/refresh
POST   /api/v1/auth/logout
GET    /api/v1/auth/me
```

#### Produtos
```
GET    /api/v1/products/search?q={query}&category={cat}&min_price={price}
GET    /api/v1/products/{asin}
GET    /api/v1/products/{asin}/history
POST   /api/v1/products/bulk-search
```

#### Alertas
```
GET    /api/v1/alerts
POST   /api/v1/alerts
PUT    /api/v1/alerts/{id}
DELETE /api/v1/alerts/{id}
```

#### Assinaturas
```
GET    /api/v1/subscriptions/plans
POST   /api/v1/subscriptions/checkout
POST   /api/v1/subscriptions/portal
GET    /api/v1/subscriptions/usage
```

#### Analytics
```
GET    /api/v1/analytics/dashboard
GET    /api/v1/analytics/trends?category={cat}&period={period}
POST   /api/v1/analytics/export
```

### Integrações Externas

1. **Amazon Real-Time Data API (RapidAPI)**
   - Rate limit: 1000 req/mês (Free) → 10000+ (Paid)
   - Implementar circuit breaker
   - Fallback para cache

2. **Stripe (Pagamentos)**
   - Checkout sessions
   - Customer portal
   - Webhooks para sincronização

3. **SendGrid (Emails)**
   - Confirmação de cadastro
   - Alertas de preço
   - Relatórios semanais

4. **AWS S3 (Storage)**
   - Histórico de dados
   - Exportações CSV/Excel
   - Backups

---

## ⚡ Performance e Escalabilidade

### Estratégias de Cache

#### Níveis de Cache
1. **Redis L1:** Dados de produtos (TTL: 1h)
2. **Redis L2:** Resultados de busca (TTL: 30min)
3. **CDN:** Assets estáticos (Cloudflare)

#### Rate Limiting
```python
Free:       10 req/min
Pro:        100 req/min
Business:   1000 req/min
Enterprise: Custom
```

### Background Tasks (Celery)

- **scrape_products**: Atualiza dados a cada 1h
- **check_alerts**: Verifica alertas a cada 15min
- **generate_reports**: Relatórios diários às 6am
- **cleanup_old_data**: Remove dados > 6 meses (Free)
- **send_digest_emails**: Emails semanais aos domingos

---

## 🔒 Segurança

### Boas Práticas Implementadas

1. **Secrets Management**
   - Variáveis de ambiente (.env)
   - AWS Secrets Manager (produção)
   - Nunca commitar secrets

2. **Proteção de API**
   - JWT com expiração curta
   - Rate limiting por IP/user
   - CORS configurado
   - Input validation (Pydantic)
   - SQL injection protection (SQLAlchemy)

3. **Dados Sensíveis**
   - Passwords: bcrypt (cost factor 12)
   - API keys: hashed no DB
   - PII: encrypted at rest

4. **Compliance**
   - LGPD: Direito ao esquecimento
   - Logs de acesso
   - Termos de uso + Privacy policy

---

## 📊 Monitoramento e Observabilidade

### Métricas-Chave (KPIs)

#### Negócio
- MRR (Monthly Recurring Revenue)
- Churn rate
- CAC (Customer Acquisition Cost)
- LTV (Lifetime Value)

#### Técnicas
- Uptime (SLA 99.9%)
- Latência p95, p99
- Error rate
- API success rate

### Tools
- **APM:** New Relic / Datadog
- **Logs:** Elasticsearch + Kibana
- **Errors:** Sentry
- **Uptime:** UptimeRobot
- **Alerts:** PagerDuty (Business+)

---

## 🚢 Deploy e DevOps

### Ambientes

1. **Development:** Local (Docker Compose)
2. **Staging:** AWS ECS (preview)
3. **Production:** AWS EKS (Kubernetes)

### CI/CD Pipeline

```yaml
Commit → GitHub Actions
  ↓
  Tests (pytest, coverage >80%)
  ↓
  Linting (flake8, black, mypy)
  ↓
  Security scan (bandit, safety)
  ↓
  Build Docker images
  ↓
  Push to ECR
  ↓
  Deploy to staging (auto)
  ↓
  Integration tests
  ↓
  Deploy to prod (manual approval)
  ↓
  Smoke tests
```

### Infraestrutura AWS

- **Compute:** ECS Fargate / EKS
- **Database:** RDS PostgreSQL (Multi-AZ)
- **Cache:** ElastiCache Redis
- **Storage:** S3 + CloudFront
- **Queue:** SQS (alternativa ao Redis)
- **Load Balancer:** ALB
- **DNS:** Route 53
- **Monitoring:** CloudWatch

---

## 📈 Roadmap de Desenvolvimento

### Fase 1: MVP (Semanas 1-4)
- ✅ Arquitetura base definida
- [ ] Backend FastAPI com auth
- [ ] Database models + migrations
- [ ] API endpoints principais
- [ ] Frontend Streamlit com login
- [ ] Docker Compose funcional

### Fase 2: Features Core (Semanas 5-8)
- [ ] Sistema de assinaturas
- [ ] Integração Stripe
- [ ] Rate limiting por plano
- [ ] Sistema de alertas
- [ ] Background tasks (Celery)
- [ ] Testes automatizados (>70% coverage)

### Fase 3: Scale & Polish (Semanas 9-12)
- [ ] Cache Redis otimizado
- [ ] CI/CD completo
- [ ] Monitoring e alerting
- [ ] Documentação API (Swagger)
- [ ] Deploy staging
- [ ] Load testing

### Fase 4: Launch (Semana 13+)
- [ ] Beta testing com 10 usuários
- [ ] Deploy produção
- [ ] Marketing website
- [ ] Onboarding flow
- [ ] Suporte ao cliente (Intercom)
- [ ] Analytics dashboard

### Fase 5: Growth (Meses 4-6)
- [ ] API pública
- [ ] Webhooks
- [ ] React frontend
- [ ] Mobile app (futuro)
- [ ] Integrações (Zapier, Make)
- [ ] White-label para enterprise

---

## 💰 Estimativa de Custos (Mensal)

### Infraestrutura
- AWS (staging + prod): ~$200
- RapidAPI (10K calls/mês): $100
- Stripe (fees): 2.9% + $0.30/transação
- SendGrid: $15 (40K emails)
- Sentry: $26 (Developer)
- Domínio + SSL: ~$10

**Total infra:** ~$351/mês + fees variáveis

### Break-even
- 4 clientes Pro ($97) = $388
- Lucro a partir de 5+ clientes

---

## 🎓 Boas Práticas de Código

### Python Standards
- **Style:** PEP 8 (black formatter)
- **Type hints:** Obrigatório (mypy)
- **Docstrings:** Google style
- **Async:** Sempre que possível
- **Tests:** pytest + coverage

### Git Workflow
- **Branches:** `main`, `develop`, `feature/*`
- **Commits:** Conventional Commits
- **PRs:** Obrigatório + review
- **Versioning:** Semantic Versioning

### Code Review Checklist
- [ ] Tests passam
- [ ] Coverage mantém >80%
- [ ] Sem secrets no código
- [ ] Documentação atualizada
- [ ] Performance adequada
- [ ] Security vulnerabilities resolvidas

---

## 📚 Documentação

### Docs Necessários
1. **README.md**: Setup rápido
2. **API.md**: Referência completa da API
3. **DEPLOYMENT.md**: Guia de deploy
4. **CONTRIBUTING.md**: Como contribuir
5. **CHANGELOG.md**: Histórico de versões
6. **ARCHITECTURE.md**: Este documento
7. **SECURITY.md**: Security policy

### User Docs
- Tutorials (video + texto)
- FAQ
- Troubleshooting
- API examples (Postman collection)

---

## 🤝 Suporte e Comunidade

### Canais
- **Email:** suporte@amazonanalytics.com.br
- **Discord:** Comunidade de usuários
- **GitHub Issues:** Bugs e feature requests
- **Status Page:** status.amazonanalytics.com.br

### SLA por Plano
- Free: Best effort (community)
- Pro: 48h response time
- Business: 24h response time
- Enterprise: 4h response time + phone support

---

## 📝 Próximos Passos

1. **Validar arquitetura** com stakeholders
2. **Configurar repositório** com estrutura definida
3. **Setup ambiente local** (Docker)
4. **Implementar backend MVP** (auth + products)
5. **Migrar frontend** para nova arquitetura
6. **Configurar CI/CD pipeline**
7. **Deploy em staging**
8. **Beta testing**
9. **Launch! 🚀**

---

**Documento mantido por:** Claude AI + Time de Desenvolvimento
**Última atualização:** 2025-11-11
**Versão:** 1.0.0
