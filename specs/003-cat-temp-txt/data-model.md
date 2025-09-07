# Data Model

## Entities

### Project
- id: UUID (primary key)
- name: string (required)
- created_at: datetime (auto)

### Character
- id: UUID (primary key)
- project_id: UUID (foreign key to Project)
- details: text (user input)
- personality: text (user input)
- image_url: string (generated)

### Product
- id: UUID (primary key)
- project_id: UUID (foreign key to Project)
- image_file: blob (uploaded file)

### Background
- id: UUID (primary key)
- project_id: UUID (foreign key to Project)
- scene_details: text (user input)
- lighting: text (user input)
- image_url: string (generated)

### Story
- id: UUID (primary key)
- project_id: UUID (foreign key to Project)
- story_text: text (user input)

### Image
- id: UUID (primary key)
- project_id: UUID (foreign key to Project)
- prompt: text (generated)
- image_url: string (generated)

## Relationships
- Project has many Characters (1:N)
- Project has many Products (1:N)
- Project has many Backgrounds (1:N)
- Project has many Stories (1:N)
- Project has many Images (1:N)

## Validation Rules
- Project name: required, max 100 chars
- Character details: required
- Product image: required, image file
- Background scene_details: required
- Story text: required
- All foreign keys: must exist
