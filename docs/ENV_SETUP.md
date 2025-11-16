# Инструкция по настройке .env файлов

## Backend (.env)

### 1. Создание файла

Скопируйте пример файла в `backend/.env`:

```bash
cd backend
cp .env.example .env
```

### 2. Обязательные параметры

#### `DJANGO_SETTINGS_MODULE`
- **Значение:** `core.settings.dev` (для разработки) или `core.settings.prod` (для продакшена)
- **Описание:** Указывает, какой файл настроек Django использовать
- **Пример:** `DJANGO_SETTINGS_MODULE=core.settings.dev`

#### `SECRET_KEY`
- **Значение:** Случайная строка для шифрования сессий и токенов
- **Описание:** **ОБЯЗАТЕЛЬНО измените в продакшене!** Используется для безопасности Django
- **Как получить:** 
  ```python
  from django.core.management.utils import get_random_secret_key
  print(get_random_secret_key())
  ```
- **Пример:** `SECRET_KEY=django-insecure-abc123xyz...` (для разработки)
- **⚠️ ВАЖНО:** Никогда не коммитьте реальный SECRET_KEY в Git!

#### `DEBUG`
- **Значение:** `1` (включено) или `0` (выключено)
- **Описание:** Режим отладки. В продакшене должно быть `0`
- **Пример:** `DEBUG=1` (для разработки)

#### `ALLOWED_HOSTS`
- **Значение:** Список доменов через запятую
- **Описание:** Домены, с которых разрешены запросы к серверу
- **Пример для разработки:** `ALLOWED_HOSTS=localhost,127.0.0.1`
- **Пример для продакшена:** `ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com`

#### `DATABASE_URL`
- **Для разработки (SQLite):**
  ```
  DATABASE_URL=sqlite:///db.sqlite3
  ```
  
- **Для продакшена (PostgreSQL):**
  ```
  DATABASE_URL=postgresql://username:password@localhost:5432/dbname
  ```
  Где:
  - `username` - имя пользователя PostgreSQL
  - `password` - пароль
  - `localhost:5432` - хост и порт (обычно localhost:5432)
  - `dbname` - имя базы данных

#### `CORS_ALLOWED_ORIGINS`
- **Значение:** URL фронтенда через запятую
- **Описание:** Разрешенные домены для CORS запросов
- **Пример для разработки:** `CORS_ALLOWED_ORIGINS=http://localhost:5173`
- **Пример для продакшена:** `CORS_ALLOWED_ORIGINS=https://yourdomain.com`

### 3. Опциональные параметры

#### RAG / GigaChat (для будущей интеграции)
```
GIGACHAT_BASE_URL=https://gigachat.api
GIGACHAT_API_KEY=your_gigachat_api_key
```
- Пока не используется, но можно настроить заранее

#### VK ID авторизация
```
VK_APP_ID=your_vk_app_id
```
- **Как получить:**
  1. Зайдите на https://dev.vk.com/
  2. Создайте приложение
  3. Скопируйте App ID
  4. В настройках приложения укажите redirect URL: `http://localhost:5173/profile` (для разработки)

#### Яндекс.Карты
```
YANDEX_MAPS_API_KEY=your_yandex_maps_api_key
```
- **Как получить:**
  1. Зайдите на https://developer.tech.yandex.ru/
  2. Создайте приложение
  3. Получите API ключ для JavaScript API
  4. Замените `YOUR_YANDEX_MAPS_API_KEY` в `frontend/index.html`

### 4. Пример полного .env для разработки

```env
# Django Settings
DJANGO_SETTINGS_MODULE=core.settings.dev
SECRET_KEY=dev-secret-key-change-me-in-production-12345
DEBUG=1
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=sqlite:///db.sqlite3

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:5173

# RAG / GigaChat (опционально)
GIGACHAT_BASE_URL=https://gigachat.api
GIGACHAT_API_KEY=dummy

# VK ID (опционально)
# VK_APP_ID=51962584

# Яндекс.Карты (опционально)
# YANDEX_MAPS_API_KEY=your_key_here
```

### 5. Пример полного .env для продакшена

```env
# Django Settings
DJANGO_SETTINGS_MODULE=core.settings.prod
SECRET_KEY=super-secret-production-key-min-50-chars-long-random-string
DEBUG=0
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database
DATABASE_URL=postgresql://dbuser:dbpassword@localhost:5432/rosatom_db

# CORS
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# RAG / GigaChat
GIGACHAT_BASE_URL=https://gigachat.api
GIGACHAT_API_KEY=real_gigachat_api_key

# VK ID
VK_APP_ID=your_real_vk_app_id

# Яндекс.Карты
YANDEX_MAPS_API_KEY=your_real_yandex_maps_key
```

---

## Frontend (.env.development)

### 1. Создание файла

```bash
cd frontend
echo "VITE_API_BASE_URL=http://localhost:8000/api/v1" > .env.development
```

### 2. Параметры

#### `VITE_API_BASE_URL`
- **Значение:** URL бэкенда API
- **Для разработки:** `VITE_API_BASE_URL=http://localhost:8000/api/v1`
- **Для продакшена:** `VITE_API_BASE_URL=https://api.yourdomain.com/api/v1`

#### `VITE_VK_APP_ID` (опционально)
- **Значение:** App ID из VK
- **Пример:** `VITE_VK_APP_ID=51962584`

### 3. Пример полного .env.development

```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_VK_APP_ID=51962584
```

---

## Безопасность

### ⚠️ ВАЖНО:

1. **Никогда не коммитьте .env файлы в Git!**
   - Убедитесь, что `.env` в `.gitignore`
   - Используйте `.env.example` для примера

2. **Используйте разные SECRET_KEY для разработки и продакшена**

3. **В продакшене:**
   - `DEBUG=0` (обязательно!)
   - Используйте сильный `SECRET_KEY`
   - Ограничьте `ALLOWED_HOSTS` только вашими доменами
   - Используйте HTTPS

4. **Храните секреты безопасно:**
   - Используйте переменные окружения на сервере
   - Или используйте менеджеры секретов (AWS Secrets Manager, HashiCorp Vault и т.д.)

---

## Проверка настроек

### Backend
```bash
cd backend
python manage.py check
python manage.py migrate
python manage.py runserver
```

Если всё работает, вы увидите:
```
Starting development server at http://127.0.0.1:8000/
```

### Frontend
```bash
cd frontend
npm run dev
```

Если всё работает, вы увидите:
```
  VITE v6.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
```

---

## Решение проблем

### Ошибка: "SECRET_KEY not set"
- Убедитесь, что файл `.env` существует в `backend/`
- Проверьте, что `SECRET_KEY` указан в файле

### Ошибка: "CORS error"
- Проверьте `CORS_ALLOWED_ORIGINS` в `backend/.env`
- Убедитесь, что URL фронтенда точно совпадает (включая порт)

### Ошибка: "Database connection failed"
- Проверьте `DATABASE_URL` в `backend/.env`
- Для PostgreSQL убедитесь, что база данных создана
- Проверьте права доступа пользователя БД

### Ошибка: "API request failed"
- Проверьте `VITE_API_BASE_URL` в `frontend/.env.development`
- Убедитесь, что бэкенд запущен
- Проверьте CORS настройки

