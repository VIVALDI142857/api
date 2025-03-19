from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from fastapi import FastAPI, Depends, File, UploadFile
from typing import Annotated
from pydantic import BaseModel
import pandas as pd
import io
from typing import Annotated, List

engine = create_async_engine('sqlite+aiosqlite:///clients.db')

new_session = async_sessionmaker(engine, expire_on_commit=False)

app = FastAPI()

async def get_session():
    async with new_session as session:
        yield session
        
        
SessionDep = Annotated[AsyncSession, Depends(get_session)]


class Base(DeclarativeBase):
    pass

class Clients(Base):
    __tablename__ = 'clients'
    id: Mapped[int] = mapped_column(primary_key=True)
    fea_1: Mapped[int]
    fea_2: Mapped[float]
    fea_3: Mapped[int]
    fea_4: Mapped[float]
    fea_5: Mapped[int]
    fea_6: Mapped[int]
    fea_7: Mapped[int]
    fea_8: Mapped[int]
    fea_9: Mapped[int]
    fea_10: Mapped[int]
    fea_11: Mapped[float]
    OVD_t1_mean: Mapped[float]
    OVD_t1_max: Mapped[int]
    OVD_t2_mean: Mapped[float]
    OVD_t2_max: Mapped[int]
    OVD_t3_mean: Mapped[float]
    OVD_t3_max: Mapped[int]
    pay_normal_mean: Mapped[float]
    pay_normal_max: Mapped[int]
    prod_code_median: Mapped[float]
    update_date_mean: Mapped[int]
    report_date_mean: Mapped[int]
    prod_limit_mean: Mapped[float]
    new_balance_mean: Mapped[float]
    highest_balance_mean: Mapped[float]
    
class AddClient(BaseModel):
    
    id: int
    fea_1: int
    fea_2: float
    fea_3: int
    fea_4: float
    fea_5: int
    fea_6: int
    fea_7: int
    fea_8: int
    fea_9: int
    fea_10: int
    fea_11: float
    OVD_t1_mean: float
    OVD_t1_max: int
    OVD_t2_mean: float
    OVD_t2_max: int
    OVD_t3_mean: float
    OVD_t3_max: int
    pay_normal_mean: float
    pay_normal_max: int
    prod_code_median: float
    update_date_mean: int
    report_date_mean: int
    prod_limit_mean: float
    new_balance_mean: float
    highest_balance_mean: float
    
    class Config:
        orm_mode = True 


    

@app.post('/setup_database')    
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    return {'success': True}
    


    
@app.post('/clients')
async def load_content(session: SessionDep, file: UploadFile = File(...)):
    contents =  await file.read()
    X_test = pd.read_csv(io.StringIO(contents.decode('utf-8')))
    new_clients = []
    for _, row in X_test.iterrows():
        new_client = Clients(
            id=int(row['id']),
            fea_1=int(row['fea_1']),
            fea_2=float(row['fea_2']),
            fea_3=int(row['fea_3']),
            fea_4=float(row['fea_4']),
            fea_5=int(row['fea_5']),
            fea_6=int(row['fea_6']),
            fea_7=int(row['fea_7']),
            fea_8=int(row['fea_8']),
            fea_9=int(row['fea_9']),
            fea_10=int(row['fea_10']),
            fea_11=float(row['fea_11']),
            OVD_t1_mean=float(row['OVD_t1_mean']),
            OVD_t1_max=int(row['OVD_t1_max']),
            OVD_t2_mean=float(row['OVD_t2_mean']),
            OVD_t2_max=int(row['OVD_t2_max']),
            OVD_t3_mean=float(row['OVD_t3_mean']),
            OVD_t3_max=int(row['OVD_t3_max']),
            pay_normal_mean=float(row['pay_normal_mean']),
            pay_normal_max=int(row['pay_normal_max']),
            prod_code_median=float(row['prod_code_median']),
            update_date_mean=int(row['update_date_mean']),
            report_date_mean=int(row['report_date_mean']),
            prod_limit_mean=float(row['prod_limit_mean']),
            new_balance_mean=float(row['new_balance_mean']),
            highest_balance_mean=float(row['highest_balance_mean'])
        )
        new_clients.append(new_client)
    session.add_all(new_clients)
    await session.commit()
    
    return {'status': 'success', 'added_rows': len(new_clients)}

# @app.get('/clients', response_model=List[AddClient])
# async def get_clients(session: SessionDep):
#     c = await session.execute('SELECT * FROM cars')
#     return c.fetchall()