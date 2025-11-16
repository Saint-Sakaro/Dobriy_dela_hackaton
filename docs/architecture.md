## Архитектурная схема экранов (ТЗ №3 «Добрые дела Росатома»)

Требовалась именно «карта окон»: без дизайна, только перечень экранов и все переходы между ними. Ниже — полный набор схем в формате mermaid, чтобы их можно было сразу вставить в документацию или инструменты визуализации.

---

### 1. Общая карта проекта: все экраны и связи

```mermaid
flowchart LR
    %% Публичный раздел
    subgraph Public["Публичная зона"]
        Landing["Э01 · Главная"]
        City["Э02 · Выбор города (виджет)"]
        NKOList["Э03 · Список НКО"]
        NKODetail["Э04 · Страница НКО"]
        Knowledge["Э05 · База знаний"]
        KnowledgeItem["Э05a · Материал детально"]
        Calendar["Э06 · Календарь событий"]
        Event["Э07 · Событие детально"]
        News["Э08 · Новости"]
        NewsDetail["Э09 · Новость детально"]
        Contacts["Э10 · Контакты / FAQ"]
        Auth["Э11 · Вход / Регистрация"]
    end

    %% Личный кабинет пользователя / НКО
    subgraph UserCab["Личный кабинет пользователя"]
        Dashboard["Э12 · Дашборд"]
        Favorites["Э13 · Избранное"]
        SavedNKO["Э13a · Сохранённые НКО"]
        SavedEvents["Э13b · Сохранённые события"]
        SavedMaterials["Э13c · Сохранённые материалы"]
        MyOrg["Э14 · Моя НКО"]
        EventForm["Э15 · Добавить событие"]
        MaterialsUpload["Э16 · Загрузить материал в базу"]
        Profile["Э17 · Профиль и настройки"]
    end

    %% Интерфейс модератора/админа
    subgraph Admin["Админ / модератор"]
        AdminAuth["Э18 · Вход администратора"]
        AdminHome["Э19 · Панель администратора"]
        Moderation["Э20 · Очередь модерации\n(НКО / события / материалы)"]
        ContentMgmt["Э21 · Управление новостями и базой знаний"]
        CityRef["Э22 · Справочники (города, категории)"]
        Users["Э23 · Пользователи и роли"]
    end

    Landing -->|"CTA «Выбрать город»"| City
    Landing -->|"CTA «НКО»"| NKOList
    Landing -->|"CTA «База знаний»"| Knowledge
    Landing -->|"CTA «Календарь»"| Calendar
    Landing -->|"CTA «Новости»"| News
    Landing -->|"Вход"| Auth
    Landing --> Contacts

    City --> NKOList
    City --> Calendar
    City --> News
    City --> Knowledge

    NKOList -->|"Открыть карту"| NKODetail
    NKODetail -->|"Добавить в избранное"| Auth

    Knowledge -->|"Открыть материал"| KnowledgeItem
    KnowledgeItem -->|"Скачать/смотреть"| Auth

    Calendar -->|"Подробнее о событии"| Event
    Event -->|"Хочу участвовать / в избранное"| Auth

    News -->|"Читать далее"| NewsDetail

    Auth --> Dashboard

    Dashboard --> Favorites
    Dashboard --> NKOList
    Dashboard --> Knowledge
    Dashboard --> Calendar
    Dashboard --> News
    Dashboard --> MyOrg
    Dashboard --> EventForm
    Dashboard --> MaterialsUpload
    Dashboard --> Profile

    Favorites --> SavedNKO
    Favorites --> SavedEvents
    Favorites --> SavedMaterials

    MyOrg -->|"Создать/редактировать"| Dashboard
    EventForm -->|"Отправить на модерацию"| Dashboard
    MaterialsUpload -->|"Отправить на модерацию"| Dashboard

    AdminAuth --> AdminHome
    AdminHome --> Moderation
    AdminHome --> ContentMgmt
    AdminHome --> CityRef
    AdminHome --> Users

    Moderation -->|"Одобрить"| Public
    Moderation -->|"Отклонить"| AdminHome
    ContentMgmt -->|"Опубликовать"| Public
```

