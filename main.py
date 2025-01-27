from fastapi import FastAPI, HTTPException
import uvicorn
from classes import ProductNode, BST, OrderNode, OrderList, Product, Order
import json

app = FastAPI()

# Instancias
product_tree = BST()
order_list = OrderList()

# Endpoints
@app.post("/products/")
def create_product(product: Product):
    product_tree.insert(product.id, product.name, product.price)
    return {"message": "Producto agregado"}

@app.get("/products/{product_id}")
def get_product(product_id: int):
    product = product_tree.search(product_id)
    if product:
        return json.loads(json.dumps({"id": product.id, "name": product.name, "price": product.price}))
    raise HTTPException(status_code=404, detail="Producto no encontrado")

@app.post("/orders/")
def create_order(order: Order):
    order_list.add_order(order.id, order.products)
    return {"message": "Pedido creado"}

@app.get("/orders/{order_id}")
def get_order(order_id: int):
    order = order_list.get_order(order_id)
    if order:
        return order
    raise HTTPException(status_code=404, detail="Pedido no encontrado")

@app.put("/orders/{order_id}")
def update_order(order_id: int, order: Order):
    if order_list.update_order(order_id, order.products):
        return {"message": "Pedido actualizado"}
    raise HTTPException(status_code=404, detail="Pedido no encontrado")

@app.delete("/orders/{order_id}")
def delete_order(order_id: int):
    if order_list.delete_order(order_id):
        return {"message": "Pedido eliminado"}
    raise HTTPException(status_code=404, detail="Pedido no encontrado")

@app.get("/orders/")
def list_orders():
    return order_list.list_orders()

if __name__ == "__main__":
    
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)