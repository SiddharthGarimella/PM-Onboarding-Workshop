import requests
import pandas as pd
import matplotlib.pyplot as plt

API_URL = "http://localhost:3001/inventory"
LOW_STOCK_THRESHOLD = 5  # items at or below this quantity are considered low stock

# Pull the live inventory from the Module 2/3 Express backend — same data
# the React dashboard is already displaying, just viewed through pandas instead.
response = requests.get(API_URL)
data = response.json()

df = pd.DataFrame(data)

# --- Total number of items ---
total_items = len(df)

# --- Group items by category ---
by_category = df.groupby("category").size()

# --- Identify low stock items ---
low_stock = df[df["quantity"] <= LOW_STOCK_THRESHOLD]
low_stock_count = len(low_stock)

print(df)
print("\nTotal items:", total_items)
print("\nItems by category:")
print(by_category)
print(f"\nLow stock items (quantity <= {LOW_STOCK_THRESHOLD}):", low_stock_count)
print(low_stock[["name", "quantity"]])

# --- Simple visualization: item count by category ---
by_category.plot(kind="bar", title="Inventory items by category")
plt.xlabel("Category")
plt.ylabel("Number of items")
plt.tight_layout()
plt.savefig("inventory_by_category.png")
print("\nChart saved to inventory_by_category.png")
