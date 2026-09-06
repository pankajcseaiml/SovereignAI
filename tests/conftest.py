import os
import sys
from pathlib import Path

# Ensure backend and scripts are in python path
root_dir = Path(__file__).resolve().parent.parent
backend_dir = root_dir / "backend"
scripts_dir = root_dir / "scripts"

for p in [str(root_dir), str(backend_dir), str(scripts_dir)]:
    if p not in sys.path:
        sys.path.insert(0, p)

# Set test environment overrides
os.environ["APP_ENV"] = "test"
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"
os.environ["REDIS_URL"] = "redis://localhost:6379/0"
os.environ["QDRANT_HOST"] = "localhost"
os.environ["JWT_SECRET"] = "test_secret_for_unit_tests"
