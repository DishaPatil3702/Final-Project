from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import os
import logging

from app.routes import lead, auth

# =======================
# Load Environment Variables
# =======================
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY", "fallback_secret")

# =======================
# Logging Configuration
# =======================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# =======================
# FastAPI App Instance
# =======================
app = FastAPI(
    title="Advanced CRM System",
    version="0.1.0",
    description="A modern CRM backend powered by FastAPI and Supabase"
)

# =======================
# CORS Middleware
# =======================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =======================
# OAuth2 Security Scheme
# =======================
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# =======================
# Root Endpoint
# =======================
@app.get("/")
def read_root():
    return {"message": "Welcome to the CRM Backend!"}

# =======================
# Global Exception Middleware
# =======================
@app.middleware("http")
async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        logger.error(f"❌ Exception occurred: {e}", exc_info=True)
        return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})

# =======================
# Include API Routes
# =======================
app.include_router(auth.router)
app.include_router(lead.router)

# =======================
# Custom OpenAPI (Swagger Security)
# =======================
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    # Add JWT Bearer Auth
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }

    # Apply BearerAuth security to all endpoints except public ones
    public_paths = ["/", "/auth/signup", "/auth/login"]
    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            if path not in public_paths:
                openapi_schema["paths"][path][method]["security"] = [{"BearerAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema

# Attach the custom OpenAPI schema
app.openapi = custom_openapi
