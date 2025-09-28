# Social Media Feed Backend

A modern Django 5.2 backend providing GraphQL API, WebSocket notifications, and REST endpoints for a social media feed application. Built with Django Channels, GraphQL, and JWT authentication.

---

## Features

- 🔐 JWT-based Authentication (GraphQL + REST)
- 📱 GraphQL API (Graphene-Django)
- ⚡ Real-time WebSocket notifications
- 🗄️ PostgreSQL database
- 🚀 Redis for caching and channels
- 🐳 Docker & Docker Compose support
- ✅ Comprehensive test suite
- 🔄 Signal-based cache invalidation
- 📝 Pre-commit hooks (black/isort/flake8)

---

## Tech Stack

- Django 5.2
- Python 3.12
- GraphQL (Graphene)
- Django Channels
- PostgreSQL
- Redis
- Docker
- JWT Authentication

---

## Quick Start

### Local Development

1. **Create and activate virtual environment:**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1  # Windows
source .venv/bin/activate     # Unix
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Setup environment:**
```bash
cp .env.example .env
# Edit .env with your settings
```

4. **Run migrations:**
```bash
python manage.py migrate
```

5. **Create superuser:**
```bash
python manage.py createsuperuser
```

6. **Run development server:**
```bash
python manage.py runserver
# Or for WebSocket support:
daphne -b 0.0.0.0 -p 8000 config.asgi:application
```

### Docker Deployment  & docker-compose


1. **Build and run:**
```bash
docker-compose up --build
```

2. **Access services:**
- GraphQL Playground: http://localhost:8000/graphql/
- WebSocket: ws://localhost:8000/ws/notifications/
- Health Check: http://localhost:8000/health/

---

## GraphQL API

### Authentication

```graphql
mutation TokenAuth {
  tokenAuth(username: "user", password: "pass") {
    token
    refreshToken
  }
}

mutation RefreshToken {
  refreshToken(refreshToken: "token") {
    token
  }
}
```

### Posts

```graphql
# Create Post
mutation {
  createPost(content: "Hello World!") {
    post {
      id
      content
      createdAt
      author {
        username
      }
    }
  }
}

# Query Feed
query {
  feed(first: 10) {
    edges {
      node {
        id
        content
        createdAt
        author {
          username
        }
        likesCount
        commentsCount
        sharesCount
      }
    }
  }
}
```

### Interactions

```graphql
# Like Post
mutation {
  likePost(postId: "1") {
    success
    post {
      id
      likesCount
    }
  }
}

# Add Comment
mutation {
  createComment(postId: "1", content: "Great post!") {
    comment {
      id
      content
      author {
        username
      }
    }
  }
}
```

---

## WebSocket Notifications / real-time notifications (Channels)

Connect to WebSocket with JWT authentication:

```javascript
const ws = new WebSocket(
  "ws://localhost:8000/ws/notifications/?token=<YOUR_JWT_TOKEN>"
);

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Received:', data);
};
```

subscription {
  notifications {
    text
    postId
    interactionType
  }
}

Notification types:
- `POST_LIKED`
- `NEW_COMMENT`
- `MENTION`
- `FOLLOW`

---

## Project Structure

```
Social-Media-Feed-Backend/
├── config/ # Project Configuration
│ ├── asgi.py # ASGI entry point
│ ├── schema.py # Root GraphQL schema (combines all app schemas)
│ ├── urls.py # URL routing (GraphQL view, health endpoint)
│ └── settings/ # Settings hierarchy
│ ├── base.py # Base settings
│ ├── local.py # Development settings (InMemory cache/channels)
│ └── production.py # Production settings (Redis cache/channels)
│
├── users/ # User Management
│ ├── models.py # Custom User model
│ ├── schema.py # User GraphQL schema
│ ├── mutations.py # User mutations (create, update)
│ └── types.py # User GraphQL types
│
├── posts/ # Post Management
│ ├── models.py # Post & Comment models
│ ├── schema.py # Post GraphQL schema
│ ├── signals.py # Cache invalidation signals
│ └── types.py # Post GraphQL types
│
├── interactions/ # User Interactions & Real-time
│ ├── consumers.py # WebSocket consumers
│ ├── middleware.py # JWT auth for WebSocket
│ ├── models.py # Interaction model (likes/comments)
│ ├── routing.py # WebSocket URL routing
│ └── signals.py # Notification signals
│
└── utils/ # Shared Utilities
├── errors.py # Error handling & formatting
└── cache.py # Cache management
```

---

## Development

### Testing

```bash
# Run tests with coverage
pytest --cov

# Run specific test file
pytest tests/test_utils_errors.py
```

### Pre-commit Hooks

```bash
# Install pre-commit hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

---

## Environment Variables

Key variables in `.env`:

```ini
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

POSTGRES_DB=social_feed
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

REDIS_URL=redis://redis:6379/0
```

---

## Production Deployment

1. **Update production settings:**
   - Set `DEBUG=False`
   - Configure `ALLOWED_HOSTS`
   - Use strong `SECRET_KEY`
   - Set up proper database credentials

2. **Configure nginx:**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }
}
```

3. **Deploy with Docker:**
```bash
docker-compose -f docker-compose.prod.yml up -d
```

---

## API Documentation

Full API documentation is available at `/graphql/` when `DEBUG=True`.

---

## Troubleshooting

### Common Issues

1. **WebSocket Connection Failed**
   - Check JWT token validity
   - Verify Redis connection
   - Ensure proper CORS settings

2. **Cache Issues**
   - Verify Redis connection
   - Check cache key patterns
   - Clear cache: `python manage.py shell -c "from django.core.cache import cache; cache.clear()"`

3. **Database Migrations**
   - Run `python manage.py makemigrations`
   - Apply: `python manage.py migrate`

---

## Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Run tests
5. Push to branch
6. Create Pull Request

---

## License

This project is licensed under the MIT License - see the LICENSE file for details.

Copyright (c) 2025 [Adam Ismail]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---