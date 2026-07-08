import pandas as pd
import sqlite3

files = ["chembarambakkam.csv", "poondi.csv", "cholavaram.csv", "redhills.csv", "veeranam.csv"]

reservoir_names = {
    "chembarambakkam.csv": "Chembarambakkam",
    "poondi.csv": "Poondi",
    "cholavaram.csv": "Cholavaram",
    "redhills.csv": "Red Hills",
    "veeranam.csv": "Veeranam"
}

months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

all_data = []

for file in files:
    print(f"\n{'='*40}")
    print(f"Processing: {file}")
    print(f"{'='*40}")
    
    df = pd.read_csv(f"raw_data/{file}")
    
    # Fix inconsistent 'Jan' column naming
    df.columns.values[1] = 'Jan'
    
    # Fix comma-formatted numbers (e.g. "1,049") and ensure all month columns are numeric
    df[months] = df[months].replace(",", "", regex=True).astype(float)
    
    # Reshape from wide to long format
    df_long = df.melt(id_vars=["Year"], value_vars=months,
                       var_name="Month", value_name="Level")
    
    df_long["Reservoir"] = reservoir_names[file]
    
    print("First 5 rows after reshaping:")
    print(df_long.head())
    print("\nData type of Level column:", df_long["Level"].dtype)
    
    all_data.append(df_long)

combined = pd.concat(all_data, ignore_index=True)

print(f"\n{'='*40}")
print("COMBINED DATASET")
print(f"{'='*40}")
print(combined.head())
print("\nFull combined shape:")
print(combined.shape)
print("\nUnique reservoirs in combined data:")
print(combined["Reservoir"].unique())
print("\nAny missing values?")
print(combined.isnull().sum())

# Save the cleaned, combined dataset into a SQLite database
conn = sqlite3.connect("chennai_water.db")
combined.to_sql("reservoir_levels", conn, if_exists="replace", index=False)
conn.close()

print("\nSaved to chennai_water.db successfully!")
# Verify by querying the database directly
conn = sqlite3.connect("chennai_water.db")
result = pd.read_sql("SELECT * FROM reservoir_levels LIMIT 10", conn)
print("\nSample query from database:")
print(result)

count = pd.read_sql("SELECT COUNT(*) as total_rows FROM reservoir_levels", conn)
print("\nTotal rows in database:")
print(count)

conn.close()