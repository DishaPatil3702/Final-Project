from fastapi import APIRouter, HTTPException, Form, Header, Depends
from fastapi.security import OAuth2PasswordBearer
from app.services.supabase_client import supabase
from app.utils.jwt_handler import create_access_token, verify_token
import bcrypt

router = APIRouter(prefix="/auth", tags=["Authentication"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

@router.post("/signup")
def signup(email: str = Form(...), password: str = Form(...)):
    try:
        existing_user = supabase.table("users").select("*").eq("email", email).execute()
        if existing_user.data:
            raise HTTPException(status_code=400, detail="User already exists")

        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        result = supabase.table("users").insert({
            "email": email,
            "password": hashed_password.decode("utf-8")
        }).execute()

        if not result.data:
            raise HTTPException(status_code=400, detail="Failed to create user")

        return {"message": "User registered successfully"}

    except Exception as e:
        print("❌ Signup Error:", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/login")
def login(email: str = Form(...), password: str = Form(...)):
    try:
        user = supabase.table("users").select("*").eq("email", email).execute()
        if not user.data:
            raise HTTPException(status_code=400, detail="Invalid email or password")

        user_data = user.data[0]
        if not bcrypt.checkpw(password.encode("utf-8"), user_data["password"].encode("utf-8")):
            raise HTTPException(status_code=400, detail="Invalid email or password")

        token = create_access_token({"sub": user_data["email"]})
        return {"access_token": token, "token_type": "bearer"}

    except Exception as e:
        print("❌ Login Error:", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/me")
def get_me(authorization: str = Header(...)):
    try:
        parts = authorization.replace("Bearer", "").strip().split()
        if not parts:
            raise HTTPException(status_code=401, detail="Invalid or missing token")

        token = parts[0]

        payload = verify_token(token)
        if payload is None:
            raise HTTPException(status_code=401, detail="Invalid or expired token")

        return {"email": payload.get("sub")}

    except Exception as e:
        print("❌ Token Error:", e)
        raise HTTPException(status_code=401, detail="Invalid or missing token")


# ✅ Function for dependency injection in other routes
def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return {"email": payload.get("sub")}
