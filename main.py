import asyncio
import sys
from pathlib import Path
import importlib.util

import yaml  # pip install pyyaml

# Пути
BASE_DIR    = Path(__file__).parent
MODULES_DIR = BASE_DIR / 'modules'
CONFIG_PATH = BASE_DIR / 'config.yml'


def load_config(path: Path = CONFIG_PATH) -> dict:
    if not path.exists():
        print(f"Конфиг {path!s} не найден", file=sys.stderr)
        sys.exit(1)
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def import_module_from_path(name: str, filepath: Path):
    """
    Динамически загружает .py-файл как модуль с именем name.
    """
    spec = importlib.util.spec_from_file_location(name, str(filepath))
    if spec is None or spec.loader is None:
        raise ImportError(f"Невозможно создать spec для {filepath}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


async def run_tasks_from_config(config: dict):
    tasks = []
    for module_name, funcs in config.items():
        module_path = MODULES_DIR / f"{module_name}.py"
        if not module_path.exists():
            print(f"Модуль '{module_name}.py' не найден", file=sys.stderr)
            continue

        module = import_module_from_path(module_name, module_path)
        for func_name, params in funcs.items():
            func = getattr(module, func_name, None)
            if func is None:
                continue

            # Если params — список, то запускаем func отдельно для каждого элемента
            if isinstance(params, list):
                for single in params:
                    coro = func(**single)
                    task = asyncio.create_task(coro, name=f"{module_name}.{func_name}.{single.get('name','')}")
                    tasks.append(task)
                    print(f"Запущена задача {module_name}.{func_name} для {single} ")
            else:
                coro = func(**params)
                task = asyncio.create_task(coro, name=f"{module_name}.{func_name}")
                tasks.append(task)
                print(f"Запущена задача {module_name}.{func_name} с args {params}")

    if not tasks:
        print("Нет задач для запуска.", file=sys.stderr)
        return

    try:
        await asyncio.gather(*tasks)
    except asyncio.CancelledError:
        for t in tasks:
            t.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)
        print("Все задачи отменены.")


def main():
    config = load_config()
    try:
        asyncio.run(run_tasks_from_config(config))
    except KeyboardInterrupt:
        # пользователь нажал Ctrl+C
        print("\nПрограмма прервана пользователем.")


if __name__ == '__main__':
    main()
