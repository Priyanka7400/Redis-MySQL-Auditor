import mysql.connector
import redis
import json
# MySQL Connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Devansh@4411",
    database="auditdb"
)

cursor = conn.cursor(dictionary=True)

# Redis Connection
r = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)
print("MySQL and Redis Connected Successfully!")
# Fetch all records from MySQL
cursor.execute("SELECT * FROM users")
mysql_data = cursor.fetchall()

print("MySQL Data:")
print(mysql_data)

# Store MySQL data into Redis
for row in mysql_data:
    r.set(f"user:{row['id']}", json.dumps(row))

print("All MySQL records have been stored in Redis.")
# Read one record from Redis
data = r.get("user:1")

print("Data from Redis:")
print(data)
import numpy as np

# Read all Redis records
redis_data = []
for row in mysql_data:
    redis_record = json.loads(r.get(f"user:{row['id']}"))
    redis_data.append(redis_record)

# Convert to NumPy arrays
mysql_array = np.array(mysql_data)
redis_array = np.array(redis_data)

# Compare records
matches = np.sum(mysql_array == redis_array)
total = len(mysql_data)

print("Matching Records:", matches)
print("Total Records:", total)
# Calculate consistency score
mismatches = total - matches
consistency_score = (matches / total) * 100

print("Mismatches:", mismatches)
print("Consistency Score:", round(consistency_score, 2), "%")
from datetime import datetime

audit_report = {
    "total_records_checked": int(total),
    "mismatches_found":int(mismatches),
    "consistency_score": f"{round(consistency_score,2)}%",
    "audit_timestamp": datetime.now().isoformat()
}

with open("audit_report.json", "w") as f:
    json.dump(audit_report, f, indent=4)

print("Audit Report Generated Successfully!")