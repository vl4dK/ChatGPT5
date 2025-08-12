# ML Trading Bot

Everyday-adaptive crypto-trading bot (1H/4H) с ML, управлением риском и исполнением на Hyperliquid. Репозиторий собран так, чтобы отдельно конфигурировать данные, признаки, модели и исполнение — без правки кода.

## Возможности
- История OHLCV 1H/4H → parquet, проверка целостности
- Генератор признаков (TA + агрегирование на 4H)
- Разметка таргетов (future return / triple-barrier)
- Модели LightGBM/XGBoost, калибровка вероятностей
- Стратегия сигналов + position sizing (vol target/Kelly-lite)
- Риск-менеджмент: дневные лимиты, SL/TP/TSL
- Исполнение на Hyperliquid (REST/WebSocket), защита от токсичности
- FastAPI для интеграций и Streamlit UI для мониторинга
- Docker Compose для api+ui, cron для ежедневной адаптации
- Roadmap с M0–M5 (см. `ROADMAP.md`)

## Структура репо

```
.
├─ api/                 # FastAPI: /predict, /status, /signals
├─ monitoring/          # отчёты/ноутбуки/метрики (при желании)
├─ src/                 # ядро бота: данные → фичи → модели → стратегия → исполнение
├─ ui/                  # Streamlit-панель мониторинга/ручного контроля
│
├─ .env.example         # пример переменных окружения
├─ config.yaml          # общий конфиг: биржа, риск, пайплайны
├─ docker-compose.yml   # готовый запуск api+ui
├─ pyproject.toml       # зависимости/линтеры (PEP 621)
├─ requirements.txt     # альтернативно: pip install -r
├─ ROADMAP.md           # вехи проекта (M0–M5)
└─ README.md
```

> Примечание: внутри `src/` ожидаются подпакеты `data/`, `features/`, `labeling/`, `models/`, `strategy/`, `risk/`, `execution/`, а также CLI-скрипты (например, `src/cli/*.py`). Если каких-то модулей ещё нет — создадим по мере прохождения M-вех из `ROADMAP.md`.

## Быстрый старт

### 1) Зависимости
Вариант A (pip):
```bash
python -m venv .venv
source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

Вариант B (PEP 621 из `pyproject.toml`):
```bash
pip install --upgrade pip
pip install -e .
```

### 2) Переменные окружения
Скопируй и заполни:
```bash
cp .env.example .env
```

Минимум:
```
EXCHANGE=hyperliquid
HL_API_KEY=...           # ключи Hyperliquid
HL_API_SECRET=...
TRADING_SYMBOLS=BTC,ETH,SOL
DATA_DIR=./data
MODEL_DIR=./models
LOG_LEVEL=INFO
ENV=dev
```

### 3) Конфиг
`config.yaml` — единая точка настройки. Базовый пример:
```yaml
exchange: hyperliquid
symbols: ["BTC", "ETH", "SOL"]
timeframes:
  train: "1h"
  aggregate: "4h"
risk:
  max_daily_drawdown: 0.15
  max_notional: 10000
features:
  ta:
    - rsi: {period: 14}
    - ema: {periods: [9, 55, 100, 200]}
    - atr: {period: 14}
labels:
  type: future_return  # либо triple_barrier
  horizon: "4h"
model:
  kind: lgbm          # либо xgb
  params:
    num_leaves: 63
    learning_rate: 0.05
    n_estimators: 400
execution:
  mode: paper         # paper|live
  slippage_bps: 1.5
```

## Типичные команды

> Имена CLI-модулей даны как рекомендуемые. Если у тебя другие — поправь названия после `-m`.

Загрузка данных:
```bash
python -m src.cli.fetch --symbols BTC,ETH,SOL --tf 1h --since 2023-01-01
```

Построение признаков:
```bash
python -m src.cli.make_features --config config.yaml
```

Обучение модели:
```bash
python -m src.cli.train --config config.yaml --model lgbm
```

Бэктест:
```bash
python -m src.cli.backtest --config config.yaml
```

Запуск трейдера:
```bash
# paper
python -m src.cli.trade --mode paper --config config.yaml
# live
python -m src.cli.trade --mode live  --config config.yaml
```

API:
```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000
```

UI:
```bash
streamlit run ui/app.py
```

## Docker

Локально поднять API и UI:
```bash
docker compose up --build
```

Ожидается два сервиса:
- `api` на `:8000` (эндпоинты `/status`, `/predict`, `/signals`)
- `ui`  на `:8501` (мониторинг позиций, PnL, ручные действия)

Проброс секретов — через `.env` и переменные окружения в `docker-compose.yml`.

## Ежедневная адаптация

Добавь в cron/systemd (пример cron, запуск в 03:10):
```cron
10 3 * * * /bin/bash -lc 'cd /path/to/repo && source .venv/bin/activate && python -m src.cli.fetch --symbols BTC,ETH,SOL --tf 1h --since 2023-01-01 && python -m src.cli.make_features --config config.yaml && python -m src.cli.train --config config.yaml && python -m src.cli.backtest --config config.yaml >> logs/daily.log 2>&1'
```

Если нужен автодеплой артефактов модели — добавь шаг экспорта/версирования (папка `models/` + запись в `docs/MODELS.md`, если используешь).

## Тесты и качество
```bash
pytest -q
ruff check .
mypy src
```

## Безопасность и риск
- Начинай в `--mode paper`.  
- Проверь `max_notional`, `max_daily_drawdown`, стопы.  
- Перед `live` включи лимиты на стороне биржи, где возможно.

## Дорожная карта
Смотри `ROADMAP.md` — план M0…M5 и чек-листы задач.

## Лицензия
Укажи лицензию (MIT/Apache-2.0/частная). Если не уверены — начни с MIT и обнови позже.
