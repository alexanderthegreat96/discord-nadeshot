class TaskSample:
    def __init__(self, bot, logger):
        self.bot = bot
        self.logger = logger

    async def main(self):
        self.logger.info("Task: TaskSample has started...")
        raise Exception("Something went wrong!")


# import math

# class TaskSample:
#     def __init__(self, bot, logger):
#         self.bot = bot
#         self.logger = logger

#     def is_prime(self, n):
#         """Helper method to check if a number is prime."""
#         if n <= 1:
#             return False
#         if n == 2:
#             return True
#         if n % 2 == 0:
#             return False
#         for i in range(3, int(math.sqrt(n)) + 1, 2):
#             if n % i == 0:
#                 return False
#         return True

#     def cpu_intensive_task(self):
#         """A CPU-intensive task for performance testing. Calculates the sum of primes up to a large number."""
#         limit = 10**6  # Limit to generate primes up to 1,000,000
#         prime_sum = sum(n for n in range(limit) if self.is_prime(n))
#         return prime_sum

#     async def main(self):
#         """Main task execution."""
#         self.logger.info("Task: TaskSample has started...")

#         # Run CPU-intensive task directly since it's already running in a separate thread
#         result = self.cpu_intensive_task()

#         self.logger.info(f"Task: TaskSample has completed. Result of prime sum: {result}")
