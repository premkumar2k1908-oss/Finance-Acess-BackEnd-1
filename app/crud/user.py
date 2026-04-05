from sqlalchemy.future import select
from app.models.user import User

async def get_user_by_email(db, email: str):
    result = await db.execute(select(User).where(User.email == email))
    return result.scalars().first()