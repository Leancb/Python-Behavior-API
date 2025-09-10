# Python Behavior API (Behave + Requests + Allure)

Automação BDD para APIs com **Behave**:
- **Status code, headers, tempo de resposta**
- **Validação de corpo (campos, tipos)**
- **Contrato via JSON Schema (jsonschema)**
- **Cenários positivos e negativos**
- **Allure Reports**
- **Docker + GitHub Actions**

## Requisitos
- Python 3.10+
- (Opcional) Allure CLI para abrir relatórios localmente

## Configuração
```bash
cp .env.example .env   # edite BASE_URL/REQUEST_TIMEOUT se quiser
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/Mac: source .venv/bin/activate
pip install -r requirements.txt
```

## Executar testes
```bash
behave -f pretty -f allure -o reports/allure-results
```

## Relatório Allure (local)
Instale o Allure CLI (https://docs.qameta.io/allure/#_get_started):
```bash
allure serve reports/allure-results
```

## Docker
```bash
docker build -t python-behavior-api:latest .
docker run --rm --env-file .env python-behavior-api:latest
```

## CI/CD (GitHub Actions)
- O workflow `API BDD CI` roda em cada push/PR:
  - Instala dependências
  - Executa o Behave
  - Publica **artifact** com `reports/allure-results`
- (Opcional) Você pode adicionar um job de publicação do Allure em Pages se desejar.
