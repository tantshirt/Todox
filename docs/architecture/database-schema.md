# Database Schema

## MongoDB Collections

### users Collection

```json
{
  "_id": ObjectId("..."),
  "email": "user@example.com",
  "hashed_password": "$2b$12$...",
  "created_at": ISODate("2025-01-12T10:00:00Z"),
  "updated_at": ISODate("2025-01-12T10:00:00Z")
}
```

**Indexes:**
- `email`: Unique index for fast lookup and uniqueness constraint
- `_id`: Default primary key index

**Schema Validation:**
```json
{
  "$jsonSchema": {
    "bsonType": "object",
    "required": ["email", "hashed_password", "created_at", "updated_at"],
    "properties": {
      "email": {
        "bsonType": "string",
        "pattern": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
      },
      "hashed_password": {
        "bsonType": "string",
        "minLength": 60,
        "maxLength": 60
      },
      "created_at": { "bsonType": "date" },
      "updated_at": { "bsonType": "date" }
    }
  }
}
```

### tasks Collection

```json
{
  "_id": ObjectId("..."),
  "title": "Complete project documentation",
  "description": "Write comprehensive docs for the architecture",
  "priority": "High",
  "deadline": ISODate("2025-01-15"),
  "status": "open",
  "label_ids": [ObjectId("..."), ObjectId("...")],
  "owner_id": ObjectId("..."),
  "created_at": ISODate("2025-01-12T10:30:00Z"),
  "updated_at": ISODate("2025-01-12T10:30:00Z")
}
```

**Indexes:**
- `owner_id`: Index for efficient querying of user's tasks
- `owner_id + created_at`: Compound index for sorted queries
- `_id`: Default primary key index

**Schema Validation:**
```json
{
  "$jsonSchema": {
    "bsonType": "object",
    "required": ["title", "priority", "deadline", "status", "label_ids", "owner_id", "created_at", "updated_at"],
    "properties": {
      "title": {
        "bsonType": "string",
        "minLength": 1,
        "maxLength": 200
      },
      "description": {
        "bsonType": ["string", "null"]
      },
      "priority": {
        "enum": ["High", "Medium", "Low"]
      },
      "deadline": {
        "bsonType": "date"
      },
      "status": {
        "enum": ["open", "done"]
      },
      "label_ids": {
        "bsonType": "array",
        "items": { "bsonType": "objectId" }
      },
      "owner_id": {
        "bsonType": "objectId"
      },
      "created_at": { "bsonType": "date" },
      "updated_at": { "bsonType": "date" }
    }
  }
}
```

### labels Collection

```json
{
  "_id": ObjectId("..."),
  "name": "Work",
  "owner_id": ObjectId("..."),
  "created_at": ISODate("2025-01-12T10:15:00Z")
}
```

**Indexes:**
- `owner_id + name`: Compound unique index for per-user label name uniqueness
- `owner_id`: Index for efficient querying of user's labels
- `_id`: Default primary key index

**Schema Validation:**
```json
{
  "$jsonSchema": {
    "bsonType": "object",
    "required": ["name", "owner_id", "created_at"],
    "properties": {
      "name": {
        "bsonType": "string",
        "minLength": 1,
        "maxLength": 50
      },
      "owner_id": {
        "bsonType": "objectId"
      },
      "created_at": { "bsonType": "date" }
    }
  }
}
```


---
