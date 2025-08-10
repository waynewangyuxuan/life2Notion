# World2Notion: Technical Design

## Architecture Overview

World2Notion is an orchestrated set of AI agents and deterministic tools that process various input formats and intelligently organize them into Notion. The system follows a pipeline architecture with clear separation between AI-powered agents and deterministic tools.

## High-Level Architecture

```
Input → Ingestion → Classification → Extraction → Auditing → Writing → Logging
```

### Core Components

#### 1. Orchestrator/Workflow Engine
- **Purpose**: Coordinates agents and tools in a well-defined order
- **Responsibilities**: 
  - Handle retries, backoff, and error handling
  - Manage pipeline execution flow
  - Ensure idempotent operations
  - Coordinate audit and approval workflows

#### 2. AI Agents (LLM-powered brains)
Pure functions that interpret content and make decisions without direct Notion access:

- **Notion Map Agent**: Builds and maintains internal map of Notion hierarchy
- **Classifier/Router Agent**: Determines item type and selects routing rules
- **Extractor Agent**: Produces strict JSON matching target Notion schemas
- **Auditor/Verifier Agent**: Validates extracted data and confidence levels

#### 3. Deterministic Tools
Handle side effects and external interactions:

- **Notion Reader Tool**: API interactions for reading Notion structure
- **Notion Writer Tool**: API interactions for writing to Notion
- **OCR/Captioner**: Image text extraction and captioning
- **Path Resolver**: Converts symbolic paths to concrete Notion IDs
- **Hasher/Deduper**: Content deduplication and similarity detection

#### 4. Local Storage
- **SQLite Database**: Notion structure cache, ingest history, entity aliases
- **Vector Index**: Semantic search for similar content and entities
- **File Storage**: Original source files and processed artifacts

## Technical Stack

### Core Technologies
- **Language**: Python 3.11+
- **Framework**: FastAPI for CLI and potential web interface
- **Database**: SQLite for local storage
- **Vector Store**: ChromaDB or FAISS for semantic search
- **AI/ML**: OpenAI GPT-4 for agents, local models for OCR

### External Integrations
- **Notion API**: Official Notion SDK for Python
- **OCR**: Tesseract or cloud OCR service
- **File Processing**: Pillow for images, PyPDF2 for PDFs

### Development Tools
- **Testing**: pytest for unit and integration tests
- **Linting**: ruff for code quality
- **Type Checking**: mypy for static analysis
- **Documentation**: Sphinx for API docs

## File Structure

```
world2notion/
├── src/
│   ├── world2notion/
│   │   ├── __init__.py
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── orchestrator.py      # Main workflow engine
│   │   │   ├── config.py            # Configuration management
│   │   │   └── exceptions.py        # Custom exceptions
│   │   ├── agents/
│   │   │   ├── __init__.py
│   │   │   ├── base.py              # Base agent class
│   │   │   ├── notion_map.py        # Notion structure mapping
│   │   │   ├── classifier.py        # Content classification
│   │   │   ├── extractor.py         # Data extraction
│   │   │   └── auditor.py           # Validation and verification
│   │   ├── tools/
│   │   │   ├── __init__.py
│   │   │   ├── notion_reader.py     # Notion API reading
│   │   │   ├── notion_writer.py     # Notion API writing
│   │   │   ├── path_resolver.py     # Path resolution
│   │   │   ├── ocr.py               # Image text extraction
│   │   │   ├── hasher.py            # Content hashing
│   │   │   └── diff.py              # Change tracking
│   │   ├── storage/
│   │   │   ├── __init__.py
│   │   │   ├── database.py          # SQLite operations
│   │   │   ├── vector_store.py      # Semantic search
│   │   │   └── file_store.py        # File management
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── content.py           # Content models
│   │   │   ├── notion.py            # Notion data models
│   │   │   └── config.py            # Configuration models
│   │   └── cli/
│   │       ├── __init__.py
│   │       ├── main.py              # CLI entry point
│   │       └── commands.py          # CLI commands
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── unit/
│   │   ├── integration/
│   │   └── fixtures/
│   └── docs/
│       ├── api.md
│       ├── configuration.md
│       └── examples.md
├── config/
│   ├── config.yaml                  # User configuration
│   └── config.lock.json             # Compiled configuration
├── data/
│   ├── inbox/                       # Input files
│   ├── cache/                       # Processed artifacts
│   └── logs/                        # Audit logs
├── pyproject.toml                   # Project configuration
├── README.md
└── requirements.txt
```

## Data Models

