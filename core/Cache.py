import logging
from redis import Redis, ConnectionError
from from_root import from_root
from core.EnvParser import EnvParser
import time

# Set up logging
logging.basicConfig(level=logging.INFO)


class Cache:
    def __init__(self, global_cache_key: str = None):
        # Parse environment variables
        env = EnvParser(from_root(".env"))
        self.__host: str = env.get(which="REDIS_HOST", default="isac-api-redis")
        self.__port: int = env.get(which="REDIS_PORT", default=6379)
        self.__password: str = env.get(which="REDIS_PASS", default="isac-api-redis")
        self.__cache_key: str = env.get(which="REDIS_GLOBAL_CACHE_KEY", default=None)

        # Set global cache key
        self.__global_cache_key: str = None
        if not self.__cache_key:
            self.__global_cache_key = (
                global_cache_key + ":" if global_cache_key else None
            )
        else:
            self.__global_cache_key = self.__cache_key + ":"

        # Establish Redis connection
        self.__redis = self.connect()

    def connect(self, timeout: int = 1) -> Redis:
        """Connect to Redis and return the client instance."""
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
        """Try to reconnect to Redis with retries and delays."""
        for attempt in range(1, retries + 1):
            try:
                logging.info(
                    f"Attempting to reconnect to Redis (attempt {attempt}/{retries})..."
                )
                return self.connect()
            except ConnectionError as e:
                logging.error(f"Reconnect attempt {attempt} failed: {e}")
                if attempt < retries:
                    time.sleep(delay)  # Wait before retrying
                else:
                    logging.error(
                        f"Failed to reconnect to Redis after {retries} attempts."
                    )
                    raise
        return None

    def _execute_with_reconnect(self, func, *args, retries=3, **kwargs):
        """Helper function to handle reconnection and re-execution of Redis operations."""
        for attempt in range(1, retries + 1):
            try:
                # Try to execute the function
                return func(*args, **kwargs)
            except ConnectionError as e:
                logging.error(f"Redis connection failed during operation: {e}")
                if attempt < retries:
                    # Try to reconnect and re-execute the function
                    logging.info(
                        f"Attempting to reconnect and retry operation (attempt {attempt}/{retries})..."
                    )
                    self.__redis = self.reconnect()  # Reconnect Redis
                else:
                    logging.error("Max retries reached. Failing operation.")
                    raise

    def get_data(self, key: str, expiration_in_seconds: int = 60) -> dict:
        """Get data from Redis for a specific key."""
        if not key:
            return {"status": False, "error": "No cache key provided."}

        try:
            full_key = self.__global_cache_key + key

            def _get_data():
                """Inner function to retrieve data from Redis."""
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
        """Set data in Redis with a specific key and expiration time."""
        if not key:
            return {"status": False, "error": "No cache key provided."}
        try:
            full_key = self.__global_cache_key + key

            def _set_data():
                """Inner function to set data in Redis."""
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
        """Delete cached data for a specific key."""
        if not key:
            return {"status": False, "error": "No cache key provided."}

        try:
            full_key = self.__global_cache_key + key
            existing_data = self.get_data(key)

            if existing_data["status"]:

                def _reset_data():
                    """Inner function to delete data in Redis."""
                    self.__redis.delete(full_key)
                    return {"status": True}

                return self._execute_with_reconnect(_reset_data)
            else:
                return {"status": False, "error": existing_data["error"]}
        except Exception as e:
            return {"status": False, "error": f"Something happened: {e}"}

    def enqueue_item(self, queue_name: str, item: str) -> dict:
        """Enqueue a generic item into the Redis queue (List)."""
        try:
            full_queue_name = self.__global_cache_key + queue_name

            def _enqueue_item():
                """Inner function to enqueue the item into the Redis queue."""
                self.__redis.lpush(full_queue_name, item)
                return {"status": True, "queue": full_queue_name, "item": item}

            return self._execute_with_reconnect(_enqueue_item)
        except Exception as e:
            return {"status": False, "error": f"Error enqueuing item: {e}"}

    def enqueue_item_unique(self, queue_name: str, item: str, item_id: str) -> dict:
        """Enqueue a generic item into the Redis queue (List) while preventing duplicates."""
        try:
            full_queue_name = self.__global_cache_key + queue_name
            unique_set_name = full_queue_name + "_set"

            def _enqueue_item():
                """Inner function to enqueue the item into the Redis queue."""
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
        """Dequeue a generic item from the Redis queue (List)."""
        try:
            full_queue_name = self.__global_cache_key + queue_name

            def _dequeue_item():
                """Inner function to dequeue the item from the Redis queue."""
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

    def process_queue(self, queue_name: str, process_func, timeout: int = 0):
        """Continuously dequeue items and process them using the provided function."""
        full_queue_name = self.__global_cache_key + queue_name
        while True:
            item = self.dequeue_item(queue_name, timeout)
            if item["status"]:
                process_func(item["item"])
            else:
                logging.info(f"Queue {full_queue_name} is empty or timeout reached.")
                break
