from pydantic import BaseModel
from typing import Optional, List
import json

class ProductNode:
    def __init__(self, id: int, name: str, price: float):
        self.id = id
        self.name = name
        self.price = price
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None
    
    def insert(self, id: int, name: str, price: float):
        if not self.root:
            self.root = ProductNode(id, name, price)
        else:
            self._insert(self.root, id, name, price)
    
    def _insert(self, node, id, name, price):
        if id < node.id:
            if node.left is None:
                node.left = ProductNode(id, name, price)
            else:
                self._insert(node.left, id, name, price)
        else:
            if node.right is None:
                node.right = ProductNode(id, name, price)
            else:
                self._insert(node.right, id, name, price)
    
    def search(self, id: int):
        return self._search(self.root, id)
    
    def _search(self, node, id):
        if node is None or node.id == id:
            return node
        if id < node.id:
            return self._search(node.left, id)
        return self._search(node.right, id)

# Lista enlazada para gestionar pedidos
class OrderNode:
    def __init__(self, id: int, products: List[int]):
        self.id = id
        self.products = products
        self.next = None

class OrderList:
    def __init__(self):
        self.head = None
    
    def add_order(self, id: int, products: List[int]):
        new_order = OrderNode(id, products)
        new_order.next = self.head
        self.head = new_order
    
    def get_order(self, id: int):
        current = self.head
        while current:
            if current.id == id:
                return json.loads(json.dumps({"id": current.id, "products": current.products}))
            current = current.next
        return None
    
    def delete_order(self, id: int):
        current = self.head
        prev = None
        while current and current.id != id:
            prev = current
            current = current.next
        if current is None:
            return False
        if prev is None:
            self.head = current.next
        else:
            prev.next = current.next
        return True
    
    def update_order(self, id: int, products: List[int]):
        current = self.head
        while current:
            if current.id == id:
                current.products = products
                return True
            current = current.next
        return False
    
    def list_orders(self):
        orders = []
        current = self.head
        while current:
            orders.append(json.loads(json.dumps({"id": current.id, "products": current.products})))
            current = current.next
        return orders

# Modelos para FastAPI
class Product(BaseModel):
    id: int
    name: str
    price: float

class Order(BaseModel):
    id: int
    products: List[int]