# Python Behavior API (Behave + Requests + Allure)

Projeto configurado com **x-api-key do ReqRes** já preenchida (`reqres-free-v1`) no `.env` e no CI.

## Rodar local
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/Mac: source .venv/bin/activate
pip install -r requirements.txt

# (opcional) edite .env para outra BASE_URL/KEY
behave -f pretty -o stdout -f allure -o reports/allure-results
```

## Allure
```bash
allure serve reports/allure-results
```

## Docker
```bash
docker build -t python-behavior-api:latest .
docker run --rm --env-file .env python-behavior-api:latest
```

## CI
O workflow já exporta `REQRES_API_KEY=reqres-free-v1`.
```yaml
env:
  BASE_URL: https://reqres.in
  REQUEST_TIMEOUT: 10
  REQRES_API_KEY: reqres-free-v1
```
