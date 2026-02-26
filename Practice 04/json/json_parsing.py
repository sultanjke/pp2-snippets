# =============================================================
# JSON Parsing: json.loads() and json.dumps()
# =============================================================

import json


# JSON is a text format for storing structured data.
# Python's json module converts between JSON strings and
# Python objects (dicts, lists, str, int, float, bool, None).

# --- json.loads(): JSON string -> Python object ---

json_string = '{"name": "Sultan", "age": 20, "gpa": 3.8, "is_active": true}'
data = json.loads(json_string)

print("--- json.loads() ---")
print(f"  Type: {type(data)}")
print(f"  Data: {data}")
print(f"  Name: {data['name']}")
print(f"  GPA:  {data['gpa']}")


# JSON arrays become Python lists
json_array = '[1, 2, 3, "hello", true, null]'
parsed_list = json.loads(json_array)
print(f"\n  JSON array -> {parsed_list}")
print(f"  Type: {type(parsed_list)}")


# Nested JSON
nested_json = '''
{
    "student": {
        "name": "Aisha",
        "grades": [90, 85, 92],
        "address": {"city": "Astana", "country": "Kazakhstan"}
    }
}
'''
nested_data = json.loads(nested_json)
city = nested_data["student"]["address"]["city"]
print(f"\n  Nested access -> city: {city}")


# --- json.dumps(): Python object -> JSON string ---

python_dict = {
    "name": "Damir",
    "age": 21,
    "courses": ["Databases", "Networks"],
    "graduated": False,
    "scholarship": None
}

# Basic conversion
json_output = json.dumps(python_dict)
print(f"\n--- json.dumps() ---")
print(f"  Type: {type(json_output)}")
print(f"  Raw:  {json_output}")

# Pretty-printed with indent
pretty_json = json.dumps(python_dict, indent=2)
print(f"\n  Pretty:\n{pretty_json}")

# sort_keys orders dictionary keys alphabetically
sorted_json = json.dumps(python_dict, indent=2, sort_keys=True)
print(f"\n  Sorted keys:\n{sorted_json}")


# --- Type mapping between Python and JSON ---
print("\n--- Python <-> JSON type mapping ---")

type_demo = {
    "string": "hello",       # str    <-> string
    "integer": 42,            # int    <-> number
    "float": 3.14,            # float  <-> number
    "boolean_true": True,     # True   <-> true
    "boolean_false": False,   # False  <-> false
    "null_value": None,       # None   <-> null
    "list": [1, 2, 3],        # list   <-> array
    "dict": {"key": "value"}  # dict   <-> object
}

print(json.dumps(type_demo, indent=2))


# ensure_ascii=False preserves non-ASCII characters (Cyrillic, etc.)
kazakh_data = {"city": "Алматы", "greeting": "Сәлем"}
print(f"\n  ASCII:     {json.dumps(kazakh_data)}")
print(f"  Non-ASCII: {json.dumps(kazakh_data, ensure_ascii=False)}")


# separators parameter controls compactness
compact = json.dumps(python_dict, separators=(",", ":"))
print(f"\n  Compact: {compact}")
