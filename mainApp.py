from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from contextlib import asynccontextmanager
from base import Product, create_db_and_tables, get_session, engine
from parser1 import parse_all_pages
from sqlmodel import Session, select
import asyncio


async def background_parser():
    while True:
        print("parser start")
        products = parse_all_pages()
        db = Session(engine)

        for product in products:
            if not db.exec(select(Product).where(Product.name == product[0])).first():
                db.add(Product(name=product[0], price=product[1]))

        db.commit()
        db.close()
        await asyncio.sleep(100)

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("lifespan start")
    create_db_and_tables()
    asyncio.create_task(background_parser())
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"Сообщение": "Добро пожаловать"}

@app.get("/products/")
async def get_products(session: Session = Depends(get_session)):
    return session.exec(select(Product)).all()

@app.get("/product/{product_id}")
async def get_product(product_id: int, session: Session = Depends(get_session)):
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Товар не найден")
    print("Продукт получен")
    return product

@app.post("/products/")
async def add_product(product: Product, session: Session = Depends(get_session)):
    session.add(product)
    session.commit()
    session.refresh(product)
    return product

@app.put("/products/{product_id}")
async def update_product(product_id: int, product: Product, session: Session = Depends(get_session)):
    dp_product = session.get(Product, product_id)
    if not dp_product:
        raise HTTPException(status_code=404, detail="Товар не найден")

    dp_product.name = product.name or dp_product.name
    dp_product.price = product.price or dp_product.name

    session.add(dp_product)
    session.commit()
    session.refresh(dp_product)
    return dp_product

@app.delete("/products/{product_id}")
async def delete_product(product_id: int, product: Product, session: Session = Depends(get_session)):
    dp_product = session.get(Product, product_id)
    if not dp_product:
        raise HTTPException(status_code=404, detail="Товар не найден")

    session.delete(dp_product)
    session.commit()
    return {"Товар удален": dp_product}