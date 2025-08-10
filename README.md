# World2Notion

Intelligent content ingestion and organization for Notion. Transform your notes, images, and thoughts into perfectly organized Notion pages with AI-powered classification and routing.

## 🚀 Features

- **Multi-Format Ingestion**: Process text files, images (with OCR), and soon audio files
- **AI-Powered Classification**: Automatically categorize content as notes, tasks, meetings, or research
- **Smart Routing**: Route content to the right place in your Notion hierarchy
- **Reliable Integration**: Idempotent operations with full audit trails
- **Local Processing**: Your data stays on your machine for privacy and speed

## 🎯 Use Cases

### For Students
- Automatically file lecture notes under the correct course with date headers
- Convert whiteboard photos to searchable text notes
- Extract action items from study sessions

### For Researchers
- Organize research papers and findings by topic
- Capture meeting notes with structured action items
- Build a searchable knowledge base from various sources

### For Professionals
- Streamline meeting documentation and follow-ups
- Capture and organize reference materials
- Maintain daily logs and project updates

## 📦 Installation

### Prerequisites
- Python 3.11 or higher
- Notion API token
- Tesseract OCR (for image processing)

### Install World2Notion

```bash
# Clone the repository
git clone https://github.com/world2notion/world2notion.git
cd world2notion

# Install in development mode
pip install -e ".[dev]"

# Or install from PyPI (when available)
pip install world2notion
```

### Install Tesseract OCR

**macOS:**
```bash
brew install tesseract
```

**Ubuntu/Debian:**
```bash
sudo apt-get install tesseract-ocr
```

**Windows:**
Download from [GitHub releases](https://github.com/UB-Mannheim/tesseract/wiki)

## 🛠️ Quick Start

### 1. Initialize Your Workspace

```bash
# Initialize World2Notion with your Notion credentials
world2notion init --notion-token <your-token> --workspace-id <your-workspace-id>
```

This will:
- Scan your Notion workspace structure
- Create a configuration file (`config/config.yaml`)
- Set up local databases for caching
- Create core databases (Daily Log, Tasks, Knowledge Snippets, Changelog)

### 2. Configure Your Setup

Edit `config/config.yaml` to customize your setup:

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

aliases:
  courses:
    "CSE-2293": "CSE-2293 Deep Learning"
    "CS2293": "CSE-2293 Deep Learning"
```

### 3. Start Ingesting Content

```bash
# Ingest a text file
world2notion ingest file path/to/lecture-notes.md

# Ingest text directly
world2notion ingest text "Meeting notes: Discussed project timeline and next steps"

# Ingest an image (with OCR)
world2notion ingest image path/to/whiteboard.jpg

# Review pending items
world2notion review

# Approve or reject items
world2notion approve <item-id>
world2notion reject <item-id> --reason "Wrong classification"
```

## 📁 Project Structure

```
world2notion/
├── src/world2notion/
│   ├── core/           # Core orchestration and configuration
│   ├── agents/         # AI agents for classification and extraction
│   ├── tools/          # Deterministic tools for external interactions
│   ├── storage/        # Local database and file storage
│   ├── models/         # Data models and schemas
│   └── cli/            # Command-line interface
├── config/             # Configuration files
├── data/               # Local data storage
│   ├── inbox/          # Input files
│   ├── cache/          # Processed artifacts
│   └── logs/           # Audit logs
└── tests/              # Test suite
```

## 🔧 Configuration

### Configuration Files

- **`config.yaml`**: User-editable configuration with routing rules, aliases, and settings
- **`config.lock.json`**: Compiled configuration with resolved Notion IDs and schemas

### Key Configuration Options

- **Routing Rules**: Define patterns and target locations for different content types
- **Entity Aliases**: Map shorthand names to full entity names (courses, people, etc.)
- **Safety Thresholds**: Set confidence levels for automatic vs. manual processing
- **Container Types**: Define how different content types are stored (pages, databases, etc.)

## 🧪 Development

### Setting Up Development Environment

```bash
# Clone and install in development mode
git clone https://github.com/world2notion/world2notion.git
cd world2notion
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Run tests
pytest

# Run linting
ruff check src/
black src/
mypy src/
```

### Running Tests

```bash
# Run all tests
pytest

# Run unit tests only
pytest tests/unit/

# Run integration tests
pytest tests/integration/

# Run with coverage
pytest --cov=world2notion
```

### Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and linting
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📚 Documentation

- [API Reference](docs/api.md)
- [Configuration Guide](docs/configuration.md)
- [Examples and Use Cases](docs/examples.md)
- [Troubleshooting](docs/troubleshooting.md)

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/world2notion/world2notion/issues)
- **Discussions**: [GitHub Discussions](https://github.com/world2notion/world2notion/discussions)
- **Documentation**: [Read the Docs](https://world2notion.readthedocs.io)

## 🗺️ Roadmap

### Phase 1: MVP (Current)
- [x] Project setup and architecture
- [ ] Basic text and image ingestion
- [ ] AI-powered classification
- [ ] Notion integration
- [ ] CLI interface

### Phase 2: Enhanced Features
- [ ] Audio processing and speech-to-text
- [ ] Advanced entity linking
- [ ] Web interface for review
- [ ] Template system

### Phase 3: Intelligence
- [ ] Learning from user corrections
- [ ] Automatic summarization
- [ ] Cross-reference detection
- [ ] Smart suggestions

---

**World2Notion** - Turn capture into a lightweight habit that doesn't break your workflow. 