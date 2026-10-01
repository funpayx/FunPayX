# Как контрибьютить в проект

Рад любой помощи. Чтобы всем было комфортно, придерживаемся простых правил.

## Локальная установка
1. Сделай fork репозитория и склонируй себе.
2. Создай и активируй виртуальное окружение:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Для Windows: venv\Scripts\activate
3. Установи зависимости:   
    ```bash
    pip install -r requirements.txt
    ```
4. Создай новую ветку под свою задачу. Называй логично, например feature/название-фичи или fix/суть-бага:
    ```bash
    git checkout -b feature/cool-new-stuff
    ```
