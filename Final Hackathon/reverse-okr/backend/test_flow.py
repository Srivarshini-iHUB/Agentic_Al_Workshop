import requests
import json
import re

BASE_URL = "http://localhost:8000/api"

# Step 1: Aggregation
print("\n🔹 Step 1: Aggregating Exploration Logs...")
aggregate_payload = {
    "logs": [
        "https://www.youtube.com/watch?v=dD2EISBDjWM",
        "https://github.com/streamlit/streamlit",
        "https://www.figma.com/file/abcd1234/UI-Mockups"
    ]
}
res = requests.post(f"{BASE_URL}/aggregate", json=aggregate_payload)
print("🧪 Status Code:", res.status_code)
print("🧪 Raw Text Response:", res.text)

try:
    aggregate_output = res.json()
    print("✅ Aggregated Output:\n", aggregate_output)
except Exception as e:
    print("❌ JSON Decode Failed in Step 1:", e)
    exit(1)

# Step 1.5: Extract clean activity list
print("\n🔹 Step 1.5: Cleaning Activity Output...")
try:
    raw_output = aggregate_output["activities"]["output"]
    match = re.search(r"```json\s*(.*?)\s*```", raw_output, re.DOTALL)
    if not match:
        raise ValueError("No JSON code block found in output.")
    cleaned_output = match.group(1)
    activity_list = json.loads(cleaned_output)
    print("✅ Parsed Activity List:\n", activity_list)
except Exception as e:
    print("❌ Failed to parse activities output:", e)
    exit(1)

# Step 2: Intent & Theme Inference
print("\n🔹 Step 2: Inferring Intent and Themes...")
res = requests.post(f"{BASE_URL}/infer-intent", json={"activities": activity_list})
print("🧪 Status Code:", res.status_code)
print("🧪 Raw Text Response:", res.text)

try:
    intent_output = res.json()
    print("✅ Inferred Themes:\n", intent_output)
except Exception as e:
    print("❌ JSON Decode Failed in Step 2:", e)
    exit(1)

# Step 3: Knowledge Graph Mapping
print("\n🔹 Step 3: Mapping Knowledge Graph...")
try:
    themes_summary = intent_output["themes"]["output"]
    print("📤 Sending to map-graph:", {"themes": themes_summary})
    res = requests.post(f"{BASE_URL}/map-graph", json={"themes": themes_summary})
    print("🧪 Status Code:", res.status_code)
    print("🧪 Raw Text Response:", res.text)

    graph_output = res.json()
    print("✅ Knowledge Graph:\n", graph_output)
except Exception as e:
    print("❌ JSON Decode Failed in Step 3:", e)
    exit(1)


# Step 4: Outcome Generator
print("\n🔹 Step 4: Generating Potential Outcomes...")
res = requests.post(f"{BASE_URL}/generate-outcomes", json={
    "knowledge_graph": graph_output,
    "themes": intent_output
})
print("🧪 Status Code:", res.status_code)
print("🧪 Raw Text Response:", res.text)

try:
    outcome_output = res.json()
    print("✅ Outcome Suggestions:\n", outcome_output)
except Exception as e:
    print("❌ JSON Decode Failed in Step 4:", e)
    exit(1)

# Step 5: Retro-OKR Generator
print("\n🔹 Step 5: Generating Retrospective OKRs...")
res = requests.post(f"{BASE_URL}/generate-okr", json={
    "outcomes": outcome_output,
    "graph": graph_output
})
print("🧪 Status Code:", res.status_code)
print("🧪 Raw Text Response:", res.text)

try:
    okr_output = res.json()
    print("✅ Final OKRs:\n", okr_output)
except Exception as e:
    print("❌ JSON Decode Failed in Step 5:", e)
    exit(1)
