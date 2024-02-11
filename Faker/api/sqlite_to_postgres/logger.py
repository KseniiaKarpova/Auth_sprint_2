import logging

# Set up logging
log_file = 'sqlite_to_postgres.log'
max_file_size = 1024 * 1024  # 1 MB
backup_count = 5

# Create a named logger for your application
logger = logging.getLogger('sqlite_to_postgres')
logger.setLevel(logging.INFO)

# Configure the file handler with log rotation
ch = logging.StreamHandler()
ch.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
ch.setLevel(logging.INFO)
logger.addHandler(ch)
