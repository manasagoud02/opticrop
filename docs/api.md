# API Documentation

## Authentication
Use a bearer token returned from the register or login endpoint.

## Endpoints
### POST /auth/register
Creates a new account.

Request body:
```json
{
  "name": "Aisha",
  "email": "aisha@example.com",
  "password": "secret123"
}
```

### POST /auth/login
Authenticates an existing user.

### POST /recommend
Returns ranked crop recommendations.

Request body:
```json
{
  "nitrogen": 90,
  "phosphorous": 45,
  "potassium": 40,
  "temperature": 24,
  "humidity": 76,
  "ph": 6.2,
  "rainfall": 160
}
```

### POST /evaluate
Evaluates a specific crop.

### GET /dashboard
Shows recent recommendations for the signed-in user.
