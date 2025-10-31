from fastapi import FastAPI, HTTPException, Depends, File, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, timedelta
import os
import shutil
import jwt
from passlib.context import CryptContext
import databases
import sqlalchemy
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, DateTime, ForeignKey, Text, ARRAY

# Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

# Database URL - supports both SQLite (development) and PostgreSQL (production)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./wine_notes.db")
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

database = databases.Database(DATABASE_URL)
metadata = MetaData()

# Tables
users_table = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String(255), unique=True, nullable=False),
    Column("name", String(255)),
    Column("google_id", String(255), unique=True),
    Column("created_at", DateTime, default=datetime.utcnow),
)

wine_notes_table = Table(
    "wine_notes",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id"), nullable=False),
    Column("wine_name", String(255), nullable=False),
    Column("vintage", Integer),
    Column("varietal", String(255), nullable=False),
    Column("region", String(255)),
    Column("producer", String(255)),
    Column("color", String(50), nullable=False),
    Column("rating", Float),
    Column("tasting_date", String(50)),
    Column("price", Float),
    Column("appearance", Text),
    Column("aroma", Text),
    Column("taste", Text),
    Column("finish", Text),
    Column("food_pairing", Text),
    Column("notes", Text),
    Column("drinking_with", String(255)),
    Column("meal_type", String(50)),
    Column("photos", ARRAY(String) if "postgresql" in DATABASE_URL else Text),  # JSON array for SQLite
    Column("created_at", DateTime, default=datetime.utcnow),
)

# Create engine and tables
if "sqlite" in DATABASE_URL:
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)
    
metadata.create_all(engine)

app = FastAPI(title="Wine Notes API")

# CORS - Update with your production domain
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Photo uploads
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# Security
security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Models
class User(BaseModel):
    id: Optional[int] = None
    email: str
    name: Optional[str] = None
    google_id: Optional[str] = None

class GoogleAuthRequest(BaseModel):
    token: str
    
class WineNote(BaseModel):
    id: Optional[int] = None
    wine_name: str
    vintage: Optional[int] = None
    varietal: str
    region: Optional[str] = None
    producer: Optional[str] = None
    color: str
    rating: Optional[float] = None
    tasting_date: Optional[str] = None
    price: Optional[float] = None
    appearance: Optional[str] = None
    aroma: Optional[str] = None
    taste: Optional[str] = None
    finish: Optional[str] = None
    food_pairing: Optional[str] = None
    notes: Optional[str] = None
    drinking_with: Optional[str] = None
    meal_type: Optional[str] = None
    photos: Optional[List[str]] = None
    created_at: Optional[str] = None

# Helper functions
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        return user_id
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

# Startup/Shutdown
@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# Routes
@app.get("/")
def root():
    return {"message": "Wine Notes API - Production Ready", "version": "2.0"}

@app.post("/api/auth/google")
async def google_auth(auth_request: GoogleAuthRequest):
    """
    Authenticate with Google OAuth token
    In production, verify the token with Google's API
    For now, this is a simplified version
    """
    # TODO: Verify token with Google API
    # For demo, we'll extract email from token payload (you need to add proper Google OAuth verification)
    
    try:
        # Decode token (in production, verify with Google)
        # This is simplified - implement proper Google OAuth verification
        payload = jwt.decode(auth_request.token, options={"verify_signature": False})
        email = payload.get("email")
        name = payload.get("name")
        google_id = payload.get("sub")
        
        if not email:
            raise HTTPException(status_code=400, detail="Invalid token")
        
        # Check if user exists
        query = users_table.select().where(users_table.c.email == email)
        user = await database.fetch_one(query)
        
        if not user:
            # Create new user
            query = users_table.insert().values(
                email=email,
                name=name,
                google_id=google_id
            )
            user_id = await database.execute(query)
        else:
            user_id = user["id"]
        
        # Create access token
        access_token = create_access_token({"user_id": user_id, "email": email})
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {"id": user_id, "email": email, "name": name}
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Authentication failed: {str(e)}")

@app.post("/api/auth/demo-login")
async def demo_login(email: str):
    """Demo login for testing - remove in production"""
    query = users_table.select().where(users_table.c.email == email)
    user = await database.fetch_one(query)
    
    if not user:
        query = users_table.insert().values(email=email, name=email.split("@")[0])
        user_id = await database.execute(query)
    else:
        user_id = user["id"]
    
    access_token = create_access_token({"user_id": user_id, "email": email})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {"id": user_id, "email": email}
    }

@app.get("/api/notes", response_model=List[WineNote])
async def get_notes(user_id: int = Depends(get_current_user)):
    """Get all wine notes for current user"""
    query = wine_notes_table.select().where(wine_notes_table.c.user_id == user_id).order_by(wine_notes_table.c.created_at.desc())
    notes = await database.fetch_all(query)
    return notes

