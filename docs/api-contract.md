## REST API Contract (v1)

> Базовый URL: `/api/v1`  
> Формат: JSON (UTF-8).  
> Статусы: стандартные HTTP. Ошибки - `{ "detail": "..." }`.

### Общие модели

```json
City {
  "id": integer,
  "slug": "sarov",
  "name": "Саров",
  "region": "Нижегородская область"
}

ActivityCategory {
  "id": integer,
  "name": "Экология",
  "description": "..."
}
```

### Справочники
| Endpoint | Метод | Описание |
| --- | --- | --- |
| `/cities/` | GET | список городов (фильтр по `?active=true`) |
| `/activity-categories/` | GET | категории направлений |

### НКО
```json
Organization {
  "id": 12,
  "name": "Экологический центр «Зелёный мир»",
  "slug": "eco-green-world",
  "tagline": "Охрана природы",
  "description": "...",
  "city": City,
  "categories": [ActivityCategory],
  "email": "info@example.com",
  "phone": "+7 999 111-22-33",
  "website": "https://...",
  "logo_url": "https://...",
  "cover_image": "https://...",
  "status": "published", // draft|pending|published|rejected
  "is_featured": false,
  "updated_at": "2025-11-15T11:35:00Z"
}
```

| Endpoint | Метод | Описание |
| --- | --- | --- |
| `/organizations/` | GET | Фильтры: `?city=slug`, `?category=id`, `?featured=true`, `?search=строка` |
| `/organizations/{slug}/` | GET | Детали + связанные события/материалы |
| `/organizations/` | POST (auth, role=`nko_owner`) | Создать черновик (`draft`) |
| `/organizations/{id}/` | PATCH/PUT (owner) | Обновить; `status` меняет модератор |
| `/organizations/{id}/submit/` | POST (owner) | Отправить на модерацию → `pending` |
| `/organizations/{id}/moderate/` | POST (moderator/admin) | `{"action": "approve"|"reject", "comment": ""}` |

### События
```json
Event {
  "id": 4,
  "title": "...",
  "description": "...",
  "city": City,
  "organization": Organization (light),
  "start_at": "2025-11-25T10:00:00Z",
  "end_at": "2025-11-25T13:00:00Z",
  "venue": "Городской парк",
  "categories": [ActivityCategory],
  "registration_url": null,
  "status": "published",
  "is_featured": false
}
```

| Endpoint | Метод | Описание |
| --- | --- | --- |
| `/events/` | GET | Фильтры: `?city=slug`, `?category=id`, `?featured=true`, `?from=2025-11-10`, `?to=` |
| `/events/{id}/` | GET | Детали |
| `/events/` | POST (owner/moderator) | Создать (draft) |
| `/events/{id}/register/` | POST (auth) | Записаться |
| `/event-registrations/` | GET (auth) | Мои события |
| `/events/{id}/moderate/` | POST (moderator) | approve/reject |

### Новости
```json
NewsItem {
  "id": 9,
  "title": "...",
  "slug": "eco-grant-2025",
  "excerpt": "...",
  "content": "...",
  "city": City | null,
  "cover_image": "...",
  "attachment_url": "...",
  "published_at": "2025-11-12T09:00:00Z",
  "author": "Администратор",
  "is_featured": true
}
```

| Endpoint | Метод | Описание |
| --- | --- | --- |
| `/news/` | GET | Фильтры: `?city=slug`, `?featured=true`, `?search=` |
| `/news/{slug}/` | GET | Детали |
| `/news/` | POST (moderator) | Создать |
| `/news/{id}/` | PATCH/DELETE (moderator) | Управление |

### База знаний
```json
Material {
  "id": 3,
  "title": "...",
  "summary": "...",
  "body": "...",
  "file_url": "https://...",
  "cover_image": "...",
  "type": "video|document|article|link",
  "categories": [MaterialCategory],
  "city": City|null,
  "is_published": true,
  "updated_at": "..."
}
```

| Endpoint | Метод | Описание |
| --- | --- | --- |
| `/materials/` | GET | Фильтры: `?category=id`, `?city=slug`, `?type=video` |
| `/materials/{id}/` | GET | Детали |
| `/materials/` | POST (moderator) | Создать |
| `/materials/{id}/` | PATCH/DELETE |

### Пользователи и авторизация

| Endpoint | Метод | Описание |
| --- | --- | --- |
| `/auth/register/` | POST | `{"email","password","role"}` |
| `/auth/login/` | POST | Возвращает Tokens/JWT |
| `/auth/logout/` | POST | Инвалидация токена |
| `/auth/me/` | GET | Профиль, роли, избранное |
| `/favorites/` | GET/POST/DELETE | Управление избранными НКО/новостями/материалами |

### Модерация
| Endpoint | Метод | Описание |
| --- | --- | --- |
| `/moderation/organizations/` | GET (mod) | `status=pending` |
| `/moderation/events/` | GET (mod) |  |
| `/moderation/materials/` | GET (mod) |  |
| `/moderation/organizations/{id}/moderate/` | POST | `{"action":"approve","comment":""}` |

### Ассистент (без RAG)
| Endpoint | Метод | Описание |
| --- | --- | --- |
| `/assistant/query/` | POST (auth) | `{"question","context_type","context_id"}` → stub ответ |

