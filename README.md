# worm-cdc-s3-backup-service
## S3 File Watcher

This Python script monitors specified local folders for file changes and uploads the modified or newly created files to an Amazon S3 bucket.

### Prerequisites

Make sure you have the following installed:

- Python
- pip (Python package installer)

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/s3-file-watcher.git
    cd s3-file-watcher
    ```

2. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

### Configuration

1. Create a `.env` file in the root directory with the following variables:

    ```env
    FOLDER_PATHS=/path/to/folder1,/path/to/folder2
    AWS_ACCESS_KEY_ID=your_access_key_id
    AWS_SECRET_ACCESS_KEY=your_secret_access_key
    S3_BUCKET_NAME=your_s3_bucket_name
    HISTORICAL_DATA=True
    ```

    Adjust the values accordingly.

2. Run the script:

    ```bash
    python s3_file_watcher.py
    ```

### Docker Compose

To run the script using Docker Compose, create a `docker-compose.yml` file with the following content:

```yaml
version: '3'
services:
  s3-file-watcher:
    image: python:3.9
    volumes:
      - /path/to/s3-file-watcher:/app
    environment:
      - FOLDER_PATHS=/app
      - AWS_ACCESS_KEY_ID=your_access_key_id
      - AWS_SECRET_ACCESS_KEY=your_secret_access_key
      - S3_BUCKET_NAME=your_s3_bucket_name
      - HISTORICAL_DATA=True
    command: python /app/s3_file_watcher.py
```

Adjust the volume path and environment variables accordingly. Then run:

```bash
docker-compose up -d
```

This will start the script in a Docker container.

### Notes

- Ensure that the AWS credentials provided have the necessary permissions to read and write to the specified S3 bucket.

- The `HISTORICAL_DATA` variable determines whether existing files in the local folders should be uploaded to S3 when the script starts.

- Hidden files (those starting with a dot `.`) are skipped during file monitoring and uploading.

- The script logs events and errors to the console.

Feel free to customize the script and configurations based on your specific use case.