@app.get("/api/notes/{note_id}", response_model=WineNote)
async def get_note(note_id: int, user_id: int = Depends(get_current_user)):
    """Get specific wine note"""
    query = wine_notes_table.select().where(
        (wine_notes_table.c.id == note_id) & (wine_notes_table.c.user_id == user_id)
    )
    note = await database.fetch_one(query)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@app.post("/api/notes", response_model=WineNote)
async def create_note(note: WineNote, user_id: int = Depends(get_current_user)):
    """Create new wine note"""
    note_dict = note.dict(exclude={"id", "created_at"})
    note_dict["user_id"] = user_id
    note_dict["created_at"] = datetime.utcnow()
    
    # Handle photos (convert list to JSON string for SQLite)
    if "sqlite" in DATABASE_URL and note_dict.get("photos"):
        import json
        note_dict["photos"] = json.dumps(note_dict["photos"])
    
    query = wine_notes_table.insert().values(**note_dict)
    note_id = await database.execute(query)
    
    # Fetch and return the created note
    return await get_note(note_id, user_id)

@app.put("/api/notes/{note_id}", response_model=WineNote)
async def update_note(note_id: int, note: WineNote, user_id: int = Depends(get_current_user)):
    """Update wine note"""
    # Check ownership
    existing = await get_note(note_id, user_id)
    
    note_dict = note.dict(exclude={"id", "created_at", "user_id"})
    
    # Handle photos for SQLite
    if "sqlite" in DATABASE_URL and note_dict.get("photos"):
        import json
        note_dict["photos"] = json.dumps(note_dict["photos"])
    
    query = wine_notes_table.update().where(
        (wine_notes_table.c.id == note_id) & (wine_notes_table.c.user_id == user_id)
    ).values(**note_dict)
    
    await database.execute(query)
    return await get_note(note_id, user_id)

@app.delete("/api/notes/{note_id}")
async def delete_note(note_id: int, user_id: int = Depends(get_current_user)):
    """Delete wine note"""
    # Get note to delete associated photos
    note = await get_note(note_id, user_id)
    
    if note.photos:
        for photo in note.photos:
            photo_path = os.path.join(UPLOAD_DIR, photo)
            if os.path.exists(photo_path):
                os.remove(photo_path)
    
    query = wine_notes_table.delete().where(
        (wine_notes_table.c.id == note_id) & (wine_notes_table.c.user_id == user_id)
    )
    await database.execute(query)
    return {"message": "Note deleted successfully"}

@app.post("/api/upload-photo/{note_id}")
async def upload_photo(
    note_id: int,
    file: UploadFile = File(...),
    user_id: int = Depends(get_current_user)
):
    """Upload photo for wine note"""
    # Verify ownership
    note = await get_note(note_id, user_id)
    
    # Generate unique filename
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{user_id}_{note_id}_{datetime.now().timestamp()}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    
    # Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Update note with photo
    current_photos = note.photos or []
    if isinstance(current_photos, str):
        import json
        current_photos = json.loads(current_photos)
    
    current_photos.append(unique_filename)
    
    if "sqlite" in DATABASE_URL:
        import json
        photos_value = json.dumps(current_photos)
    else:
        photos_value = current_photos
    
    query = wine_notes_table.update().where(
        (wine_notes_table.c.id == note_id) & (wine_notes_table.c.user_id == user_id)
    ).values(photos=photos_value)
    
    await database.execute(query)
    
    return {"filename": unique_filename, "url": f"/uploads/{unique_filename}"}

@app.delete("/api/delete-photo/{note_id}/{filename}")
async def delete_photo(note_id: int, filename: str, user_id: int = Depends(get_current_user)):
    """Delete photo from wine note"""
    note = await get_note(note_id, user_id)
    
    current_photos = note.photos or []
    if isinstance(current_photos, str):
        import json
        current_photos = json.loads(current_photos)
    
    if filename in current_photos:
        current_photos.remove(filename)
        
        # Delete file
        photo_path = os.path.join(UPLOAD_DIR, filename)
        if os.path.exists(photo_path):
            os.remove(photo_path)
        
        if "sqlite" in DATABASE_URL:
            import json
            photos_value = json.dumps(current_photos)
        else:
            photos_value = current_photos
        
        query = wine_notes_table.update().where(
            (wine_notes_table.c.id == note_id) & (wine_notes_table.c.user_id == user_id)
        ).values(photos=photos_value)
        
        await database.execute(query)
        
        return {"message": "Photo deleted successfully"}
    
    raise HTTPException(status_code=404, detail="Photo not found")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
