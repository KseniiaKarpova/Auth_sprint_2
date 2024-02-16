import uuid
from datetime import datetime

from sqlalchemy import ForeignKey, MetaData, String, Text, types, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from models.choices import SocialNetworksEnum


metadata = MetaData()


class Base(AsyncAttrs, DeclarativeBase):
    metadata = metadata
    is_active: Mapped[bool] = mapped_column(default=True)  # instead deleting change this field
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(onupdate=datetime.utcnow, nullable=True)


class User(Base):
    __tablename__ = 'users'

    uuid: Mapped[UUID] = mapped_column(types.Uuid,
                                       default=uuid.uuid4,
                                       primary_key=True)
    login: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=True)
    surname: Mapped[str] = mapped_column(String(255), nullable=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)
    user_roles: Mapped[list['UserRole']] = relationship(back_populates='user',
                                                 cascade='all, delete',
                                                 passive_deletes=True)

    user_history: Mapped[list['UserHistory']] = relationship(
        back_populates='user',
        cascade='all, delete',
        passive_deletes=True)

    social_accounts: Mapped[list["UserSocialAccount"]] = relationship(
        back_populates="user",
        cascade="all, delete",
        passive_deletes=True, )


class Role(Base):
    __tablename__ = 'roles'

    uuid: Mapped[UUID] = mapped_column(types.Uuid,
                                       default=uuid.uuid4,
                                       primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    user_roles: Mapped[list['UserRole']] = relationship(back_populates="role",
                                                  cascade="all, delete",
                                                  passive_deletes=True, )

    @staticmethod
    def get_colums():
        return ['uuid', 'name']


class UserRole(Base):
    __tablename__ = 'users_roles'

    uuid: Mapped[UUID] = mapped_column(types.Uuid,
                                       default=uuid.uuid4,
                                       primary_key=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey('users.uuid'),
                                          onupdate='CASCADE',
                                          nullable=False)
    role_id: Mapped[UUID] = mapped_column(ForeignKey('roles.uuid'),
                                          onupdate='CASCADE',
                                          nullable=False)
    user: Mapped['User'] = relationship(back_populates='user_roles')
    role: Mapped['Role'] = relationship(back_populates='user_roles')


class UserHistory(Base):
    __tablename__ = 'user_history'

    uuid: Mapped[UUID] = mapped_column(types.Uuid,
                                       default=uuid.uuid4,
                                       primary_key=True)

    user_id: Mapped[UUID] = mapped_column(ForeignKey('users.uuid'),
                                          onupdate='CASCADE',
                                          nullable=False)

    user_agent: Mapped[str] = mapped_column(String(255), nullable=True)
    refresh_token: Mapped[str] = mapped_column(Text(), nullable=True)
    user: Mapped['User'] = relationship(back_populates='user_history')


"""
After created a table make migration by:
 alembic revision --autogenerate -m 'Name of migration(Created User Table)'
"""
