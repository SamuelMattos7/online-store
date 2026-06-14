import urllib.parse
from datetime import datetime
from sqlalchemy import (
    create_engine, Column, Integer, String, Text, 
    Float, Boolean, DateTime, ForeignKey, text
)
from sqlalchemy.orm import declarative_base, relationship

# 1. Define your credentials
DB_USER = "postgres"
DB_PASSWORD = "Valquiria4512"  
DB_HOST = "menu.c126y46ect0b.us-east-2.rds.amazonaws.com"
DB_PORT = "5432"
DB_NAME = "menu"

# 2. Handle special characters in passwords (highly recommended)
# This prevents SQLAlchemy from misinterpreting symbols like '@' or ':' in your password
safe_password = urllib.parse.quote_plus(DB_PASSWORD)

# 3. Construct the Connection URI
DATABASE_URL = f"postgresql://{DB_USER}:{safe_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, connect_args={"sslmode": "require"})
Base = declarative_base()

# 2. Table Definitions (Models)

class Customer(Base):
    __tablename__ = 'customers'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    phone = Column(String(20), nullable=False)
    full_name = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class Category(Base):
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)
    sort_order = Column(Integer, default=0)
    
    # Optional: Relationship to easily fetch items belonging to this category
    items = relationship("MenuItem", back_populates="category")


class MenuItem(Base):
    __tablename__ = 'menu_items'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    # Using Float mapping to preserve the (10, 2) precision from your SQL
    price = Column(Float(10, 2), nullable=False)
    is_available = Column(Boolean, default=True)
    preparation_time_minutes = Column(Integer, default=15)
    image_url = Column(Text, nullable=True)
    
    # Links back to the Category model
    category = relationship("Category", back_populates="items")


# 3. Execution Block
if __name__ == "__main__":
    try:
        print("Connecting to RDS and generating tables...")
        # This line checks what tables are missing in RDS and creates them
        Base.metadata.create_all(engine)
        print("--- Tables Created Successfully! ---")
        
        # Verify by printing the table names currently in the database
        with engine.connect() as conn:
            inspector = text(
                "SELECT table_name FROM information_schema.tables WHERE table_schema='public';"
            )
            tables = conn.execute(inspector).fetchall()
            print("Current tables in database:")
            for table in tables:
                print(f" - {table[0]}")
                
    except Exception as e:
        print("--- Table Creation Failed ---")
        print(e)