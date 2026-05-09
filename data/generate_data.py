"""
generate_data.py
Generates realistic synthetic data for Sonido Digital Guatemala.
Run once to produce: products.csv, inventory.csv, sales.csv, inquiries.csv
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

np.random.seed(42)
random.seed(42)

# ── PRODUCT CATALOG ────────────────────────────────────────────────────────────
products = [
    # (id, name, brand, category, cost, price, reorder_point, max_stock)
    ("P001", "Memphis 15-MJP124",    "Memphis Audio",    "Subwoofer",     1200, 2199, 5, 30),
    ("P002", "Memphis MXA300.4",     "Memphis Audio",    "Amplificador",  1800, 3299, 4, 20),
    ("P003", "Memphis PRX500.1",     "Memphis Audio",    "Amplificador",  2400, 4499, 3, 15),
    ("P004", "Rockford T1D412",      "Rockford Fosgate", "Subwoofer",     2200, 3999, 4, 25),
    ("P005", "Rockford R500X1D",     "Rockford Fosgate", "Amplificador",  1600, 2899, 5, 20),
    ("P006", "Rockford P3D4-12",     "Rockford Fosgate", "Subwoofer",     1400, 2599, 6, 30),
    ("P007", "Pioneer AVH-W4500NEX", "Pioneer",          "Head Unit",     2800, 4999, 3, 15),
    ("P008", "Pioneer TS-A1680F",    "Pioneer",          "Bocinas",        350,  699, 10, 50),
    ("P009", "Pioneer TS-WX130DA",   "Pioneer",          "Subwoofer",      900, 1699, 6, 25),
    ("P010", "JBL GT-BassPro12",     "JBL",              "Subwoofer",     1100, 1999, 5, 25),
    ("P011", "JBL Stadium 52F",      "JBL",              "Bocinas",        500,  999, 8, 40),
    ("P012", "JBL Club 5001",        "JBL",              "Amplificador",  1300, 2399, 4, 20),
    ("P013", "Cerwin Vega VPAS10",   "Cerwin Vega",      "Subwoofer",      950, 1799, 5, 20),
    ("P014", "Cerwin Vega HED H740", "Cerwin Vega",      "Bocinas",        420,  849, 8, 35),
    ("P015", "KBT BT-7500",         "KBT Electronics",  "Head Unit",     1200, 2199, 4, 20),
    ("P016", "KBT AMP-1500D",        "KBT Electronics",  "Amplificador",   950, 1799, 5, 20),
    ("P017", "Stinger SGP32",        "Stinger",          "Accesorios",     180,  349, 15, 60),
    ("P018", "Stinger SHW12G",       "Stinger",          "Accesorios",     120,  249, 20, 80),
    ("P019", "Soundskins SS-1SQ",    "Soundskins",       "Accesorios",     280,  549, 12, 50),
    ("P020", "Soundskins Pro Roll",  "Soundskins",       "Accesorios",     350,  699, 10, 40),
]

df_products = pd.DataFrame(products, columns=[
    "product_id","product_name","brand","category",
    "cost_gtq","price_gtq","reorder_point","max_stock"
])
df_products.to_csv("/home/claude/sonido_digital/data/products.csv", index=False)

# ── INVENTORY ──────────────────────────────────────────────────────────────────
inventory_rows = []
for _, p in df_products.iterrows():
    stock = random.randint(0, p["max_stock"])
    inventory_rows.append({
        "product_id":     p["product_id"],
        "current_stock":  stock,
        "reorder_point":  p["reorder_point"],
        "max_stock":      p["max_stock"],
        "last_restock":   (datetime.today() - timedelta(days=random.randint(5, 60))).strftime("%Y-%m-%d"),
        "status": "Crítico" if stock == 0 else
                  "Bajo"    if stock <= p["reorder_point"] else
                  "OK"      if stock <= p["max_stock"] * 0.75 else "Sobrestock"
    })

df_inventory = pd.DataFrame(inventory_rows)
df_inventory.to_csv("/home/claude/sonido_digital/data/inventory.csv", index=False)

# ── SALES HISTORY (18 months) ──────────────────────────────────────────────────
start_date = datetime(2024, 1, 1)
end_date   = datetime(2025, 6, 30)
date_range = pd.date_range(start_date, end_date, freq="D")

# Seasonal multipliers (month 1-12)
seasonality = {1:0.9, 2:0.85, 3:1.0, 4:1.0, 5:0.95, 6:1.15,
               7:1.1, 8:1.0, 9:0.95, 10:1.05, 11:1.2, 12:1.4}

# Category base daily sales probability
base_prob = {
    "Subwoofer":    0.55,
    "Amplificador": 0.45,
    "Head Unit":    0.35,
    "Bocinas":      0.60,
    "Accesorios":   0.70,
}

sales_rows = []
sale_id = 1
for date in date_range:
    s_mult = seasonality[date.month]
    # Weekend boost
    w_mult = 1.3 if date.weekday() >= 5 else 1.0
    for _, p in df_products.iterrows():
        prob = base_prob[p["category"]] * s_mult * w_mult * 0.3
        if random.random() < prob:
            qty = random.randint(1, 3)
            discount = random.choice([0, 0, 0, 0.05, 0.10])
            revenue = round(qty * p["price_gtq"] * (1 - discount), 2)
            sales_rows.append({
                "sale_id":    f"S{sale_id:05d}",
                "date":       date.strftime("%Y-%m-%d"),
                "product_id": p["product_id"],
                "brand":      p["brand"],
                "category":   p["category"],
                "quantity":   qty,
                "unit_price": p["price_gtq"],
                "discount":   discount,
                "revenue_gtq":revenue,
                "profit_gtq": round(qty * (p["price_gtq"] * (1-discount) - p["cost_gtq"]), 2),
            })
            sale_id += 1

df_sales = pd.DataFrame(sales_rows)
df_sales.to_csv("/home/claude/sonido_digital/data/sales.csv", index=False)

# ── CUSTOMER INQUIRIES ─────────────────────────────────────────────────────────
channels  = ["WhatsApp", "Instagram", "TikTok", "Facebook", "Tienda física"]
ch_prob   = [0.40,       0.25,        0.15,     0.12,       0.08]
outcomes  = ["Venta concretada", "Cotización enviada", "Sin respuesta", "Cancelado"]
out_prob  = [0.35, 0.30, 0.20, 0.15]

inq_rows = []
for i, date in enumerate(pd.date_range("2024-06-01", "2025-06-30", freq="D")):
    n = random.randint(1, 6)
    for _ in range(n):
        cat = random.choice(list(base_prob.keys()))
        inq_rows.append({
            "inquiry_id": f"I{i*10+_:05d}",
            "date":       date.strftime("%Y-%m-%d"),
            "channel":    np.random.choice(channels, p=ch_prob),
            "category":   cat,
            "outcome":    np.random.choice(outcomes, p=out_prob),
        })

df_inquiries = pd.DataFrame(inq_rows)
df_inquiries.to_csv("/home/claude/sonido_digital/data/inquiries.csv", index=False)

print("✅ Data generated:")
print(f"  products.csv    → {len(df_products)} products")
print(f"  inventory.csv   → {len(df_inventory)} SKUs")
print(f"  sales.csv       → {len(df_sales)} transactions")
print(f"  inquiries.csv   → {len(df_inquiries)} inquiries")
