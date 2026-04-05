from pydantic import BaseModel
from datetime import date
from typing import List, Dict, Any

class DashboardOut(BaseModel):
    total_income: float
    total_expense: float
    net_balance: float
    category_totals: List[Any]

class RecordCreate(BaseModel):
    amount: float
    type: str   # "income" or "expense"
    category: str
    date: date

class RecordOut(BaseModel):
    id: int
    amount: float
    type: str
    category: str
    date: date
    created_by: int

    class Config:
        from_attributes = True