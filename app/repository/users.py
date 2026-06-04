from sqlalchemy import Select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.core.repositories import BaseRepository


class UserRepository(BaseRepository[User]):
    """
    User repository provides all the database operations for the User model.
    """

    

    async def get_by_username(
        self, username: str, join_: set[str] | None = None
    ) -> User | list[User] | None:
        """
        Get user by username.

        :param username: Username.
        :param join_: Set of relationship names to eager-load.
        :return: User instance, list of Users (when joining), or None.
        """
        query = await self._query(join_)
        query = query.filter(User.username == username)

        if join_ is not None:
            return await self.all_unique(query)

        return await self._one_or_none(query)

    async def get_by_email(
        self, email: str, join_: set[str] | None = None
    ) -> User | list[User] | None:
        """
        Get user by email.

        :param email: Email address.
        :param join_: Set of relationship names to eager-load.
        :return: User instance, list of Users (when joining), or None.
        """
        query = await self._query(join_)
        query = query.filter(User.email == email)

        if join_ is not None:
            return await self.all_unique(query)

        return await self._one_or_none(query)

    def _join_journal_entries(self, query: Select) -> Select:
        """
        Eager-load the ``journal_entries`` relationship via a JOIN.

        Called automatically by ``_query`` when ``join_={"journal_entries"}``
        is passed.  The ``contains_joined_collection`` option tells
        SQLAlchemy to deduplicate rows produced by the JOIN.

        :param query: Base SELECT query.
        :return: Query with joinedload applied.
        """
        return query.options(joinedload(User.journal_entries)).execution_options(
            contains_joined_collection=True
        )
