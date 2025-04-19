from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Dict
from itertools import permutations

app = FastAPI()

warehouse_stock = {
    "C1": {"A", "B", "C"},
    "C2": {"D", "E", "F"},
    "C3": {"G", "H", "I"}
}

distances = {
    ("C1", "L1"): 10,
    ("C2", "L1"): 20,
    ("C3", "L1"): 15,
    ("C1", "C2"): 10,
    ("C1", "C3"): 12,
    ("C2", "C3"): 8,
    ("C2", "C1"): 10,
    ("C3", "C1"): 12,
    ("C3", "C2"): 8,
    ("L1", "C1"): 10,
    ("L1", "C2"): 20,
    ("L1", "C3"): 15
}

cost_per_km = 1
product_weight = 0.5

class Order(BaseModel):
    __root__: Dict[str, int]

def get_cost(path):
    return sum(distances.get((path[i], path[i+1]), 0) for i in range(len(path)-1)) * cost_per_km

def calculate_delivery_cost(order: Dict[str, int]) -> int:
    centers_needed = set()
    for product in order:
        for center, products in warehouse_stock.items():
            if product in products:
                centers_needed.add(center)
                break

    min_total_cost = float('inf')
    for start in centers_needed:
        for perm in permutations(centers_needed - {start}):
            route = [start]
            for center in perm:
                route += ["L1", center]
            route += ["L1"]
            cost = get_cost(route)
            if cost < min_total_cost:
                min_total_cost = cost

    return int(min_total_cost)

@app.post("/calculate")
async def calculate(request: Order):
    order_data = request.__root__
    cost = calculate_delivery_cost(order_data)
    return {"minimum_cost": cost}
