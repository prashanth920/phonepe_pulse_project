import os
import json
import pandas as pd

# ==================================================
# 📍 Set your root data path here
# ==================================================
ROOT_DIR = r"C:\Users\prash\Downloads\phonepe_project\pulse\data"

# Output directory
OUTPUT_DIR = r"C:\Users\prash\Downloads\phonepe_project\parsed_output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ==================================================
# 🗂️ Helper Functions
# ==================================================
def load_json(file_path):
    """Safely load JSON file"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error reading {file_path}: {e}")
        return {}

def get_year_quarter(file_path):
    """Extract year and quarter from path"""
    year = os.path.basename(os.path.dirname(file_path))
    quarter = os.path.basename(file_path).replace(".json", "")
    return year, quarter

# ==================================================
# 📦 Lists for collecting data
# ==================================================
agg_trans, agg_user, agg_insurance = [], [], []
map_trans, map_user, map_insurance = [], [], []
top_trans, top_user, top_insurance = [], [], []

# ==================================================
# 🔁 Walk through all JSON files
# ==================================================
for root, _, files in os.walk(ROOT_DIR):
    for file in files:
        if not file.endswith(".json"):
            continue

        file_path = os.path.join(root, file)
        year, quarter = get_year_quarter(file_path)

        data = load_json(file_path)
        if not data or "data" not in data or data["data"] is None:
            continue  # skip empty files

        section = (
            "aggregated" if "aggregated" in root else
            "map" if "map" in root else
            "top" if "top" in root else ""
        )

        sub_data = data.get("data") or {}

        # ==================================================
        # 🧮 1️⃣ Aggregated Data
        # ==================================================
        if section == "aggregated":
            # ---- Transactions ----
            if "transaction" in root:
                for entry in sub_data.get("transactionData", []) or []:
                    instruments = entry.get("paymentInstruments") or []
                    if not instruments:
                        continue
                    agg_trans.append({
                        "year": int(year),
                        "quarter": int(quarter),
                        "category": entry.get("name"),
                        "type": instruments[0].get("type"),
                        "count": instruments[0].get("count"),
                        "amount": instruments[0].get("amount")
                    })

            # ---- User ----
            elif "user" in root:
                total = sub_data.get("aggregated") or {}
                devices = sub_data.get("usersByDevice") or []
                if devices:
                    for u in devices:
                        agg_user.append({
                            "year": int(year),
                            "quarter": int(quarter),
                            "brand": u.get("brand"),
                            "count": u.get("count"),
                            "percentage": u.get("percentage"),
                            "registered_users": total.get("registeredUsers"),
                            "app_opens": total.get("appOpens")
                        })
                else:
                    agg_user.append({
                        "year": int(year),
                        "quarter": int(quarter),
                        "brand": None,
                        "count": None,
                        "percentage": None,
                        "registered_users": total.get("registeredUsers"),
                        "app_opens": total.get("appOpens")
                    })

            # ---- Insurance ----
            elif "insurance" in root:
                for entry in sub_data.get("transactionData", []) or []:
                    instruments = entry.get("paymentInstruments") or []
                    if not instruments:
                        continue
                    agg_insurance.append({
                        "year": int(year),
                        "quarter": int(quarter),
                        "name": entry.get("name"),
                        "count": instruments[0].get("count"),
                        "amount": instruments[0].get("amount")
                    })

        # ==================================================
        # 🗺️ 2️⃣ Map Data
        # ==================================================
        elif section == "map":
            # ---- Map Transaction ----
            if "transaction" in root:
                for entry in sub_data.get("hoverDataList", []) or []:
                    metric = entry.get("metric") or [{}]
                    map_trans.append({
                        "year": int(year),
                        "quarter": int(quarter),
                        "state": entry.get("name"),
                        "count": metric[0].get("count"),
                        "amount": metric[0].get("amount")
                    })

            # ---- Map User ----
            elif "user" in root:
                hover = sub_data.get("hoverData") or {}
                for state, val in hover.items():
                    map_user.append({
                        "year": int(year),
                        "quarter": int(quarter),
                        "state": state,
                        "registered_users": val.get("registeredUsers"),
                        "app_opens": val.get("appOpens")
                    })

            # ---- Map Insurance ----
            elif "insurance" in root:
                for entry in sub_data.get("hoverDataList", []) or []:
                    metric = entry.get("metric") or [{}]
                    map_insurance.append({
                        "year": int(year),
                        "quarter": int(quarter),
                        "state": entry.get("name"),
                        "count": metric[0].get("count"),
                        "amount": metric[0].get("amount")
                    })

        # ==================================================
        # 🏆 3️⃣ Top Data
        # ==================================================
        elif section == "top":
            for level in ["states", "districts", "pincodes"]:
                entries = sub_data.get(level) or []
                if not entries:
                    continue

                # ---- Top Transaction ----
                if "transaction" in root:
                    for entry in entries:
                        metric = entry.get("metric") or {}
                        top_trans.append({
                            "year": int(year),
                            "quarter": int(quarter),
                            "level": level,
                            "entity": entry.get("entityName"),
                            "count": metric.get("count"),
                            "amount": metric.get("amount")
                        })

                # ---- Top User ----
                elif "user" in root:
                    for entry in entries:
                        top_user.append({
                            "year": int(year),
                            "quarter": int(quarter),
                            "level": level,
                            "entity": entry.get("name"),
                            "registered_users": entry.get("registeredUsers")
                        })

                # ---- Top Insurance ----
                elif "insurance" in root:
                    for entry in entries:
                        metric = entry.get("metric") or {}
                        top_insurance.append({
                            "year": int(year),
                            "quarter": int(quarter),
                            "level": level,
                            "entity": entry.get("entityName"),
                            "count": metric.get("count"),
                            "amount": metric.get("amount")
                        })

# ==================================================
# 📊 Convert Lists → DataFrames
# ==================================================
dfs = {
    "aggregated_transaction": pd.DataFrame(agg_trans),
    "aggregated_user": pd.DataFrame(agg_user),
    "aggregated_insurance": pd.DataFrame(agg_insurance),
    "map_transaction": pd.DataFrame(map_trans),
    "map_user": pd.DataFrame(map_user),
    "map_insurance": pd.DataFrame(map_insurance),
    "top_transaction": pd.DataFrame(top_trans),
    "top_user": pd.DataFrame(top_user),
    "top_insurance": pd.DataFrame(top_insurance)
}

# ==================================================
# 💾 Save all CSVs
# ==================================================
for name, df in dfs.items():
    file_path = os.path.join(OUTPUT_DIR, f"{name}.csv")
    df.to_csv(file_path, index=False)
    print(f"✅ Saved: {file_path} ({len(df)} rows)")

print("\n🎉 All PhonePe Pulse JSONs parsed successfully and safely!")
