### General Setup

1.  **Import Libraries**: Import necessary libraries such as Flask, google.generativeai, os, etc.
2.  **Configure Logging**: Set up logging for debugging and monitoring.
3.  **Initialize Flask App**: Create a Flask application instance.
4.  **Configure Session**: Set up session management for user data.
5.  **Configure CORS**: Enable Cross-Origin Resource Sharing for the app.
6.  **Configure Gemini**: Initialize the Gemini model with an API key.
7.  **Global Variables**:
    *   `browser_opened`: Flag to control browser opening.
    *   `latest_rfid_data`: Dictionary to store the latest RFID data.
    *   `excel_file_path`: Path to the Excel file for storing patient data.
    *   `REPORTS_DIR`: Path to the directory containing patient reports.
    *    `PDF_SPECIFIC_DIR`: Path to a specific directory containing PDF reports.
8.  **File Mover Functionality:**
    *   `start_file_mover()`: Function to start a separate script (`filemover.py`) as a subprocess for moving files from a downloads folder to a destination folder.
    *   `stop_file_mover()`: Function to terminate the file mover subprocess when the Flask app exits. This function is registered to be called on exit.

### Utility Functions

1.  `update_excel_with_rfid(pid)`:
    *   Get current date and time.
    *   Create a Pandas DataFrame with the PID, date, and time.
    *   Check if the Excel file exists.
    *   If exists, append the new data to the existing data.
    *   If not exists, create a new Excel file with the data.
    *   Save the updated DataFrame to the Excel file.
2.  `get_last_visit_info(pid)`:
    *   Read data from the Excel file using Pandas.
    *   Filter rows for the given patient ID.
    *   Sort visits by date and time.
    *   If only one visit, return "First Visit" indicator.
    *   Otherwise, get the second to last visit record.
    *   Calculate days since the last visit.
    *   Return the last visit date, time, and days since.

### Route Handlers

1.  `/process_audio` (POST):
    *   Get audio file from the request.
    *   Save the audio file to a temporary file.
    *   Transcribe the audio using the Whisper model.
    *   Store the transcript in the session.
    *   Remove the temporary audio file.
    *   Return the transcript as JSON.
2.  `/generate_report` (POST):
    *    Read transcript from file.
    *   Generate a medical report using the Gemini model based on the transcript and a predefined prompt.
    *   Clean the HTML content in the response.
    *   Store the cleaned HTML report in the session.
    *   Return the cleaned HTML report.
3.  `/get_report` (GET):
    *   Retrieve the medical report from the session.
    *   If no report found, return an error.
    *   Return the report.
4.  `/view_report/<patient_id>/<report_name>`:
    *   Construct the file path for the report.
    *   Read the content of the report file.
    *   Render the `view_report.html` template with the report content.
5.  `/report`:
    *   Get patient ID from URL parameters.
    *   List reports for the given patient ID.
    *   Render the `report.html` template with the list of reports.
    *   Add specific PDFs to reports.
6.  `/view-specific-pdf/<filename>`:
    *   Serve a PDF file from a specific directory.
7.  `/view_pdf/<patient_id>/<filename>`:
    *   Construct the path to the PDF file.
    *   Serve the PDF file.
8.  `/analyze-pdf` (POST):
    *   Get the PDF file from the request.
    *   Save the PDF file to a temporary file.
    *   Read the PDF data.
    *   Generate a summary using the Gemini model.
    *   Remove the temporary file.
    *   Return the summary as JSON.
9.  `/rfid_trigger`:
    *   Get RFID UID from the request.
    *   Update the `latest_rfid_data`.
    *   Clear the session.
    *   Store the patient ID and scan time in the session.
    *   Update the Excel file with the RFID data.
    *   Open the browser if it's not already opened or if the last trigger was more than 5 seconds ago.
    *   Return a success status as JSON.
10. `/latest_rfid`:
    *   Return the `latest_rfid_data` as JSON.
11. `/test`:
    *   Return a success message for ESP32 connection.
12. `/get_patient_id`:
    *   Return the patient ID from the session as JSON.
13. `/`:
    *   Render the `landing.html` template with the patient ID and last visit information.
14. `/voice-capture`:
    *   Render the `voice-capture.html` template.
15. `/voice-capture2`:
    *   Render the `voice-capture2.html` template.
16. `/app`:
    *   Render the `index.html` template.
17. `/vitals.html`:
    *   Render the `vitals.html` template.
18. `/reports/<patient_id>`:
    *   Get reports for the patient ID.
    *   Render the `reports.html` template with the reports data.

### Main Execution

1.  **Start Flask App**: Run the Flask application on host `0.0.0.0` and port 5000 with debugging enabled.
