from core.Logger import Logger
from redis import Redis, ConnectionError
from from_root import from_root
from core.EnvParser import EnvParser
import time

# Set up logging
logging = Logger("Redis-Cache").get_logger()


class Cache:
    """
    Cache handles Redis-based caching, queue management, and data persistence.

    WARNING:
        This class provides core caching infrastructure for the application.
        **Do NOT modify this class unless you know exactly what you're doing.**
        Changes here can impact data consistency, queue processing, or break Redis connections.

        If you need additional caching behavior, consider extending this class
        or interacting with it through its public methods.
    """

    def __init__(self, global_cache_key: str = None):
        """
        Initializes the Cache instance, sets up Redis connection and global cache key.

        Args:
            global_cache_key (str, optional): Custom global cache key prefix. Defaults to value from .env.
        """
        env = EnvParser(from_root(".env"))
        self.__host: str = env.get(which="REDIS_HOST", default="nadeshot-redis")
        self.__port: int = env.get(which="REDIS_PORT", default=6379)
        self.__password: str = env.get(which="REDIS_PASS", default="nadeshot-redis")
        self.__cache_key: str = env.get(
            which="REDIS_GLOBAL_CACHE_KEY", default="nadeshot-bot"
        )

        if not global_cache_key:
            self.__global_cache_key: str = f"{self.__cache_key}:"
        else:
            self.__global_cache_key: str = f"{global_cache_key}:" or "test-cache-key"

        self.__redis = self.connect()

    def connect(self, timeout: int = 1) -> Redis:
        """
        Connect to Redis and return the client instance.

        Args:
            timeout (int): Timeout for the Redis socket connection in seconds.

        Returns:
            Redis: Redis client instance.
        """
        try:
            return Redis(
                host=self.__host,
                port=self.__port,
                password=self.__password,
                db=0,
                socket_timeout=timeout,
            )
        except Exception as e:
            logging.error(f"Failed to connect to Redis: {e}")
            raise

    def reconnect(self, retries: int = 3, delay: int = 2) -> Redis:
        """
        Attempt to reconnect to Redis with retries and delays.

        Args:
            retries (int): Number of retry attempts.
            delay (int): Delay between attempts in seconds.

        Returns:
            Redis: Redis client instance after successful reconnection.
        """
        for attempt in range(1, retries + 1):
            try:
                logging.info(
                    f"Attempting to reconnect to Redis (attempt {attempt}/{retries})..."
                )
                return self.connect()
            except ConnectionError as e:
                logging.error(f"Reconnect attempt {attempt} failed: {e}")
                if attempt < retries:
                    time.sleep(delay)
                else:
                    logging.error(
                        f"Failed to reconnect to Redis after {retries} attempts."
                    )
                    raise
        return None

    def _execute_with_reconnect(self, func, *args, retries=3, **kwargs):
        """
        Helper method to execute a Redis operation with automatic reconnection on failure.

        Args:
            func: The Redis operation function to execute.
            *args: Positional arguments for the function.
            retries (int): Number of retry attempts.
            **kwargs: Keyword arguments for the function.

        Returns:
            The result of the Redis operation.
        """
        for attempt in range(1, retries + 1):
            try:
                return func(*args, **kwargs)
            except ConnectionError as e:
                logging.error(f"Redis connection failed during operation: {e}")
                if attempt < retries:
                    logging.info(
                        f"Attempting to reconnect and retry operation (attempt {attempt}/{retries})..."
                    )
                    self.__redis = self.reconnect()
                else:
                    logging.error("Max retries reached. Failing operation.")
                    raise

    def get_data(self, key: str, expiration_in_seconds: int = 60) -> dict:
        """
        Retrieve cached data from Redis.

        Args:
            key (str): The key to retrieve data for.
            expiration_in_seconds (int): Expiration for caching logic context.

        Returns:
            dict: Result status, key, data or error.
        """
        if not key:
            return {"status": False, "error": "No cache key provided."}

        try:
            full_key = self.__global_cache_key + key

            def _get_data():
                cached_data = self.__redis.get(full_key)
                if cached_data:
                    return {
                        "status": True,
                        "key": full_key,
                        "expirationInSeconds": expiration_in_seconds,
                        "data": cached_data,
                    }
                else:
                    return {
                        "status": False,
                        "key": full_key,
                        "expirationInSeconds": expiration_in_seconds,
                        "error": "No data cached for the provided key.",
                    }

            return self._execute_with_reconnect(_get_data)
        except Exception as e:
            return {"status": False, "error": f"Something happened: {e}"}

    def set_data(self, key: str, data: str, expiration_in_seconds: int = 60) -> dict:
        """
        Set data in Redis cache with an expiration.

        Args:
            key (str): Cache key.
            data (str): Data to store.
            expiration_in_seconds (int): Expiration time.

        Returns:
            dict: Result status, key, and data confirmation or error.
        """
        if not key:
            return {"status": False, "error": "No cache key provided."}
        try:
            full_key = self.__global_cache_key + key

            def _set_data():
                self.__redis.set(full_key, data, ex=expiration_in_seconds)
                return {
                    "status": True,
                    "key": full_key,
                    "expirationInSeconds": expiration_in_seconds,
                    "data": data,
                }

            return self._execute_with_reconnect(_set_data)
        except Exception as e:
            return {"status": False, "error": f"Something happened: {e}"}

    def reset_data(self, key: str) -> dict:
        """
        Delete a specific cached key.

        Args:
            key (str): Cache key to delete.

        Returns:
            dict: Result status or error.
        """
        if not key:
            return {"status": False, "error": "No cache key provided."}

        try:
            full_key = f"{self.__global_cache_key}{key}"
            existing_data = self.get_data(key)

            if existing_data["status"]:

                def _reset_data():
                    self.__redis.delete(full_key)
                    return {"status": True}

                return self._execute_with_reconnect(_reset_data)
            else:
                return {"status": False, "error": existing_data["error"]}
        except Exception as e:
            return {"status": False, "error": f"Something happened: {e}"}

    def enqueue_item(self, queue_name: str, item: str) -> dict:
        """
        Enqueue an item into a Redis list (queue).

        Args:
            queue_name (str): Name of the queue.
            item (str): Item to enqueue.

        Returns:
            dict: Result status or error.
        """
        try:
            full_queue_name = self.__global_cache_key + queue_name

            def _enqueue_item():
                self.__redis.lpush(full_queue_name, item)
                return {"status": True, "queue": full_queue_name, "item": item}

            return self._execute_with_reconnect(_enqueue_item)
        except Exception as e:
            return {"status": False, "error": f"Error enqueuing item: {e}"}

    def enqueue_item_unique(self, queue_name: str, item: str, item_id: str) -> dict:
        """
        Enqueue an item into a Redis queue while ensuring uniqueness.

        Args:
            queue_name (str): Queue name.
            item (str): Item to enqueue.
            item_id (str): Unique ID for item tracking.

        Returns:
            dict: Result status or error.
        """
        try:
            full_queue_name = self.__global_cache_key + queue_name
            unique_set_name = full_queue_name + "_set"

            def _enqueue_item():
                if not self.__redis.sismember(unique_set_name, item_id):
                    self.__redis.lpush(full_queue_name, item)
                    self.__redis.sadd(unique_set_name, item_id)
                    return {"status": True, "queue": full_queue_name, "item": item}
                else:
                    return {"status": False, "error": "Duplicate item not added."}

            return self._execute_with_reconnect(_enqueue_item)
        except Exception as e:
            return {"status": False, "error": f"Error enqueuing item: {e}"}

    def dequeue_item(self, queue_name: str, timeout: int = 0) -> dict:
        """
        Dequeue an item from the Redis queue.

        Args:
            queue_name (str): Queue name.
            timeout (int): Timeout for blocking pop.

        Returns:
            dict: Result status and dequeued item or error.
        """
        try:
            full_queue_name = self.__global_cache_key + queue_name

            def _dequeue_item():
                item = self.__redis.brpop(full_queue_name, timeout=timeout)
                if item:
                    return {
                        "status": True,
                        "queue": full_queue_name,
                        "item": item[1].decode("utf-8"),
                    }
                else:
                    return {
                        "status": False,
                        "queue": full_queue_name,
                        "message": "Queue is empty or timeout reached.",
                    }

            return self._execute_with_reconnect(_dequeue_item)
        except Exception as e:
            return {"status": False, "error": f"Error dequeuing item: {e}"}

    def process_queue(
        self, queue_name: str, process_func, is_unique: bool = False, timeout: int = 0
    ):
        """
        Continuously process items from a Redis queue using the given processing function.

        Args:
            queue_name (str): Name of the queue.
            process_func: Function to process each dequeued item.
            is_unique (bool): Whether to clear the unique set after processing.
            timeout (int): Timeout for dequeue operation.
        """
        full_queue_name = self.__global_cache_key + queue_name
        unique_set_name = full_queue_name + "_set"

        while True:
            item = self.dequeue_item(queue_name, timeout)
            if item["status"]:
                try:
                    process_func(item["item"])
                    logging.info(f"Processed item: {item['item']}")
                except Exception as e:
                    logging.error(f"Error processing item {item['item']}: {e}")
            else:
                logging.info(f"Queue {full_queue_name} is empty or timeout reached.")
                break

        if is_unique:
            try:

                def _clear_set():
                    if self.__redis.type(unique_set_name) == b"set":
                        self.__redis.delete(unique_set_name)
                        return {
                            "status": True,
                            "message": f"Unique set '{unique_set_name}' cleared.",
                        }
                    else:
                        return {
                            "status": False,
                            "error": f"Set: {unique_set_name} was not found.",
                        }

                clear_result = self._execute_with_reconnect(_clear_set)
                if clear_result["status"]:
                    logging.info(clear_result["message"])
                else:
                    logging.warning(clear_result["error"])
            except Exception as e:
                logging.error(f"Failed to clear unique set '{unique_set_name}': {e}")

    def clear_cache(self, prefix: str = None) -> dict:
        """
        Clear all Redis cache keys that match a given prefix.

        Args:
            prefix (str, optional): Prefix for keys to delete.

        Returns:
            dict: Result status and message or error.
        """
        if prefix is None:
            prefix = self.__global_cache_key
        else:
            prefix = f"{self.__global_cache_key}{prefix}"

        try:
            if not prefix.endswith(":"):
                prefix += ":"

            def _clear_keys():
                cursor = 0
                deleted_keys_count = 0

                while True:
                    cursor, keys = self.__redis.scan(cursor=cursor, match=f"{prefix}*")
                    if keys:
                        self.__redis.delete(*keys)
                        deleted_keys_count += len(keys)

                    if cursor == 0:
                        break

                return {
                    "status": True,
                    "message": f"Cleared {deleted_keys_count} keys with prefix '{prefix}'.",
                }

            return self._execute_with_reconnect(_clear_keys)
        except Exception as e:
            logging.error(f"Failed to clear cache with prefix '{prefix}': {e}")
            return {"status": False, "error": f"Failed to clear cache: {e}"}
