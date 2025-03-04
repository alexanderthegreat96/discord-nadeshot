from typing import Callable, List, Optional, Any, Dict
from core.Cache import Cache
from core.Logger import Logger
from core.Config import Config


class QueueMessageProcessor:
    def __init__(self, logger: Logger):
        self.cache: Cache = Cache()
        self.config: Config = Config()
        self.logger: Logger = logger

    def __get_queue_name(self, queue_name_env_key: str) -> str:
        """
        Retrieve the queue name from the environment using the specified key.
        :param queue_name_env_key: The environment variable key for the queue name.
        :return: The queue name as a string.
        :raises ValueError: If the queue name is not found in the environment.
        """
        queue_name: Optional[str] = self.config.env().get(
            queue_name_env_key, "str", None
        )
        if not queue_name:
            raise ValueError(
                f"Could not find queue name: {queue_name_env_key} inside .env"
            )
        return queue_name

    def send_to_queue(
        self,
        queue_name_env_key: Optional[str] = None,
        item: Optional[str] = None,
        is_unique: bool = False,
        item_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Send an item to a Redis queue. Supports optional uniqueness constraints.

        :param queue_name_env_key: The environment variable key for the queue name.
                                If None, a default queue name must be managed by the implementation.
        :param item: The item to enqueue. Must be a string. Defaults to None.
        :param is_unique: Whether the item should be uniquely enqueued (no duplicates). Defaults to False.
        :param item_id: An optional identifier for the item when using unique enqueuing. Defaults to None.
        :return: A dictionary representing the result of the enqueue operation.
        :raises ValueError: If required parameters like `queue_name_env_key` or `item` are missing.
        """
        queue_name: str = self.__get_queue_name(queue_name_env_key)

        if not item:
            raise ValueError("The `item` parameter is required to enqueue data.")

        if is_unique:
            return self.cache.enqueue_item_unique(
                queue_name=queue_name, item=item, item_id=item_id
            )
        return self.cache.enqueue_item(queue_name=queue_name, item=item)

    def process_queue(
        self,
        queue_name_env_key: str,
        process_function: Callable[[Any], Optional[Any]],
        is_unique: bool = False,
    ) -> List[Any]:
        """
        Process the Redis queue by applying the provided processing function.
        :param queue_name_env_key: The environment variable key for the queue name.
        :param process_function: A callable that processes a single message.
                                 It should take the message as input and return a result.
                                 A falsy return value is considered a failed processing.
        :return: A list of results from successfully processed messages.
        """
        queue_name: str = self.__get_queue_name(queue_name_env_key)
        self.logger.info(f"Starting to process queue: {queue_name}")
        processed_results: List[Any] = []

        def handle_message(message: Any) -> None:
            try:
                if process_function is not None:
                    processed_results.append(process_function(message))
                else:
                    processed_results.append(message)
            except Exception as e:
                err: str = f"Error while processing message: {message}. Error: {e}"
                self.logger.error(err)
                return

        self.cache.process_queue(
            queue_name=queue_name, process_func=handle_message, is_unique=is_unique
        )
        return processed_results
