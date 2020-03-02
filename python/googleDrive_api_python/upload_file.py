#!/usr/bin/python

"""Google Drive Quickstart in Python.
This script uploads a single file to Google Drive.
edit by baijun,makeitbai@qq.com
ps:try more times if failed
reference:https://developers.google.com/drive/api/v3/quickstart/python
Step 1: Turn on the Drive API via reference
Step 2: Install the Google Client Library
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
Step 3:upload files
"""

from __future__ import print_function
import pprint
import six
import httplib2
from googleapiclient.discovery import build
import googleapiclient.http
import oauth2client.client
import argparse

parser = argparse.ArgumentParser(description='upload to google drive',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-f','--file_path',dest='file_path',help='file_path to upload',required=True, type=str)
args = parser.parse_args()
# OAuth 2.0 scope that will be authorized.
# Check https://developers.google.com/drive/scopes for all available scopes.
OAUTH2_SCOPE = 'https://www.googleapis.com/auth/drive'

# Location of the client secrets.
CLIENT_SECRETS = 'credentials.json'

# Path to the file to upload.
#FILENAME = 'document.txt'#'1904.09290.pdf',test succeed in format[.txt,.pdf,.7z],so i guess any type is ok
FILENAME = args.file_path
# Metadata about the file.
MIMETYPE = 'text/plain'
TITLE = FILENAME.split('/')[-1]#'My New Text Document'#new name,locate in root path in drive
DESCRIPTION = 'A shiny new text document about hello world.'

# Perform OAuth2.0 authorization flow.
flow = oauth2client.client.flow_from_clientsecrets(CLIENT_SECRETS, OAUTH2_SCOPE)
flow.redirect_uri = oauth2client.client.OOB_CALLBACK_URN
authorize_url = flow.step1_get_authorize_url()
print('Go to the following link in your browser: ' + authorize_url)
# `six` library supports Python2 and Python3 without redefining builtin input()
code = six.moves.input('Enter verification code: ').strip()
credentials = flow.step2_exchange(code)

# Create an authorized Drive API client.
http = httplib2.Http()
credentials.authorize(http)
drive_service = build('drive', 'v2', http=http)

# Insert a file. Files are comprised of contents and metadata.
# MediaFileUpload abstracts uploading file contents from a file on disk.
media_body = googleapiclient.http.MediaFileUpload(
    FILENAME,
    mimetype=MIMETYPE,
    resumable=True
)
# The body contains the metadata for the file.
body = {
  'title': TITLE,
  'description': DESCRIPTION,
}

# Perform the request and print the result.
new_file = drive_service.files().insert(
  body=body, media_body=media_body).execute()
pprint.pprint(new_file)
