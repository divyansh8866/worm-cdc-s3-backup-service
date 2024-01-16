try:
    import boto3
    import os
    import time
    import logging
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    from dotenv import load_dotenv
except Exception as e:
    print(f"Error While Importing Library : {e}")
# Load environment variables from .env file
load_dotenv()

# AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
# AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']

# S3_BUCKET_NAME = os.environ['S3_BUCKET_NAME']
# FOLDER_PATHS = os.environ['FOLDER_PATHS']
HISTORICAL_DATA = os.environ['HISTORICAL_DATA']

FOLDER_PATHS = os.getenv("FOLDER_PATHS").split(',')
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
HISTORICAL_DATA = os.getenv("HISTORICAL_DATA")
AWS_SESSION_TOKEN = ''
root_dir = ""


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Watcher:
    def __init__(self, folder_paths):
        self.observer = Observer()
        self.folder_paths = folder_paths

    def run(self):
        for folder_path in self.folder_paths:
            global root_dir
            root_dir = folder_path
            logger.info(f"S3 Bucket Name : {S3_BUCKET_NAME}")
            # Upload existing files first
            if HISTORICAL_DATA == 'True':
                self.upload_existing_files(folder_path)
            else :
                logger.info(f"Skipping Historical Data Backup")
            logger.info(f"Watching {folder_path}...")

            event_handler = Handler(folder_path)
            self.observer.schedule(event_handler, path=folder_path, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            logger.error("Error")
        self.observer.join()

    def upload_existing_files(self, folder_path):
        for root, _, files in os.walk(folder_path):
            for file in files:
                if not file.startswith('.'):
                    file_path = os.path.join(root, file)
                    logger.info(f"Uploading existing file - {file_path}.")
                    upload_to_s3(file_path)
                else:
                    logger.info(f"Skipping Hidden file : {file}")
        logger.info(f"Historical Data Backup Complete")
        

class Handler(FileSystemEventHandler):
    def __init__(self, folder_path):
        self.folder_path = folder_path

    def on_any_event(self, event):
        if event.is_directory:
            return None

        file_name = os.path.basename(event.src_path)

        if not file_name.startswith('.'):
            if event.event_type == 'created':
                logger.info(f"Received created event - {event.src_path}.")
                upload_to_s3(event.src_path)

            elif event.event_type == 'modified':
                logger.info(f"Received modified event - {event.src_path}.")
                upload_to_s3(event.src_path)
        else:
            logger.info(f"Skipping Hidden file : {file_name}")

def upload_to_s3(file_path):
    try: 
        s3 = boto3.client('s3')
        object_name = file_path
        root_folder = f'{root_dir}/'
        object_name = object_name.replace(root_folder, '')
        s3.upload_file(file_path, S3_BUCKET_NAME, object_name)
        logger.info(f"Uploaded {file_path} to S3.")
    except Exception as e:
        logger.error(f"Error uploading {object_name} to S3: {e}")

if __name__ == '__main__':
    if not FOLDER_PATHS:
        logger.error('Please set the FOLDER_PATHS variable.')
    elif not AWS_ACCESS_KEY_ID:
        logger.error('Please set the AWS_ACCESS_KEY_ID variable.')
    elif not AWS_SECRET_ACCESS_KEY:
        logger.error('Please set the AWS_SECRET_ACCESS_KEY variable.')
    else:
        if AWS_SESSION_TOKEN:
            boto3.setup_default_session(
                aws_access_key_id=AWS_ACCESS_KEY_ID,
                aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                aws_session_token=AWS_SESSION_TOKEN
            )
        else:
            boto3.setup_default_session(
                aws_access_key_id=AWS_ACCESS_KEY_ID,
                aws_secret_access_key=AWS_SECRET_ACCESS_KEY
            )

        watcher = Watcher(FOLDER_PATHS)
        watcher.run()
