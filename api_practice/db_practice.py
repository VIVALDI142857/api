from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from fastapi import FastAPI, Depends
from typing import Annotated
from pydantic import BaseModel

engine = create_async_engine('sqlite+aiosqlite:///cars.db')

new_session = async_sessionmaker(engine, expire_on_commit=False)

app = FastAPI()

async def get_session():
    async with new_session as session:
        yield session
        
        
SessionDep = Annotated[AsyncSession, Depends(get_session)]


class Base(DeclarativeBase):
    pass

class CarModel(Base):
    __tablename__ = 'cars'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    model: Mapped[str]
    brand: Mapped[str]
    
class SchemaAddCar(BaseModel):
    model: str
    brand: str
    
class CarSchema(SchemaAddCar):
    id: int
    

@app.post('/setup_database')    
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    return {'success': True}
    


    
@app.post('/cars')
async def add_car(data: SchemaAddCar, session:SessionDep):
    new_car = CarModel(
        model = data.model,
        brand = data.brand
    )
    session.add(new_car)
    await session.commit()
    await session.refresh(new_car)
    return {'id': new_car.id, 'model': new_car.model, 'brand': new_car.brand}

@app.get('/cars', response_model=list[CarSchema])
async def get_cars(session: SessionDep):
    cars = await session.execute('SELECT * FROM cars')
    return cars.fetchall()