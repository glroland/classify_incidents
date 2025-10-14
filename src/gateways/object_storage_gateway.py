""" Service Gateway for accessing S3/Object Storage. """
import logging
from pathlib import Path
import boto3
from utils.settings import settings

logger = logging.getLogger(__name__)

class ObjectStorageGateway():
    """ Service Gateway for Object Storage """

    # object storage client info
    s3_client = None
    bucket_name : str = None

    def __init__(self):
        """ Default Constructor """
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id = settings.OBJECT_STORAGE_ACCESS_KEY,
            aws_secret_access_key = settings.OBJECT_STORAGE_SECRET_KEY,
            endpoint_url = settings.OBJECT_STORAGE_URL,
            #verify = False,
            config = boto3.session.Config(signature_version='s3v4')   # For MinIO compatibility
        )
        self.bucket_name = settings.OBJECT_STORAGE_BUCKET

    def list(self):
        """ List the files in a bucket.
        
            bucket_name - bucket name
        """
        # validate bucket name
        if self.bucket_name is None or len(self.bucket_name) == 0:
            msg = "Bucket Name is required but is empty!"
            logger.error(msg)
            raise ValueError(msg)

        # invoke list objects api
        response = self.s3_client.list_objects_v2(Bucket=self.bucket_name)

        object_list = []

        # save object list to a clean array
        if "Contents" in response:
            for obj in response["Contents"]:
                object_list.append(obj['Key'])

        logger.debug("List of Objects in folder: %s", object_list)
        return object_list

    def upload(self, key : str, contents : str):
        """ Upload a new file to the bucket. """
        # validate input parameters
        if key is None or len(key) == 0:
            msg = "Key is required but is empty!"
            logger.error(msg)
            raise ValueError(msg)
        if contents is None or len(contents) == 0:
            contents = ""

        # upload the data
        logger.info("Uploading contents to bucket.  Key=%s", key)
        self.s3_client.put_object(Bucket=self.bucket_name,
                                  Key=key,
                                  Body=contents)

    def download(self, key : str) -> str:
        """ Downloads a file from the bucket.
        
            key - name of file
        """
        # validate input parameters
        if key is None or len(key) == 0:
            msg = "Key is required but is empty!"
            logger.error(msg)
            raise ValueError(msg)

        # download the file
        logger.info("Downloading file from bucket.  Key=%s", key)
        response = self.s3_client.get_object(Bucket=self.bucket_name, Key=key)
        contents = response['Body'].read().decode('utf-8')

        logger.debug("File contents.  Key=%s Contents=%s", key, contents)
        return contents

    def delete(self, key : str):
        """ Deletes the specified file from the bucket.
        
            key - name of file to delete
        """
        # validate input parameters
        if key is None or len(key) == 0:
            msg = "Key is required but is empty!"
            logger.error(msg)
            raise ValueError(msg)

        # download the file
        logger.info("Deleting file from bucket.  Key=%s", key)
        self.s3_client.delete_object(Bucket=self.bucket_name, Key=key)

    def delete_root_dir(self, root_dir : str):
        """ Deletes all files in/under the root directory from the bucket.
        
            root_dir - root directory
        """
        # validate input parameters
        if root_dir is None or len(root_dir) == 0:
            msg = "root_dir is required but is empty!"
            logger.error(msg)
            raise ValueError(msg)

        # list files
        all_files = self.list()
        for file in all_files:
            # parse path
            path_object = Path(file)
            parts = path_object.parts

            # check for match
            if parts is not None and len(parts) > 1:
                if parts[0] == root_dir:
                    logger.warning("Deleting file: %s", file)
                    self.delete(file)
