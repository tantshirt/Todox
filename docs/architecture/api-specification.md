# API Specification

## REST API Specification

```yaml
openapi: 3.0.0
info:
  title: Todox API
  version: 1.0.0
  description: RESTful API for Todox task management application
servers:
  - url: http://localhost:8000
    description: Local development
  - url: https://todox-backend.up.railway.app
    description: Production (Railway)

components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
  
  schemas:
    User:
      type: object
      properties:
        id:
          type: string
        email:
          type: string
          format: email
        created_at:
          type: string
          format: date-time
        updated_at:
          type: string
          format: date-time
    
    Task:
      type: object
      properties:
        id:
          type: string
        title:
          type: string
        description:
          type: string
          nullable: true
        priority:
          type: string
          enum: [High, Medium, Low]
        deadline:
          type: string
          format: date
        status:
          type: string
          enum: [open, done]
        label_ids:
          type: array
          items:
            type: string
        owner_id:
          type: string
        created_at:
          type: string
          format: date-time
        updated_at:
          type: string
          format: date-time
    
    Label:
      type: object
      properties:
        id:
          type: string
        name:
          type: string
        owner_id:
          type: string
        created_at:
          type: string
          format: date-time
    
    AuthResponse:
      type: object
      properties:
        access_token:
          type: string
        token_type:
          type: string
          default: bearer
        expires_in:
          type: integer
          description: Token expiry time in seconds
    
    Error:
      type: object
      properties:
        detail:
          type: string

paths:
  /health:
    get:
      summary: Health check endpoint
      responses:
        '200':
          description: Service is healthy
          content:
            application/json:
              schema:
                type: object
                properties:
                  status:
                    type: string
                  database:
                    type: string
  
  /auth/register:
    post:
      summary: Register a new user
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - email
                - password
              properties:
                email:
                  type: string
                  format: email
                password:
                  type: string
                  minLength: 8
      responses:
        '201':
          description: User created successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '400':
          description: Validation error
        '409':
          description: Email already exists
  
  /auth/login:
    post:
      summary: Login with email and password
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - email
                - password
              properties:
                email:
                  type: string
                  format: email
                password:
                  type: string
      responses:
        '200':
          description: Login successful
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AuthResponse'
        '401':
          description: Invalid credentials
  
  /auth/me:
    get:
      summary: Get current user info
      security:
        - BearerAuth: []
      responses:
        '200':
          description: Current user data
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '401':
          description: Unauthorized
  
  /tasks:
    get:
      summary: List all tasks for authenticated user
      security:
        - BearerAuth: []
      responses:
        '200':
          description: List of tasks
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Task'
        '401':
          description: Unauthorized
    
    post:
      summary: Create a new task
      security:
        - BearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - title
                - priority
                - deadline
              properties:
                title:
                  type: string
                description:
                  type: string
                priority:
                  type: string
                  enum: [High, Medium, Low]
                deadline:
                  type: string
                  format: date
                label_ids:
                  type: array
                  items:
                    type: string
      responses:
        '201':
          description: Task created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Task'
        '400':
          description: Validation error
        '401':
          description: Unauthorized
  
  /tasks/{id}:
    patch:
      summary: Update a task
      security:
        - BearerAuth: []
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                title:
                  type: string
                description:
                  type: string
                  nullable: true
                priority:
                  type: string
                  enum: [High, Medium, Low]
                deadline:
                  type: string
                  format: date
                status:
                  type: string
                  enum: [open, done]
                label_ids:
                  type: array
                  items:
                    type: string
      responses:
        '200':
          description: Task updated
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Task'
        '400':
          description: Validation error
        '401':
          description: Unauthorized
        '404':
          description: Task not found
    
    delete:
      summary: Delete a task
      security:
        - BearerAuth: []
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
      responses:
        '204':
          description: Task deleted
        '401':
          description: Unauthorized
        '404':
          description: Task not found
  
  /labels:
    get:
      summary: List all labels for authenticated user
      security:
        - BearerAuth: []
      responses:
        '200':
          description: List of labels
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Label'
        '401':
          description: Unauthorized
    
    post:
      summary: Create a new label
      security:
        - BearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - name
              properties:
                name:
                  type: string
                  maxLength: 50
      responses:
        '201':
          description: Label created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Label'
        '400':
          description: Validation error
        '401':
          description: Unauthorized
        '409':
          description: Label name already exists for this user
  
  /labels/{id}:
    patch:
      summary: Update a label
      security:
        - BearerAuth: []
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - name
              properties:
                name:
                  type: string
                  maxLength: 50
      responses:
        '200':
          description: Label updated
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Label'
        '400':
          description: Validation error
        '401':
          description: Unauthorized
        '404':
          description: Label not found
        '409':
          description: Label name already exists
    
    delete:
      summary: Delete a label
      security:
        - BearerAuth: []
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
      responses:
        '204':
          description: Label deleted (also removed from all tasks)
        '401':
          description: Unauthorized
        '404':
          description: Label not found
```


---
