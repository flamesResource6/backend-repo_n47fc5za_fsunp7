import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any, Dict

from database import create_document
from schemas import HotelBooking, AirbnbBooking

app = FastAPI(title="StayHub API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "StayHub backend is running"}

@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        from database import db
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = db.name if hasattr(db, 'name') else "Unknown"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    # Environment
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"

    return response

# Booking endpoints
@app.post("/api/bookings/hotel")
def create_hotel_booking(booking: HotelBooking):
    try:
        booking_id = create_document("hotelbooking", booking)
        return {"status": "ok", "id": booking_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/bookings/airbnb")
def create_airbnb_booking(booking: AirbnbBooking):
    try:
        booking_id = create_document("airbnbbooking", booking)
        return {"status": "ok", "id": booking_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Expose schemas for tooling
class SchemaResponse(BaseModel):
    schemas: Dict[str, Any]

@app.get("/schema")
def get_schema() -> Dict[str, Any]:
    return {
        "hotelbooking": HotelBooking.model_json_schema(),
        "airbnbbooking": AirbnbBooking.model_json_schema(),
    }


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
