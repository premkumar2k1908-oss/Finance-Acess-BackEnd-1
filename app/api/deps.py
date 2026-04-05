from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import verify_password
from app.crud.user import get_user_by_email
from app.core.config import settings
from app.models.user import Role

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await get_user_by_email(db, email=email)
    if not user or not verify_password(token, user.hashed_password):  # Simplified; use payload.id
        raise credentials_exception
    return user

def require_role(required_role: Role):
    def role_checker(current_user: User = Depends(get_current_user)):
        role_hierarchy = {Role.VIEWER: 0, Role.ANALYST: 1, Role.ADMIN: 2}
        if role_hierarchy[current_user.role] < role_hierarchy[required_role]:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return current_user
    return role_checker