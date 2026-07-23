import uuid
from datetime import datetime, date
from sqlalchemy import UUID
from sqlalchemy import Date
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from typing import Annotated

uuid_pk = Annotated[uuid.UUID, mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        default=uuid.uuid4,
    )]

created_at = Annotated[datetime, mapped_column(
    DateTime(timezone=True),
    default=func.now(), 
    nullable=False,

)]
updated_at = Annotated[datetime, mapped_column(
    DateTime(timezone=True),
    default=func.now(), 
    nullable=False,

)]

class BaseDBModel(DeclarativeBase):
    __tablename__: str
    __table_args__: dict[str, str] | tuple = {'schema': 'db_schema'}

    @classmethod
    def group_by_fields(cls, exclude: list[str] | None = None) -> list:
        payload = []
        if not exclude:
            exclude = []

        for column in cls.__table__.columns:
            if column.key in exclude:
                continue

            payload.append(column)

        return payload

class UserModel(BaseDBModel):
    __tablename__ = 'users'
    id: Mapped[uuid_pk]
    first_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    middle_name: Mapped[str] = mapped_column(
        String(255),
        nullable=True,
    )
    last_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    email: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
        unique=True,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

class PasswordsModel(BaseDBModel):
    __tablename__ = 'passwords'
    id: Mapped[uuid_pk]
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        ForeignKey("db_schema.users.id"),
        nullable=False,
        unique=True,

    )
    password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

class RolesModel(BaseDBModel):
    __tablename__ = 'roles'
    role: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        primary_key=True,
    )
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]


class UserRolesModel(BaseDBModel):
    __tablename__ = 'user_roles'
    id: Mapped[uuid_pk]
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        ForeignKey("db_schema.users.id"),
        nullable=False,

    )
    role: Mapped[str] = mapped_column(
        String(255),
        ForeignKey("db_schema.roles.role"),
        nullable=False,

    )
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

class ElementsModel(BaseDBModel):
    __tablename__ = 'elements'
    element: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        primary_key=True,
    )
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

class RoleElementsModel(BaseDBModel):
    __tablename__ = 'role_elements'
    id: Mapped[uuid_pk]
    element: Mapped[str] = mapped_column(
        String(255),
        ForeignKey("db_schema.elements.element"),
        nullable=False,

    )
    role: Mapped[str] = mapped_column(
        String(255),
        ForeignKey("db_schema.roles.role"),
        nullable=False,

    )
    create: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )
    update: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )
    get: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )
    get_all: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )
    delete: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
