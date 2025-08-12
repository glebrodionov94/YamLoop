# YamLoop — оркестратор асинхронных задач по YAML

<!-- Badges (опционально, замените <group>/<project> своими) -->
[![pipeline status](https://gitlab.com/<group>/<project>/badges/main/pipeline.svg)](https://gitlab.com/<group>/<project>/-/pipelines)
[![coverage report](https://gitlab.com/<group>/<project>/badges/main/coverage.svg)](https://gitlab.com/<group>/<project>/-/graphs/master/charts)

Минималистичный раннер, который читает `config.yml`, динамически подключает модули из `modules/` и параллельно (через `asyncio`) запускает функции с параметрами. Подходит для сборки простых интеграций, задач планирования, опросов API и бэкенд-утилит.

---

## Возможности

- 📦 Загрузка Python-модулей по имени файла из каталога `modules/`
- ⚙️ Конфигурация через YAML: словари и списки параметров
- 🧵 Параллельный запуск задач с `asyncio.create_task`
- 🪪 Именование задач (`module.func.name` при наличии ключа `name`)
- 🧯 Корректная отмена задач и обработка `Ctrl+C`
- 🔎 Аккуратные сообщения об отсутствующих модулях/функциях

---
