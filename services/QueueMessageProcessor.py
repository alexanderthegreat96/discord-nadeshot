from typing import Callable, List, Optional, Any, Dict
from core.Cache import Cache
from core.Logger import Logger
from core.Config import Config


class QueueMessageProcessor:
    """
    QueueMessageProcessor handles sending and processing items in Redis queues
    with optional uniqueness enforcement and dynamic queue name resolution.

    WARNING:
        **Do NOT modify this class.**
        This is core infrastructure for queue-based message handling.
        Changing its behavior can lead to message loss, duplicate processing,
        or corrupted queue states.

        If customization is needed, extend functionality outside of this class
        using provided public methods or via safe wrappers.

    Features:
        - Dynamically resolves queue names from environment variables.
        - Supports unique item queuing to avoid duplicates.
        - Facilitates safe, logged message processing from queues.
    """

    def __init__(self, logger: Logger):
        """
        Initialize the QueueMessageProcessor with required dependencies.

        Args:
            logger (Logger): A Logger instance for event logging.
        """
        self.cache: Cache = Cache()
        self.config: Config = Config()
        self.logger: Logger = logger

    def __get_queue_name(self, queue_name_env_key: str) -> str:
        """
        Retrieve the queue name from the environment using the specified key.

        Args:
            queue_name_env_key (str): The environment variable key for the queue name.

        Returns:
            str: The queue name as a string.

        Raises:
            ValueError: If the queue name is not found in the environment.
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
        Send an item to a Redis queue, with optional uniqueness enforcement.

        Args:
            queue_name_env_key (Optional[str]): Environment variable key for the queue name.
            item (Optional[str]): The item to enqueue.
            is_unique (bool): Whether the item should be enqueued uniquely.
            item_id (Optional[str]): Identifier for uniqueness tracking.

        Returns:
            Dict[str, Any]: Result of the enqueue operation.

        Raises:
            ValueError: If required parameters like queue name or item are missing.
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
        Process a Redis queue by applying the provided processing function to each item.

        Args:
            queue_name_env_key (str): Environment variable key for the queue name.
            process_function (Callable[[Any], Optional[Any]]): Function to process each message.
            is_unique (bool): Whether to clear unique set tracking after processing.

        Returns:
            List[Any]: Results of successfully processed messages.
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

        self.cache.process_queue(
            queue_name=queue_name, process_func=handle_message, is_unique=is_unique
        )
        return processed_results
