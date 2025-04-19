
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict

app = FastAPI()

product_centers = {
    "C1": {"A", "B", "C"},
    "C2": {"D", "E", "F"},
    "C3": {"G", "H", "I"},
}

center_distances = {
    "C1": 10,
    "C2": 15,
    "C3": 20,
}

cost_per_km = 2

class Order(BaseModel):
    A: int = 0
    B: int = 0
    C: int = 0
    D: int = 0
    E: int = 0
    F: int = 0
    G: int = 0
    H: int = 0
    I: int = 0

def calculate_cost(order: Dict[str, int]) -> int:
    products = {k: v for k, v in order.items() if v > 0}
    min_total_cost = float('inf')

    for start_center in center_distances:
        total_cost = 0
        current_location = start_center
        remaining = dict(products)

        while remaining:
            found = False
            for center in center_distances:
                center_products = product_centers[center]
                to_pick = {p for p in remaining if p in center_products}
                if to_pick:
                    travel = abs(center_distances[center] - center_distances[current_location])
                    trip_cost = travel * cost_per_km + center_distances[center] * cost_per_km
                    total_cost += trip_cost
                    current_location = center
                    for product in to_pick:
                        del remaining[product]
                    found = True
                    break
            if not found:
                break

        min_total_cost = min(min_total_cost, total_cost)

    return int(min_total_cost)

@app.post("/calculate-cost")
def calculate_delivery_cost(order: Order):
    order_dict = order.dict()
    cost = calculate_cost(order_dict)
    return {"cost": cost}





'''
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
    '''
