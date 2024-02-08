# %%
from abc import ABC, abstractmethod

# Import all submodules to expose the public API
from .completion import OpenAIResource
from .orm import SQLAlchemyResource
from .postgres import PostgresResource


class BaseResource(ABC):
    """
    Base class for resources in the API.

    This class defines the common interface for interacting with resources.
    Subclasses should implement the abstract methods to provide specific functionality.

    Args:
        T: The type of the resource.

    Attributes:
        None
    """

    @abstractmethod
    def query(self, query, params=None):
        """
        Execute a query on the resource.

        Args:
            query: The query to execute.
            params: The parameters to pass to the query.

        Returns:
            The result of the query.

        Raises:
            NotImplementedError: If the method is not implemented by the subclass.
        """
        raise NotImplementedError

    @abstractmethod
    def get(self, entity_id):
        """
        Get a resource by its ID.

        Args:
            entity_id: The ID of the resource.

        Returns:
            The resource object.

        Raises:
            NotImplementedError: If the method is not implemented by the subclass.
        """
        raise NotImplementedError

    @abstractmethod
    def get_all(self):
        """
        Get all resources.

        Returns:
            A list of all resource objects.

        Raises:
            NotImplementedError: If the method is not implemented by the subclass.
        """
        raise NotImplementedError

    @abstractmethod
    def add(self, **kwargs: object) -> None:
        """
        Add a new resource.

        Args:
            **kwargs: Additional keyword arguments for creating the resource.

        Returns:
            None

        Raises:
            NotImplementedError: If the method is not implemented by the subclass.
        """
        raise NotImplementedError

    @abstractmethod
    def update(self, entity_id, **kwargs: object) -> None:
        """
        Update a resource.

        Args:
            entity_id: The ID of the resource to update.
            **kwargs: Additional keyword arguments for updating the resource.

        Returns:
            None

        Raises:
            NotImplementedError: If the method is not implemented by the subclass.
        """
        raise NotImplementedError

    @abstractmethod
    def delete(self, entity_id: int) -> None:
        """
        Delete a resource.

        Args:
            entity_id: The ID of the resource to delete.

        Returns:
            None

        Raises:
            NotImplementedError: If the method is not implemented by the subclass.
        """
        raise NotImplementedError

    @abstractmethod
    def remove(self, entity_id: int) -> None:
        """
        Remove a resource.

        Args:
            entity_id: The ID of the resource to remove.

        Returns:
            None

        Raises:
            NotImplementedError: If the method is not implemented by the subclass.
        """
        raise NotImplementedError


# %%