### Content Models
```python
@dataclass
class ContentItem:
    id: str
    source_type: SourceType  # TEXT, IMAGE, AUDIO
    content: str
    metadata: Dict[str, Any]
    source_file: Optional[Path]
    created_at: datetime
    hash: str

@dataclass
class ClassificationResult:
    item_type: ItemType  # NOTE, TASK, MEETING, RESEARCH
    confidence: float
    routing_rule: str
    entities: List[Entity]

@dataclass
class ExtractionResult:
    schema: str
    fields: Dict[str, Any]
    source_spans: Dict[str, List[Span]]
    confidence: float
```

### Notion Models
```python
@dataclass
class NotionPage:
    id: str
    title: str
    parent_id: Optional[str]
    properties: Dict[str, Any]
    blocks: List[NotionBlock]

@dataclass
class NotionDatabase:
    id: str
    title: str
    properties: Dict[str, PropertySchema]
    rows: List[NotionRow]
```

## Configuration System

### User Configuration (config.yaml)
```yaml
notion:
  token: "your-notion-token"
  workspace_id: "your-workspace-id"

base_paths:
  school: "/School"
  coursework: "/School/Coursework"
  daily_log: "/Daily Log"

routing_rules:
  - pattern: "class notes"
    target: "/School/Coursework/{course}/Notes/#{date}"
    schema: "note"
  
  - pattern: "daily reflection"
    target: "/Daily Log"
    schema: "daily_entry"

containers:
  notes:
    type: "page_with_headings"
    date_format: "YYYY-MM-DD"
  
  tasks:
    type: "database"
    database_id: "tasks-db-id"

aliases:
  courses:
    "CSE-2293": "CSE-2293 Deep Learning"
    "CS2293": "CSE-2293 Deep Learning"

safety:
  confidence_threshold: 0.8
  require_approval: true
  max_retries: 3
```

### Compiled Configuration (config.lock.json)
```json
{
  "resolved_paths": {
    "/School/Coursework/CSE-2293 Deep Learning": "page-id-123",
    "/Daily Log": "database-id-456"
  },
  "schemas": {
    "note": {
      "title": "string",
      "content": "rich_text",
      "date": "date",
      "course": "select"
    }
  },
  "functions": {
    "date_formatter": "YYYY-MM-DD",
    "idempotency_key": "hash(content) + path"
  }
}
```

## API Design

### Core Operations
```python
class World2Notion:
    async def ingest_file(self, file_path: Path) -> IngestResult
    async def ingest_text(self, text: str, metadata: Dict) -> IngestResult
    async def ingest_image(self, image_path: Path) -> IngestResult
    
    async def approve_item(self, item_id: str) -> bool
    async def reject_item(self, item_id: str, reason: str) -> bool
    async def revert_item(self, item_id: str) -> bool
    
    async def sync_notion_map(self) -> None
    async def update_config(self, config_updates: Dict) -> None
```

### CLI Interface
```bash
# Initialize workspace
world2notion init --notion-token <token> --workspace-id <id>

# Ingest content
world2notion ingest file path/to/note.md
world2notion ingest text "Meeting notes from today"
world2notion ingest image path/to/whiteboard.jpg

# Review pending items
world2notion review
world2notion approve <item-id>
world2notion reject <item-id> --reason "Wrong classification"

# Manage configuration
world2notion config show
world2notion config update --add-alias "CS2293:CSE-2293 Deep Learning"

# Sync and maintenance
world2notion sync
world2notion revert <item-id>
```

## Security and Privacy

### Data Handling
- All processing happens locally by default
- Original files stored in encrypted local storage
- API keys stored securely using system keyring
- Audit logs contain no sensitive content

### Notion Integration
- Read-only access to workspace structure
- Write access limited to specified paths
- Idempotent operations prevent accidental duplicates
- All changes logged with full audit trail

## Performance Considerations

### Caching Strategy
- Notion structure cached locally with TTL
- Vector embeddings cached for similarity search
- Processed content cached to avoid re-processing

### Scalability
- Async processing for I/O operations
- Batch processing for multiple files
- Configurable rate limiting for API calls
- Efficient vector search with approximate nearest neighbors

## Testing Strategy

### Unit Tests
- Agent logic with mocked LLM responses
- Tool functionality with mocked external APIs
- Data model validation and serialization

### Integration Tests
- End-to-end pipeline with test Notion workspace
- Configuration management and hot-reloading
- Error handling and recovery scenarios

### Performance Tests
- Large file processing benchmarks
- API rate limiting and backoff
- Memory usage and cleanup
