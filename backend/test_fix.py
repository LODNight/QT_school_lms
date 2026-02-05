import sys
import os
sys.path.append(os.getcwd())
try:
    import schemas
    print("Import schemas successful")
except Exception as e:
    print(f"Import schemas failed: {e}")
    sys.exit(1)
