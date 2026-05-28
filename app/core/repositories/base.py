from typing import Any, Generic, TypeVar

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """
    Generic base repository that provides common database operations
    for any SQLAlchemy model. Extend this class and set the model type
    to get CRUD and query helpers for free.
    """

    def __init__(self, session: AsyncSession, model: type[ModelType]) -> None:
        self.session = session
        self.model = model

    # ------------------------------------------------------------------
    # Write operations
    # ------------------------------------------------------------------

    async def create(self, data: dict[str, Any]) -> ModelType:
        """
        Insert a new row and return the hydrated instance.

        :param data: Column values as a dictionary.
        :return: Created model instance.
        """
        instance = self.model(**data)
        self.session.add(instance)
        await self.session.flush()
        await self.session.refresh(instance)
        return instance

    async def delete(self, instance: ModelType) -> None:
        """
        Delete a model instance from the database.

        :param instance: Model instance to delete.
        """
        await self.session.delete(instance)
        await self.session.flush()

    # ------------------------------------------------------------------
    # Read operations
    # ------------------------------------------------------------------

    async def get_by_id(self, id: int) -> ModelType | None:
        """
        Fetch a row by its primary key.

        :param id: Primary key value.
        :return: Model instance or None.
        """
        return await self.session.get(self.model, id)

    async def _query(self, join_: set[str] | None = None) -> Select:
        """
        Build a SELECT query for this model, optionally applying
        eager-load JOINs.

        Each name in *join_* maps to a ``_join_<name>`` method on the
        subclass.  For example ``join_={"journal_entries"}`` will call
        ``self._join_journal_entries(query)``.

        :param join_: Set of relationship names to eager-load.
        :return: SQLAlchemy Select object.
        """
        query: Select = select(self.model)

        if join_ is not None:
            for join_name in join_:
                join_method = getattr(self, f"_join_{join_name}", None)
                if join_method is not None:
                    query = join_method(query)

        return query

    async def _one_or_none(self, query: Select) -> ModelType | None:
        """
        Execute *query* and return a single result or None.

        :param query: SELECT query to execute.
        :return: Model instance or None.
        """
        result = await self.session.execute(query)
        return result.scalars().one_or_none()

    async def all_unique(self, query: Select) -> list[ModelType]:
        """
        Execute *query* and return all unique results.

        Use this instead of ``_one_or_none`` when the query contains a
        JOIN that may produce duplicate rows.

        :param query: SELECT query to execute.
        :return: Deduplicated list of model instances.
        """
        result = await self.session.execute(query)
        return list(result.unique().scalars().all())
