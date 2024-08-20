from typing import Annotated

from fastapi import HTTPException, APIRouter, Depends
from fastapi.params import Path
from sqlalchemy.orm import Session
from starlette import status

from src.app.database import get_db
from src.app.pessoa.models import Pessoa
from src.app.pessoa.schemas import PessoaRequest

router = APIRouter()


db_dependency = Annotated[Session, Depends(get_db)]


@router.get('/pessoas', status_code=status.HTTP_200_OK)
async def read_all_pessoa(db: db_dependency):
    return db.query(Pessoa).all()


@router.get('/pessoa/{pessoa_id}', status_code=status.HTTP_200_OK)
async def get_pessoa_by_id(db: db_dependency, pessoa_id: int = Path(gt=0)):
    pessoa = db.query(Pessoa).filter(pessoa_id == Pessoa.id).first()
    if pessoa is not None:
        return pessoa
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Pessoa not found')


@router.post('/pessoa', status_code=status.HTTP_201_CREATED)
async def create_pessoa(db: db_dependency, pessoa_request: PessoaRequest):
    pessoa = Pessoa(**pessoa_request.dict())
    db.add(pessoa)
    db.commit()
    db.refresh(pessoa)
    return {'message': 'Pessoa created successfully'}


@router.put('/pessoa/{pessoa_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_pessoa(db: db_dependency, pessoa_request: PessoaRequest, pessoa_id: int = Path(gt=0)):
    pessoa = db.query(Pessoa).filter(pessoa_id == Pessoa.id).first()
    if pessoa:
        for field, value in pessoa_request.dict(exclude_unset=True).items():
            setattr(pessoa, field, value)
        db.commit()
        db.refresh(pessoa)
        return {'message': 'Pessoa updated successfully'}
    else:
        return {'message': 'Pessoa not found'}


@router.delete('/pessoa/{pessoa_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_pessoa(db: db_dependency, pessoa_id: int = Path(gt=0)):
    pessoa = db.query(Pessoa).filter(pessoa_id == Pessoa.id).first()
    if pessoa is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail='Pessoa not found')

    db.delete(pessoa)
    db.commit()
    return {'message': 'Pessoa deleted successfully'}
