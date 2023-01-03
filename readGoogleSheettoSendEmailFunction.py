import gspread
from oauth2client.service_account import ServiceAccountCredentials
import google.auth
import sendgrid
import json
import traceback
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *
import base64
# This Google Cloud function is activated using HTTP trigger and on trigger it will fetch data from Google Sheets API . Then it will send this data as attachment to receiver email address 
# Define a function for authenticating with the Google Sheets API
def _authenticate_google_sheets():
    # Define the scope for the authentication
    scopes = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/spreadsheets',
             'https://www.googleapis.com/auth/drive.file',
             'https://www.googleapis.com/auth/drive']

    # Read the credentials from the service account keys file
    credentials, project_id = google.auth.default(scopes)

    # Initialize the authorization object            
    google_sheets_client = gspread.authorize(credentials)
    return google_sheets_client

def http_controller(request):
    # Authenticate with the Google Sheets API
    google_sheets_client = _authenticate_google_sheets()

    # Open the Google Sheets file
    try:
        google_sheets_file = google_sheets_client.open('HandsOnCloudSampleExcel')

        # Get the first sheet in the file
        sheet_info = google_sheets_file.sheet1

        # Get and print all records
        _send_email(json.dumps(sheet_info.get_all_records()))
    except gspread.exceptions.SpreadsheetNotFound:
        print('Error: The specified Google Sheets file was not found')
    except:
        print(traceback.format_exc())
    return '202'

def _send_email(data):
    # Set up the SendGrid client
    sg = SendGridAPIClient("<Your SendGrid API Key>")


    # Set up the email message
    from_email = Email("fromemail@test.com")
    to_email = To("toemail@test.com")
    subject = "Urgent!! 2022 Sales - Ambirt Inc"
    content = Content("text/plain", "Hi Simon, \n Please find sales data in attached file as below. \n regards")
    mail = Mail(from_email, to_email, subject, content)
    
    # Create the data for the attachment from a variable
    attachment = Attachment()
    attachment.file_content = FileContent(base64.b64encode(data.encode("utf-8")).decode())
    attachment.file_type = FileType('application/txt')
    attachment.file_name = FileName('dataAttachment.txt')
    attachment.disposition = Disposition('attachment')
    mail.attachment = attachment
    
    # Send the email
    try:
     response = sg.client.mail.send.post(request_body=mail.get())

    except:
        print(traceback.format_exc())
