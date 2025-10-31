from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
import json
import os
import shutil
import jwt
import secrets

# Configuration
SECRET_KEY = os.getenv("SECRET_KEY", secrets.token_hex(32))
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 7

app = FastAPI(title="Wine Notes API")

# CORS
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")
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

try:
    app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")
except:
    pass

# Simple JSON file storage (works everywhere)
DATA_FILE = "wine_data.json"

def load_data() -> Dict[str, Any]:
    """Load all data from JSON file"""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    return {"users": {}, "notes": []}

def save_data(data: Dict[str, Any]):
    """Save all data to JSON file"""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def create_token(user_email: str) -> str:
    """Create JWT token"""
    expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    payload = {
        "email": user_email,
        "exp": expire
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str) -> Optional[str]:
    """Verify JWT token and return email"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("email")
    except:
        return None

def get_user_email(authorization: str) -> str:
    """Extract and verify user email from Authorization header"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    token = authorization.replace("Bearer ", "")
    email = verify_token(token)
    
    if not email:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    return email

@app.get("/")
def root():
    return {"message": "Wine Notes API - Production Ready", "version": "2.0"}

@app.post("/api/auth/demo-login")
def demo_login(request: Dict[str, Any]):
    """Demo login - just creates a token for any email"""
    email = request.get("email")
    if not email:
        raise HTTPException(status_code=400, detail="Email required")
    
    data = load_data()
    
    # Create user if doesn't exist
    if email not in data["users"]:
        data["users"][email] = {
            "email": email,
            "name": email.split("@")[0],
            "created_at": datetime.now().isoformat()
        }
        save_data(data)
    
    token = create_token(email)
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": data["users"][email]
    }

@app.get("/api/notes")
def get_notes(authorization: str = ""):
    """Get all wine notes for current user"""
    email = get_user_email(authorization)
    data = load_data()
    
    # Filter notes for this user
    user_notes = [note for note in data["notes"] if note.get("user_email") == email]
    return sorted(user_notes, key=lambda x: x.get("created_at", ""), reverse=True)

@app.get("/api/notes/{note_id}")
def get_note(note_id: int, authorization: str = ""):
    """Get specific wine note"""
    email = get_user_email(authorization)
    data = load_data()
    
    for note in data["notes"]:
        if note.get("id") == note_id and note.get("user_email") == email:
            return note
    
    raise HTTPException(status_code=404, detail="Note not found")

@app.post("/api/notes")
def create_note(note: Dict[str, Any], authorization: str = ""):
    """Create new wine note"""
    email = get_user_email(authorization)
    data = load_data()
    
    # Generate new ID
    max_id = max([n.get("id", 0) for n in data["notes"]], default=0)
    new_id = max_id + 1
    
    note["id"] = new_id
    note["user_email"] = email
    note["created_at"] = datetime.now().isoformat()
    
    data["notes"].append(note)
    save_data(data)
    
    return note

@app.put("/api/notes/{note_id}")
def update_note(note_id: int, updated_note: Dict[str, Any], authorization: str = ""):
    """Update wine note"""
    email = get_user_email(authorization)
    data = load_data()
    
    for i, note in enumerate(data["notes"]):
        if note.get("id") == note_id and note.get("user_email") == email:
            updated_note["id"] = note_id
            updated_note["user_email"] = email
            updated_note["created_at"] = note.get("created_at")
            data["notes"][i] = updated_note
            save_data(data)
            return updated_note
    
    raise HTTPException(status_code=404, detail="Note not found")

@app.delete("/api/notes/{note_id}")
def delete_note(note_id: int, authorization: str = ""):
    """Delete wine note"""
    email = get_user_email(authorization)
    data = load_data()
    
    for i, note in enumerate(data["notes"]):
        if note.get("id") == note_id and note.get("user_email") == email:
            # Delete photos
            if note.get("photos"):
                for photo in note["photos"]:
                    photo_path = os.path.join(UPLOAD_DIR, photo)
                    if os.path.exists(photo_path):
                        try:
                            os.remove(photo_path)
                        except:
                            pass
            
            data["notes"].pop(i)
            save_data(data)
            return {"message": "Note deleted successfully"}
    
    raise HTTPException(status_code=404, detail="Note not found")

@app.post("/api/upload-photo/{note_id}")
async def upload_photo(note_id: int, file: UploadFile, authorization: str = ""):
    """Upload photo for wine note"""
    email = get_user_email(authorization)
    data = load_data()
    
    # Find note
    note_index = None
    for i, note in enumerate(data["notes"]):
        if note.get("id") == note_id and note.get("user_email") == email:
            note_index = i
            break
    
    if note_index is None:
        raise HTTPException(status_code=404, detail="Note not found")
    
    # Save file
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{email.replace('@', '_').replace('.', '_')}_{note_id}_{int(datetime.now().timestamp())}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Update note
    if not data["notes"][note_index].get("photos"):
        data["notes"][note_index]["photos"] = []
    
    data["notes"][note_index]["photos"].append(unique_filename)
    save_data(data)
    
    return {"filename": unique_filename, "url": f"/uploads/{unique_filename}"}

@app.delete("/api/delete-photo/{note_id}/{filename}")
def delete_photo(note_id: int, filename: str, authorization: str = ""):
    """Delete photo from wine note"""
    email = get_user_email(authorization)
    data = load_data()
    
    for i, note in enumerate(data["notes"]):
        if note.get("id") == note_id and note.get("user_email") == email:
            if note.get("photos") and filename in note["photos"]:
                note["photos"].remove(filename)
                
                # Delete file
                photo_path = os.path.join(UPLOAD_DIR, filename)
                if os.path.exists(photo_path):
                    try:
                        os.remove(photo_path)
                    except:
                        pass
                
                data["notes"][i] = note
                save_data(data)
                return {"message": "Photo deleted successfully"}
    
    raise HTTPException(status_code=404, detail="Photo not found")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
