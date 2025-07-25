#!/usr/bin/env python

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Ensure project root is in sys.path for config import
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
load_dotenv(dotenv_path=ROOT / ".env")
from config import config

def main():
    # Output all key config and environment info as a single CSV line, no extra formatting
    items = [
        f"ROOT={config.ROOT}",
        f"ADMIN_DIR={config.ADMIN_DIR}",
        f"SRC_DIR={config.SRC_DIR}",
        f"PRESENTATION_DIR={config.PRESENTATION_DIR}",
        f"BRAND_DIR={config.BRAND_DIR}",
        f"BUSINESS_DIR={config.BUSINESS_DIR}",
        f"DATA_DIR={config.DATA_DIR}",
        f"NOTEBOOKS_DIR={config.NOTEBOOKS_DIR}",
        f"LOGS_DIR={config.LOGS_DIR}",
        f"ALLURE_RESULTS_DIR={config.ALLURE_RESULTS_DIR}",
        f"ENVIRONMENTS={','.join(config.ENVIRONMENTS)}",
        f"PRESENTATION_APPS={','.join(config.PRESENTATION_APPS.keys())}",
        f"DEBUG_MODE={getattr(config, 'DEBUG_MODE', False)}",
        f"TESTING_MODE={getattr(config, 'TESTING_MODE', False)}",
        f"MAINTENANCE_MODE={getattr(config, 'MAINTENANCE_MODE', False)}",
        f"VERSION={getattr(config, 'VERSION', '')}"
    ]
    print(','.join(items))

if __name__ == "__main__":
    main()#!/usr/bin/env python
import os
import sys
from pathlib import Path
from config import config

def main():
    # Print key config and environment info in a single line, no extra spaces or formatting
    items = [
        f"ROOT={config.ROOT}",
        f"ADMIN_DIR={config.ADMIN_DIR}",
        f"SRC_DIR={config.SRC_DIR}",
        f"PRESENTATION_DIR={config.PRESENTATION_DIR}",
        f"BRAND_DIR={config.BRAND_DIR}",
        f"BUSINESS_DIR={config.BUSINESS_DIR}",
        f"DATA_DIR={config.DATA_DIR}",
        f"NOTEBOOKS_DIR={config.NOTEBOOKS_DIR}",
        f"LOGS_DIR={config.LOGS_DIR}",
        f"ALLURE_RESULTS_DIR={config.ALLURE_RESULTS_DIR}",
        f"ENVIRONMENTS={','.join(config.ENVIRONMENTS)}",
        f"PRESENTATION_APPS={','.join(config.PRESENTATION_APPS.keys())}",
        f"DEBUG_MODE={getattr(config, 'DEBUG_MODE', False)}",
        f"TESTING_MODE={getattr(config, 'TESTING_MODE', False)}",
        f"MAINTENANCE_MODE={getattr(config, 'MAINTENANCE_MODE', False)}",
        f"VERSION={getattr(config, 'VERSION', '')}"
    ]
    print(';'.join(items))

if __name__ == "__main__":
    main()
