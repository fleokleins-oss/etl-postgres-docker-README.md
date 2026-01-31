# ETL Pipeline - PostgreSQL + Docker

Pipeline ETL completo demonstrando extração, transformação e carga de dados usando Python, PostgreSQL e Docker.

## 🎯 Objetivo

Demonstrar um pipeline de dados production-ready com:
- Extração de dados de múltiplas fontes
- Transformações SQL e Python
- Validação de qualidade de dados
- Containerização com Docker
- Logs e monitoramento

## 🏗️ Arquitetura

```
┌─────────────┐
│   Sources   │ (APIs, CSVs, DBs)
└──────┬──────┘
       │ Extract
       ▼
┌─────────────┐
│  Staging    │ (Raw data)
│  PostgreSQL │
└──────┬──────┘
       │ Transform
       ▼
┌─────────────┐
│ Data Marts  │ (Analytics-ready)
│  PostgreSQL │
└─────────────┘
```

## 🚀 Quick Start

### Pré-requisitos
- Docker e Docker Compose instalados
- Python 3.9+

### Executar o Pipeline

```bash
# 1. Clone o repositório
git clone https://github.com/fleokleins-oss/etl-postgres-docker.git
cd etl-postgres-docker

# 2. Subir o banco de dados
docker-compose up -d

# 3. Instalar dependências Python
pip install -r requirements.txt

# 4. Executar o ETL
python src/etl.py
```

### Verificar Resultados

```bash
# Conectar ao PostgreSQL
docker exec -it etl-postgres psql -U postgres -d analytics

# Ver dados transformados
SELECT * FROM marts.daily_metrics LIMIT 10;
```

## 📁 Estrutura do Projeto

```
etl-postgres-docker/
├── docker-compose.yml       # Setup PostgreSQL + Adminer
├── requirements.txt         # Dependências Python
├── README.md               # Este arquivo
│
├── src/
│   ├── etl.py             # Pipeline principal
│   ├── extract.py         # Módulo de extração
│   ├── transform.py       # Módulo de transformação
│   ├── load.py            # Módulo de carga
│   └── config.py          # Configurações
│
├── sql/
│   ├── schema.sql         # DDL do banco
│   ├── staging/           # Queries de staging
│   └── marts/             # Queries de marts
│
└── tests/
    ├── test_extract.py
    ├── test_transform.py
    └── test_quality.py
```

## 🔧 Componentes

### Extract
- Lê dados de APIs públicas (exemplo: JSONPlaceholder)
- Suporta CSVs e bancos de dados externos
- Tratamento de erros e retry logic

### Transform
- Limpeza de dados (nulls, duplicatas, outliers)
- Agregações e joins
- Enriquecimento de dados
- Validações de qualidade

### Load
- Inserção incremental (upsert)
- Partition por data
- Índices otimizados
- Logs de execução

## 📊 Dados de Exemplo

O pipeline processa dados de usuários e posts:

**Staging (Raw):**
```sql
staging.users      -- Dados brutos de usuários
staging.posts      -- Dados brutos de posts
```

**Marts (Analytics-ready):**
```sql
marts.daily_metrics       -- Métricas diárias agregadas
marts.user_summary        -- Resumo por usuário
marts.post_analytics      -- Analytics de posts
```

## 🧪 Validações de Qualidade

```python
# Exemplos de validações implementadas
- not_null: campos obrigatórios
- unique: unicidade de IDs
- relationships: integridade referencial
- accepted_values: domínios válidos
- custom_sql: regras de negócio
```

## 📈 Monitoramento

O pipeline gera logs estruturados:

```json
{
  "timestamp": "2025-01-31T10:30:00",
  "stage": "extract",
  "status": "success",
  "records": 100,
  "duration_seconds": 2.5
}
```

## 🔄 Agendamento

Para produção, use Apache Airflow ou cron:

```bash
# Exemplo cron: rodar diariamente às 3am
0 3 * * * cd /path/to/project && python src/etl.py
```

## 🐛 Troubleshooting

**Erro: "Connection refused"**
```bash
# Verificar se o PostgreSQL está rodando
docker ps | grep postgres

# Ver logs do container
docker logs etl-postgres
```

**Erro: "Duplicate key violation"**
```bash
# Limpar dados de staging e reprocessar
python src/etl.py --clean
```

## 📚 Próximos Passos

- [ ] Adicionar suporte a S3/GCS para staging
- [ ] Implementar Airflow DAG
- [ ] Adicionar dashboards com Metabase/Superset
- [ ] Testes de integração com pytest
- [ ] CI/CD com GitHub Actions

## 🛠️ Stack Tecnológica

- **Language:** Python 3.9+
- **Database:** PostgreSQL 14
- **Container:** Docker, Docker Compose
- **Libraries:** pandas, SQLAlchemy, psycopg2
- **Testing:** pytest

## 📄 Licença

MIT License - use livremente para estudos e projetos.

## 🤝 Contribuições

Pull requests são bem-vindos! Para grandes mudanças, abra uma issue primeiro.

## 📧 Contato

- GitHub: [@fleokleins-oss](https://github.com/fleokleins-oss)
- LinkedIn: [seu-perfil](https://linkedin.com/in/seu-perfil)

---

**Nota:** Este é um projeto de demonstração para portfolio. Em produção, considere:
- Secrets management (não hardcode credenciais)
- Observability tools (DataDog, Prometheus)
- Data catalog (Apache Atlas, Amundsen)
- Testes mais abrangentes
