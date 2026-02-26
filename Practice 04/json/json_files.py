# =============================================================
# Reading and Writing JSON Files
# =============================================================

import json
import os

# All file operations use the script's own directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


# --- json.dump(): write a Python object to a JSON file ---

student_records = [
    {"name": "Alice", "grade": 92, "passed": True},
    {"name": "Bob", "grade": 67, "passed": False},
    {"name": "Charlie", "grade": 85, "passed": True},
]

output_path = os.path.join(SCRIPT_DIR, "output.json")

with open(output_path, "w") as file:
    json.dump(student_records, file, indent=2)

print(f"--- Written to {os.path.basename(output_path)} ---")
print(f"  Records saved: {len(student_records)}")


# --- json.load(): read a JSON file into a Python object ---

with open(output_path, "r") as file:
    loaded_records = json.load(file)

print(f"\n--- Read from {os.path.basename(output_path)} ---")
for record in loaded_records:
    status = "PASS" if record["passed"] else "FAIL"
    print(f"  {record['name']}: {record['grade']} ({status})")


# --- Writing nested data ---

config = {
    "app_name": "StudentPortal",
    "version": "2.1.0",
    "debug": False,
    "database": {
        "host": "localhost",
        "port": 5432,
        "name": "students_db"
    },
    "features": ["auth", "grades", "schedule"],
    "max_users": None
}

config_path = os.path.join(SCRIPT_DIR, "config.json")

with open(config_path, "w") as file:
    json.dump(config, file, indent=4)

print(f"\n--- Config written to {os.path.basename(config_path)} ---")


# --- Reading and modifying, then saving back ---

with open(config_path, "r") as file:
    loaded_config = json.load(file)

# Update some values
loaded_config["debug"] = True
loaded_config["version"] = "2.2.0"
loaded_config["features"].append("notifications")

with open(config_path, "w") as file:
    json.dump(loaded_config, file, indent=4)

print(f"  Updated version to {loaded_config['version']}")
print(f"  Debug mode: {loaded_config['debug']}")
print(f"  Features: {loaded_config['features']}")


# --- Handling errors when reading JSON ---

print(f"\n--- Error handling ---")

# File not found
try:
    with open("nonexistent.json", "r") as file:
        json.load(file)
except FileNotFoundError:
    print("  FileNotFoundError: file does not exist")

# Invalid JSON content
try:
    bad_json = '{"name": "Alice", age: 20}'  # missing quotes around key
    json.loads(bad_json)
except json.JSONDecodeError as error:
    print(f"  JSONDecodeError: {error.msg} (position {error.pos})")


# Clean up generated files
os.remove(output_path)
os.remove(config_path)
print(f"\n  Cleaned up generated files.")
