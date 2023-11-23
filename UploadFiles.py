import os
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from tqdm import tqdm
from googleapiclient.http import MediaIoBaseDownload, MediaIoBaseUpload
from io import BytesIO
import pickle

# If modifying these SCOPES, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.file']

def get_service():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)
    return service

def upload_files(service, folder_id, source_folder):
    # List all files in the source folder
    files_to_upload = [os.path.join(source_folder, f) for f in os.listdir(source_folder) if os.path.isfile(os.path.join(source_folder, f))]
    
    for file_path in files_to_upload:
        file_metadata = {
            'name': os.path.basename(file_path),
            'parents': [folder_id]
        }

        with open(file_path, "rb") as f:
            # Create a BytesIO buffer and copy the file content
            file_buffer = BytesIO()
            file_buffer.write(f.read())
            file_size = file_buffer.tell()

            # Reset the buffer position
            file_buffer.seek(0)

            # Create a custom media upload object with progress bar
            media = MediaIoBaseUpload(file_buffer, mimetype='application/octet-stream', chunksize=1024*1024, resumable=True)
            request = service.files().create(body=file_metadata, media_body=media, fields='id')
            
            # Custom tqdm progress bar
            pbar = tqdm(total=file_size, unit='B', unit_scale=True, desc=f"Uploading {os.path.basename(file_path)}")
            
            response = None
            while response is None:
                status, response = request.next_chunk()
                if status:
                    pbar.update(status.resumable_progress - pbar.n)
            pbar.close()

def main():
    service = get_service()
    folder_id = 'Your_Folder_ID'  # Replace with the Google Drive Folder ID (The string behind the last '/' of the folder URL)
    source_folder = 'C:\\Your_Path\\'  # Replace with the path to your folder
    upload_files(service, folder_id, source_folder)

if __name__ == '__main__':
    main()
