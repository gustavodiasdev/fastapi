from fastapi import FastAPI

from src.app.database import engine
from src.app.pessoa import pessoa, models

app = FastAPI()


models.Base.metadata.create_all(bind=engine)
app.include_router(pessoa.router)



@app.get('/')
async def welcome():
    return {'message': 'Welcome to our pessoa-api'}