---

### 2. Публичные экраны: детальная схема переходов

```mermaid
flowchart TD
    Landing["Э01 · Главная\n— герой-блок, описание портала"]
    CityWidget["Э02 · Выбор города\n— dropdown / карта / поиск"]
    Blocks["Блоки CTA\n— НКО · База знаний · Календарь · Новости"]
    Footer["Футер\n— контакты Росатома, соцсети"]

    NKOList["Э03 · Список НКО\n— фильтры по городу, направлению"]
    NKODetail["Э04 · Страница НКО\n— поля из ТЗ"]

    Knowledge["Э05 · База знаний\n— категории, теги"]
    KnowledgeItem["Э05a · Материал\n— видео/PDF/ссылки"]

    Calendar["Э06 · Календарь\n— вид календарь + список"]
    EventDetail["Э07 · Событие\n— описание, место, контакты"]

    NewsFeed["Э08 · Новости\n— фильтр по городу"]
    NewsDetail["Э09 · Новость детально"]

    Contacts["Э10 · Контакты / FAQ"]

    Landing --> CityWidget
    Landing --> Blocks
    Blocks --> NKOList
    Blocks --> Knowledge
    Blocks --> Calendar
    Blocks --> NewsFeed
    NKOList --> NKODetail
    Knowledge --> KnowledgeItem
    Calendar --> EventDetail
    NewsFeed --> NewsDetail
    Landing --> Contacts
```

---

### 3. Личный кабинет пользователя / НКО

```mermaid
flowchart LR
    Dashboard["Э12 · Дашборд\n— последние новости, события, рекомендации"]
    Favorites["Э13 · Избранное"]
    SavedNKO["Сохранённые НКО"]
    SavedEvents["Сохранённые события"]
    SavedMaterials["Сохранённые материалы"]
    MyOrg["Э14 · Моя НКО"]
    OrgForm["Форма редактирования НКО"]
    EventForm["Э15 · Добавить событие"]
    MaterialsUpload["Э16 · Добавить материал"]
    Profile["Э17 · Профиль и настройки"]

    Dashboard -->|"Кнопка «Избранное»"| Favorites
    Favorites --> SavedNKO
    Favorites --> SavedEvents
    Favorites --> SavedMaterials

    Dashboard -->|"«Создать / редактировать НКО»"| MyOrg
    MyOrg --> OrgForm
    OrgForm -->|"Отправить (модерация)"| Dashboard

    Dashboard -->|"«Добавить событие»"| EventForm
    EventForm -->|"Сохранить" (→ модерация)| Dashboard

    Dashboard -->|"«Добавить материал»"| MaterialsUpload
    MaterialsUpload -->|"Сохранить» (→ модерация)"| Dashboard

    Dashboard -->|"«Профиль»"| Profile
    Profile -->|"Сохранить"| Dashboard
```

---

### 4. Интерфейс администратора и модерации

```mermaid
flowchart TD
    AdminAuth["Э18 · Вход администратора"]
    AdminHome["Э19 · Главная администратора\n— статистика, уведомления"]
    Moderation["Э20 · Очередь модерации\n— вкладки: НКО | События | Материалы"]
    ContentMgmt["Э21 · Управление контентом\n— Новости, База знаний"]
    CityRef["Э22 · Справочники\n— города, направления, категории"]
    Users["Э23 · Пользователи и роли"]

    AdminAuth --> AdminHome
    AdminHome --> Moderation
    AdminHome --> ContentMgmt
    AdminHome --> CityRef
    AdminHome --> Users

    Moderation -->|"Одобрить"| Public
    Moderation -->|"Отклонить"| AdminHome
    ContentMgmt -->|"Опубликовать"| Public
    CityRef --> AdminHome
    Users --> AdminHome
```

---

