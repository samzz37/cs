"""
Pytest configuration and project path setup
"""
import sys
from pathlib import Path

# Add project root and backend to Python path for imports
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / 'backend'))
sys.path.insert(0, str(project_root / 'certificate-engine'))
sys.path.insert(0, str(project_root / 'exports'))
sys.path.insert(0, str(project_root / 'monitoring'))
sys.path.insert(0, str(project_root / 'ranking-module'))
