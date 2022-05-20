from fastapi import FastAPI

from controllers import user, item, chat, auth, websockets
from repository.database.async_postgres import database
from repository.database.redis import connection

app = FastAPI(version="1")
app.include_router(user.router)
app.include_router(item.router)
app.include_router(chat.router)
app.include_router(auth.router)
app.add_api_websocket_route("/ws", websockets.websocket_connection)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await connection.close()
    await database.disconnect()
