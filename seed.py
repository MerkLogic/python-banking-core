import asyncio
from database import engine, Base, async_session_factory
from models import Account, Client

async def seed_data():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with async_session_factory() as session:
        c1 = Client(full_name='Иван Иванов', email='ivan@ex.com')
        c2 = Client(full_name='Петр Петров', email='petr@ex.com')
        c3 = Client(full_name='Василий Васильев', email='vasiliy@ex.com')

        session.add_all([c1, c2, c3])
        await session.flush()#получаем ID клиента

        a1 = Account(account_number='4081781000000000000001', client_id=c1.id, balance=15000.0)
        a2 = Account(account_number='4081781000000000000002', client_id=c1.id, balance=500.0)
        a3 = Account(account_number='4081781000000000000003', client_id=c2.id, balance=8000.0)
        a4 = Account(account_number='4081781000000000000004', client_id=c3.id, balance=1200.0, is_active=False)

        session.add_all([a1, a2, a3])
        await session.commit()
        print('БД инициализирована')
if __name__ == '__main__':
    asyncio.run(seed_data())