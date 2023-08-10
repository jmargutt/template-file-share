import requests
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from azure.storage.fileshare import ShareDirectoryClient, ShareFileClient, generate_account_sas, ResourceTypes, AccountSasPermissions
import click
import logging
logging.root.handlers = []
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG, filename='ex.log')
# set up logging to console
console = logging.StreamHandler()
console.setLevel(logging.WARNING)
# set a format which is simpler for console use
formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(message)s')
console.setFormatter(formatter)
logging.getLogger("").addHandler(console)
load_dotenv(dotenv_path="../credentials/.env")
connection = os.getenv('CONNECTION').encode('utf-8').decode('utf-8')


def upload_file(share, file_path, share_path, sas_token):
    file_client = ShareFileClient(
        account_url=f"https://{os.getenv('ACCOUNT_NAME')}.file.core.windows.net",
        credential=sas_token,
        share_name=share,
        file_path=share_path)
    with open(file_path, "rb") as source_file:
        file_client.upload_file(source_file)


def download_file(share, file_path, share_path, sas_token):
    file_client = ShareFileClient(
        account_url=f"https://{os.getenv('ACCOUNT_NAME')}.file.core.windows.net",
        credential=sas_token,
        share_name=share,
        file_path=share_path)
    with open(file_path, "wb") as file_handle:
        data = file_client.download_file()
        data.readinto(file_handle)


def list_files(share, directory, sas_token):
    parent_dir = ShareDirectoryClient(
        account_url=f"https://{os.getenv('ACCOUNT_NAME')}.file.core.windows.net",
        credential=sas_token,
        share_name=share,
        directory_path=directory)
    share_list = list(parent_dir.list_directories_and_files())
    return [f"{share.name}" for share in share_list]


@click.command()
def main():
    utc_timestamp = datetime.utcnow()

    sas_token = generate_account_sas(
        account_name=os.getenv("ACCOUNT_NAME"),
        account_key=os.getenv("ACCOUNT_KEY"),
        resource_types=ResourceTypes(service=True, container=True, object=True),
        permission=AccountSasPermissions(
            read=True, write=True, delete=True, list=True, add=True, create=True, update=True, process=True,
            delete_previous_version=True),
        expiry=datetime.utcnow() + timedelta(hours=1)
    )
    file_share = os.getenv('SHARE')

    print(list_files(file_share, 'export-data', sas_token))
    download_file(file_share, '...', '...', sas_token)
    upload_file(file_share, '...', '...', sas_token)

    logging.info('Python timer trigger function ran at %s', utc_timestamp)


if __name__ == "__main__":
    main()

