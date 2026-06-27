import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import json
import random

print("=== Redis-MySQL Consistency Auditor ===")

# --- STEP 1: Dummy Data Generation (Simulating Databases) ---
print("\n[1/4] Generating 100 records from MySQL & Redis...")

# Hum 100 users ka fake data bana rahe hain
mysql_database = {}
redis_cache = {}

for user_id in range(1, 101):
    original_balance = random.randint(100, 5000)
    mysql_database[user_id] = original_balance
    
    # 95% data sync rahega, 5% data jaanbujhkar mismatch karenge test karne ke liye
    if random.random() > 0.05:
        redis_cache[user_id] = original_balance
    else:
        redis_cache[user_id] = original_balance + random.choice([-200, 500, -100])

print("✓ Simulated MySQL Database & Redis Cache successfully.")

# --- STEP 2: Fetching and Data Comparison using NumPy ---
print("\n[2/4] Auditing data consistency using NumPy arrays...")

mysql_list = []
redis_list = []

for user_id in range(1, 101):
    mysql_list.append([user_id, mysql_database[user_id]])
    redis_list.append([user_id, redis_cache.get(user_id, -1)])

# Converting to NumPy Arrays
arr_mysql = np.array(mysql_list)
arr_redis = np.array(redis_list)

# Comparing balances (Index 1)
mismatches_mask = arr_mysql[:, 1] != arr_redis[:, 1]
mismatches_count = np.sum(mismatches_mask)

total_records = 100
consistency_score = ((total_records - mismatches_count) / total_records) * 100

print(f"✓ Audit complete. Found {mismatches_count} mismatches.")

# --- STEP 3: Visualizing with Matplotlib ---
print("\n[3/4] Generating Consistency Heatmap...")

grid_data = np.ones(100)
grid_data[mismatches_mask] = 0  # 0 represents mismatch (Red)
grid_matrix = grid_data.reshape((10, 10))

plt.figure(figsize=(6, 6))
plt.imshow(grid_matrix, cmap='RdYlGn', interpolation='nearest')
plt.title(f"Redis-MySQL Consistency Heatmap\nScore: {consistency_score}%")
plt.colorbar(label="0: Mismatch (Red) | 1: In Sync (Green)")
print("✓ Close the graph window to see the final JSON output.")
plt.show()

# --- STEP 4: Output JSON Report ---
print("\n[4/4] Final Audit Report (JSON):")

output_report = {
    "total_records_checked": int(total_records),
    "mismatches_found": int(mismatches_count),
    "consistency_score": f"{consistency_score:.1f}%",
    "audit_timestamp": datetime.now().isoformat(timespec='seconds')
}

print(json.dumps(output_report, indent=2))