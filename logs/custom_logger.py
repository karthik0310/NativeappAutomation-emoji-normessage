import logging
import os
import sys

class Logger:
    @staticmethod
    def get_logger():
        """
        Configures and returns a logger instance with UTF-8 encoding.
        The log directory is dynamically generated based on the current working directory or an environment variable.
        """
        logger = logging.getLogger("CustomLogger")
        logger.setLevel(logging.INFO)

        # Prevent duplicate log handlers
        if not logger.handlers:
            # Determine the log directory dynamically
            base_dir = os.getenv("LOG_DIR", os.getcwd())  # Use LOG_DIR env variable if set, otherwise use current dir
            log_dir = os.path.join(base_dir, "logs")
            os.makedirs(log_dir, exist_ok=True)  # Ensure log directory exists

            # Log file path
            log_file_path = os.path.join(log_dir, "seconddevice.log")

            # File handler (UTF-8 encoding)
            file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
            file_handler.setLevel(logging.INFO)

            # Formatter for logs
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(formatter)

            # Stream handler (console output)
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(formatter)

            # Add handlers to logger
            logger.addHandler(file_handler)
            logger.addHandler(console_handler)

        return logger
