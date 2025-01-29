import logging
import os

class Logger:
    @staticmethod
    def get_logger():
        """
        Configures and returns a logger instance.
        """
        logger = logging.getLogger("CustomLogger")
        logger.setLevel(logging.INFO)

        # Prevent duplicate log handlers
        if not logger.handlers:
            # Ensure log directory exists
            log_dir = r"C:\Users\karthik\PycharmProjects\PythonProjectMyappiumseconddevice\logs"
            os.makedirs(log_dir, exist_ok=True)

            # File handler (with a valid file path)
            file_handler = logging.FileHandler(os.path.join(log_dir, "seconddevice.log"))
            file_handler.setLevel(logging.INFO)

            # Formatter for logs
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(formatter)

            # Stream handler (console output)
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)

            # Add handlers to logger
            logger.addHandler(file_handler)
            logger.addHandler(console_handler)

        return logger
