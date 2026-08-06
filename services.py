from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import Account, TransactionHistory

async def transfer_funds(session: AsyncSession, sender_account_id: int, receiver_account_id: int,
                         amount: float) -> bool:
    if amount <= 0:
        raise ValueError('Сумма перевода должна быть больше 0')
    if sender_account_id == receiver_account_id:
        failed_tx = TransactionHistory(sender_account_id=sender_account_id, receiver_account_id=receiver_account_id,
                                       amount=amount, status='FAILED', description='Перевод на один и тот же счет'
                                       )
        session.add(failed_tx)
        await session.commit()
        return False

    try:
        sender_res = await session.execute(select(Account).where(Account.id == sender_account_id))
        receiver_res = await session.execute(select(Account).where(Account.id == receiver_account_id))
        sender = sender_res.scalar_one_or_none()
        receiver = receiver_res.scalar_one_or_none()

        if not sender or not receiver:
            raise  ValueError('Один или оба счета не найдены')

        if not sender.is_active or not receiver.is_active:
            raise  ValueError('Один или оба счета неактивны')

        if sender.balance < amount:
            raise ValueError('Недостаточно средств')

        sender.balance -= amount
        receiver.balance += amount

        success_tx = TransactionHistory(sender_account_id=sender.id, receiver_account_id=receiver.id, amount=amount,
                                        status='SUCCESS', description='еревод выполнен успешно')
        session.add(success_tx)
        await session.commit()
        return True

    except Exception as e:
        await session.rollback()
        failed_tx = TransactionHistory(sender_account_id=sender_account_id, receiver_account_id=receiver_account_id,
                                       amount=amount, status='FAILED', description=str(e)
                                       )
        session.add(failed_tx)
        await session.commit()
        return False
