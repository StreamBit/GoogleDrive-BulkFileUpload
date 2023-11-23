# Google Drive Bulk File Uploader

## Description
This Python script allows for bulk uploading of files from a specified local directory to a Google Drive folder. It handles authentication, supports large files by uploading in chunks, and provides a real-time progress bar for each file upload.

## Requirements
- Google Drive API enabled in your Google Cloud project.
- `credentials.json` from the Google Developer Console for OAuth2 authentication.
- Python libraries: `google-auth-oauthlib`, `google-api-python-client`, `tqdm`.

## Setup
1. Place your `credentials.json` file in the same directory as the script.
2. Install required libraries:
```
pip install google-auth-oauthlib google-api-python-client tqdm
```

## Usage
1. Run the script once to authenticate and save the authentication token:
```
python UploadFiles.py
```

2. Modify `folder_id` in the script with the ID of the target Google Drive folder.
3. Change `source_folder` to the path of your local directory containing the files to upload.
4. Re-run the script to start uploading files.

## Features
- Bulk uploads files from a specified directory.
- Handles large files with chunked uploads.
- Displays upload progress with a real-time progress bar.

## Notes
- If modifying the OAuth scopes, delete `token.pickle` to re-authenticate.
- Ensure your Google Drive API and billing are properly set up in the Google Cloud Console.

## Author
StreamBit
