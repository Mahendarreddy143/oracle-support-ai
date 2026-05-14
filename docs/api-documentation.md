# 📚 API Documentation

## Base URL
```
https://api.oracle-support-ai.com/v1
```

## Authentication
All API requests require JWT token in Authorization header:
```
Authorization: Bearer <token>
```

---

## Endpoints

### Issues

#### Create Issue
```
POST /issues
Content-Type: application/json

{
  "title": "PL/SQL procedure error",
  "description": "Getting ORA-06502 error",
  "category": "plsql",
  "error_message": "ORA-06502: PL/SQL: numeric or value error",
  "code_snippet": "...",
  "environment": {
    "oracle_version": "19c",
    "os": "Linux"
  }
}

Response: 201 Created
{
  "id": "uuid",
  "status": "open",
  "created_at": "2026-05-14T10:30:00Z"
}
```

#### Get Issue
```
GET /issues/{issue_id}

Response: 200 OK
{
  "id": "uuid",
  "title": "...",
  "status": "resolved",
  "solutions": [...],
  "created_at": "2026-05-14T10:30:00Z",
  "updated_at": "2026-05-14T11:00:00Z"
}
```

#### Search Issues
```
GET /issues/search?q=pl%2Fsql+error&category=plsql&limit=10&offset=0

Response: 200 OK
{
  "results": [
    {
      "id": "uuid",
      "title": "...",
      "relevance_score": 0.95,
      "category": "plsql"
    }
  ],
  "total": 150,
  "limit": 10,
  "offset": 0
}
```

#### List Issues
```
GET /issues?category=sql&status=resolved&limit=20&offset=0

Response: 200 OK
{
  "data": [...],
  "pagination": {
    "total": 500,
    "limit": 20,
    "offset": 0
  }
}
```

### Chat

#### Start Chat Session
```
POST /chat/sessions

{
  "issue_id": "uuid"
}

Response: 201 Created
{
  "session_id": "uuid",
  "created_at": "2026-05-14T10:30:00Z"
}
```

#### Send Message
```
POST /chat/sessions/{session_id}/messages

{
  "content": "Can you help me debug this procedure?",
  "code_context": "..."
}

Response: 201 Created
{
  "message_id": "uuid",
  "content": "...",
  "timestamp": "2026-05-14T10:30:00Z"
}
```

#### Get Chat History
```
GET /chat/sessions/{session_id}/messages?limit=50

Response: 200 OK
{
  "messages": [...],
  "session_id": "uuid"
}
```

### Users

#### Register
```
POST /auth/register

{
  "email": "user@example.com",
  "password": "secure_password",
  "full_name": "John Doe"
}

Response: 201 Created
{
  "user_id": "uuid",
  "email": "user@example.com",
  "token": "jwt_token"
}
```

#### Login
```
POST /auth/login

{
  "email": "user@example.com",
  "password": "password"
}

Response: 200 OK
{
  "access_token": "jwt_token",
  "refresh_token": "refresh_token",
  "expires_in": 3600
}
```

#### Get Profile
```
GET /users/me

Response: 200 OK
{
  "id": "uuid",
  "email": "user@example.com",
  "full_name": "John Doe",
  "created_at": "2026-01-01T00:00:00Z"
}
```

### Analytics

#### Get Stats
```
GET /analytics/stats

Response: 200 OK
{
  "total_issues": 1500,
  "resolved_issues": 1200,
  "active_users": 250,
  "avg_resolution_time": "2.5 hours"
}
```

#### Get Category Stats
```
GET /analytics/categories

Response: 200 OK
{
  "plsql": { "count": 450, "resolved": 400 },
  "sql": { "count": 350, "resolved": 320 },
  "forms": { "count": 300, "resolved": 250 }
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "error": "validation_error",
  "message": "Invalid issue category",
  "details": {
    "category": "Category must be one of: plsql, sql, forms, ..."
  }
}
```

### 401 Unauthorized
```json
{
  "error": "unauthorized",
  "message": "Invalid or expired token"
}
```

### 404 Not Found
```json
{
  "error": "not_found",
  "message": "Issue not found"
}
```

### 429 Too Many Requests
```json
{
  "error": "rate_limit_exceeded",
  "message": "You have exceeded the rate limit",
  "retry_after": 60
}
```

### 500 Internal Server Error
```json
{
  "error": "internal_error",
  "message": "An internal error occurred",
  "request_id": "uuid"
}
```

---

## Rate Limiting

- **Free Tier**: 100 requests/hour
- **Pro Tier**: 1000 requests/hour
- **Enterprise**: Unlimited

Headers included in response:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1652510400
```

---

## Pagination

All list endpoints support pagination:

```
GET /issues?limit=20&offset=0

Query Parameters:
- limit: Number of results (default: 20, max: 100)
- offset: Number of results to skip (default: 0)
```

---

## WebSocket (Real-time Chat)

```javascript
const ws = new WebSocket('wss://api.oracle-support-ai.com/ws/chat');

ws.onopen = () => {
  ws.send(JSON.stringify({
    type: 'subscribe',
    session_id: 'uuid'
  }));
};

ws.onmessage = (event) => {
  const message = JSON.parse(event.data);
  console.log('New message:', message);
};
```
