"""World2Notion: Intelligent content ingestion and organization for Notion."""

__version__ = "0.1.0"
__author__ = "World2Notion Team"
__email__ = "team@world2notion.com"

# Only expose the main interface - following atomicity principle
from .core.config import Config
from .core.orchestrator import World2Notion

__all__ = ["World2Notion", "Config"] 