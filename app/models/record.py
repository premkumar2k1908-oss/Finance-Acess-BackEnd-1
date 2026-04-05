from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class FinancialRecord(Base):
    __tablename__ = "financial_records"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    type = Column(String)  # income or expense
    category = Column(String)
    date = Column(Date)
    created_by = Column(Integer, ForeignKey("users.id"))