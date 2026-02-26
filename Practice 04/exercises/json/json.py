import json
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(SCRIPT_DIR, "sample-data.json")

with open(DATA_PATH, "r") as file:
    data = json.load(file)

# Only show the first 3 interfaces (eth1/33, eth1/34, eth1/35)
interfaces = data["imdata"][:3]

# Print the formatted table
print("Interface Status")
print("=" * 80)
print(f"{'DN':<51}{'Description':<22}{'Speed':<8}{'MTU':<6}")
print(f"{'-' * 50} {'-' * 20}  {'-' * 6}  {'-' * 6}")

for interface in interfaces:
    attributes = interface["l1PhysIf"]["attributes"]
    dn = attributes["dn"]
    description = attributes["descr"]
    speed = attributes["speed"]
    mtu = attributes["mtu"]
    print(f"{dn:<51}{description:<22}{speed:<8}{mtu:<6}")


## Outputs whole existing data column (second option)

# import json
# import os

# SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# DATA_PATH = os.path.join(SCRIPT_DIR, "sample-data.json")

# with open(DATA_PATH, "r") as file:
#     data = json.load(file)

# interfaces = data["imdata"]

# print("Interface Status")
# print("=" * 80)
# print(f"{'DN':<51}{'Description':<22}{'Speed':<8}{'MTU':<6}")
# print(f"{'-' * 50} {'-' * 20}  {'-' * 6}  {'-' * 6}")

# for interface in interfaces:
#     attributes = interface["l1PhysIf"]["attributes"]
#     dn = attributes["dn"]
#     description = attributes["descr"]
#     speed = attributes["speed"]
#     mtu = attributes["mtu"]
#     print(f"{dn:<51}{description:<22}{speed:<8}{mtu:<6}")