### Применение схем
- Каждый узел = отдельный экран/окно, как требовалось. Номера можно сохранить для макетов и задач («Э05» = базовый идентификатор).
- Стрелки показывают переходы (кнопки, ссылки, CTA). Подписи добавлены только там, где есть неоднозначность.
- Для нашей «фишки» (RAG-помощник на GigaChat) можно добавить ещё один экран и соединить его с `Landing`, `NKODetail`, `Dashboard`, `AdminHome` без изменения логики остальных блоков.

---

## Интеграция RAG / GigaChat

### Точки входа на фронтенде
- **Плавающая кнопка «Спросить помощника»**: отображается на `Landing`, `NKOList`, `Knowledge`, `Calendar`, `News`, `Dashboard`, `MyOrg`, `AdminHome`.
- **Контекстные CTA**:
  - `Э04 · Страница НКО` → «Спросить про эту НКО».
  - `Э05a · Материал` → «Пояснить материал».
  - `Э07 · Событие` → «Помочь подготовиться».
  - `Э14 · Моя НКО` / `Э15 · Добавить событие` → генерация черновиков описаний.
- **Админка**: подсказки при модерации («Суммаризировать заявку», «Проверить факты»).

### Функциональные сценарии
1. **Справочная помощь пользователю** — вопрос по НКО/событию/материалу с автоматическим подставлением контекста (ID записи, ссылки на источники).
2. **Генерация черновиков** — для НКО/событий/новостей помощник предлагает структуру текста, проверяет соответствие брендбуку.
3. **Админ-модерация** — резюмирование новых заявок, подсказки по критериям проверки.
4. **FAQ/Поиск** — RAG возвращает не только ответ, но и список документов с подсветкой релевантных частей.

### Архитектура потока данных

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant Backend as Django API
    participant RAG as RAG Service (FastAPI/ML)
    participant VectorDB as Qdrant/FAISS
    participant GigaChat

    User->>Frontend: Вводит вопрос / жмёт CTA
    Frontend->>Backend: POST /assistant/query {question, context_id, user_id}
    Backend->>RAG: gRPC/HTTP запрос с токеном GigaChat
    RAG->>VectorDB: Поиск релевантных фрагментов (по городу, типу контента)
    RAG->>GigaChat: Prompt (вопрос + контекст)
    GigaChat-->>RAG: Ответ + токены
    RAG-->>Backend: Форматированный ответ, источники, метаданные
    Backend-->>Frontend: JSON {answer, sources, latency, trace_id}
    Frontend-->>User: Отображение ответа + ссылки на документы
```

### Компоненты
- `ml/ingest.py` — загрузка ТЗ, контента сайта, минуток и новостей → нарезка и запись в VectorDB.
- `ml/rag_service.py` — FastAPI-сервис, инкапсулирующий эмбеддинги, поиск и вызовы GigaChat.
- `backend/assistant/` — Django app c REST endpoint, авторизацией, хранением истории запросов.
- `frontend/src/features/assistant` — виджет чата + контекстные кнопки.

### Технические заметки
- **Контекст**: используем фильтры по городу/типу контента, чтобы ответы были специфичны.
- **Кэширование**: популярные вопросы (FAQ) кешируются в Redis, но всегда можно запросить RAG для уточнений.
- **Безопасность**: токены GigaChat и сервисные ключи в `.env`, трафик между Backend ↔ RAG только внутри VPC/докер-сети.
- **Трекинг качества**: логируем промпты/ответы (без персональных данных) в `assistant_logs` для дебага и метрик.

Такую схему можно расширить под live-стриминг ответов (Server-Sent Events/WebSocket) или голосовой интерфейс, если останется время.

### Что дальше
1. Сверить список экранов с оригинальным ТЗ ( `docs/tz.txt` ) — если появятся новые требования, добавляем новые узлы.
2. Перенести схемы в Miro/Figma и подписать пользовательские сценарии для каждой аудитории (жители, НКО, модераторы).
3. На базе номеров экранов разбить задачи между фронтом, бэком и ML (например, «Э05 — API каталога материалов»).

