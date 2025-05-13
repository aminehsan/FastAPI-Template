from uuid import UUID
from sqlmodel import Session, select
from models.items import Item, ItemCreate, ItemUpdate


def create(owner_id: UUID, item: ItemCreate, session: Session):
    session.add(Item.model_validate(
        item,
        update={'owner_id': owner_id}
    ))
    session.commit()


def read_by_id(item_id: UUID, session: Session) -> Item | None:
    return session.get(Item, item_id)


def read(skip: int, limit: int, session: Session) -> list[Item]:
    return session.exec(
        statement=select(Item).offset(skip).limit(limit)
    ).all()


def update(db_item: Item, item: ItemUpdate, session: Session):
    db_item.sqlmodel_update(item.model_dump(exclude_unset=True))
    session.add(db_item)
    session.commit()


def delete(db_item: Item, session: Session):
    session.delete(db_item)
    session.commit()
