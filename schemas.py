"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import date

# Example schemas (replace with your own):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Hotel and Airbnb booking schemas for this app

class HotelBooking(BaseModel):
    """
    Hotel bookings collection schema
    Collection name: "hotelbooking" (lowercase of class name)
    """
    full_name: str = Field(..., description="Guest full name")
    email: EmailStr = Field(..., description="Guest email")
    destination: str = Field(..., description="City or location")
    check_in: date = Field(..., description="Check-in date")
    check_out: date = Field(..., description="Check-out date")
    guests: int = Field(..., ge=1, le=10, description="Number of guests")
    rooms: int = Field(1, ge=1, le=5, description="Number of rooms")
    room_type: Optional[str] = Field(None, description="Room type preference")
    special_requests: Optional[str] = Field(None, description="Special requests")

class AirbnbBooking(BaseModel):
    """
    Airbnb-style bookings collection schema
    Collection name: "airbnbbooking" (lowercase of class name)
    """
    guest_name: str = Field(..., description="Guest full name")
    email: EmailStr = Field(..., description="Guest email")
    listing_name: Optional[str] = Field(None, description="Preferred listing name if any")
    location: str = Field(..., description="City or neighborhood")
    check_in: date = Field(..., description="Check-in date")
    check_out: date = Field(..., description="Check-out date")
    guests: int = Field(..., ge=1, le=12, description="Number of guests")
    budget_per_night: Optional[float] = Field(None, ge=0, description="Target budget per night")
    notes: Optional[str] = Field(None, description="Additional notes or requests")

# Add your own schemas here:
# --------------------------------------------------

# Note: The Flames database viewer will automatically:
# 1. Read these schemas from GET /schema endpoint
# 2. Use them for document validation when creating/editing
# 3. Handle all database operations (CRUD) directly
# 4. You don't need to create any database endpoints!
