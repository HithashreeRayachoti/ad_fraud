import json
import pandas as pd
import re # Import the regular expressions library

# === CONFIG ===
json_path = "mouse_movements.json"

# === 1. Load outer JSON
with open(json_path, 'r') as f:
    raw_data = json.load(f)

# === 2. Extract mouse movements from 'total_behaviour' string
# The data is in the 'total_behaviour' key, not 'mousemove_times'
behaviour_string = raw_data.get("total_behaviour", "")

# Use regular expression to find all coordinate pairs like '[m(x,y)]'
# It captures the numbers inside the parentheses
matches = re.findall(r'\[m\((\d+),(\d+)\)\]', behaviour_string)

# === 3. Parse each x/y point
parsed = []
# Loop through the found matches and create a list of dictionaries
for i, match in enumerate(matches):
    parsed.append({
        'x': int(match[0]),
        'y': int(match[1]),
        'timestamp': i  # Generate a simple incremental timestamp
    })

# === 4. Convert to DataFrame
df = pd.DataFrame(parsed)

# === 5. Null Check
print("\n📊 Null Value Summary:")
null_summary = df.isnull().sum()
percent_missing = (null_summary / len(df)) * 100 if len(df) > 0 else 0

summary_df = pd.DataFrame({
    'Null Count': null_summary,
    'Percent Missing': percent_missing
}).sort_values(by='Percent Missing', ascending=False)

print(summary_df)

# === 6. Preview
print("\n🔍 Data Preview:")
print(df.head())

print("\n🧮 Shape:", df.shape)