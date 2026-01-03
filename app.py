from fastapi import FastAPI
from routers import webhook
from models.database import init_db

app = FastAPI()
app.include_router(webhook.router)

@app.on_event("startup")
def startup_event():
    init_db()

if __name__ == "__main__":
    import uvicorn
    from config.settings import settings
    uvicorn.run("app:app", host=settings.HOST, port=settings.PORT, reload=True)