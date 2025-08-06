from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import traceback

app = FastAPI(title="Advanced CRM System")

# Enable CORS (optional)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 👇 This catches and prints ALL internal exceptions
@app.middleware("http")
async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        logging.error(f"❌ Exception occurred: {e}")
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={"detail": f"Internal Server Error: {str(e)}"},
        )

# Import your routes
from app.routes import lead
app.include_router(lead.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Advanced CRM API"}
