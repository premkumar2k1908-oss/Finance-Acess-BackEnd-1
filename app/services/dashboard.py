from sqlalchemy import func, case
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.record import FinancialRecord

async def get_dashboard_summary(db: AsyncSession, user_id: int):
    stmt = select(
        func.sum(case((FinancialRecord.type == 'income', FinancialRecord.amount), else_=0)).label('total_income'),
        func.sum(case((FinancialRecord.type == 'expense', FinancialRecord.amount), else_=0)).label('total_expense'),
        func.json_group_array(func.json_object('category', FinancialRecord.category, 'total', func.sum(FinancialRecord.amount))).label('category_totals')
    ).where(FinancialRecord.created_by == user_id).group_by()
    result = await db.execute(stmt)
    row = result.fetchone()
    net_balance = row.total_income - row.total_expense if row else 0
    return {
        'total_income': row.total_income or 0,
        'total_expense': row.total_expense or 0,
        'net_balance': net_balance,
        'category_totals': row.category_totals or []
    }