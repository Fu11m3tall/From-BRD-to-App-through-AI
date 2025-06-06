import json
import logging
import re  # Import the regular expression module
from django.shortcuts import render
from django.http import JsonResponse
from .utils.brd_parser import extract_text_from_pdf
from .utils.gemini_client import analyze_brd

# You'll need these for docx/doc parsing if you decide to implement them
# from docx import Document  # pip install python-docx
# from textract import process # pip install textract (might have external dependencies)

logger = logging.getLogger(__name__)

def upload_brd_view(request):
    # This view will now always render the 'brd-upload.html' template for GET requests.
    # For POST requests (AJAX), it will return JSON.

    if request.method == 'POST':
        # --- Crucial: Get the file by the name your JavaScript sends it as! ---
        uploaded_file = request.FILES.get('brd_file')  # This now matches 'brd_file' from JS

        # Default response data structure for JSON
        response_data = {
            'status': 'error',
            'message': 'An unknown error occurred.',
            'analysis_data': None,
            'extracted_text': None,
            'raw_ai_response': None  # For debugging AI JSON parsing errors
        }

        if not uploaded_file:
            response_data['message'] = "No file was uploaded. Please select a file and try again."
            logger.warning("AJAX: No file uploaded in POST request.")
            return JsonResponse(response_data, status=400)  # Bad Request

        filename = uploaded_file.name  # Capture filename

        try:
            file_extension = uploaded_file.name.lower().split('.')[-1]
            extracted_text = None

            if file_extension == 'pdf':
                extracted_text = extract_text_from_pdf(uploaded_file)
            elif file_extension == 'txt':
                extracted_text = uploaded_file.read().decode('utf-8')
            # Add DOCX/DOC parsing here, remember to handle dependencies:
            # elif file_extension == 'docx':
            #     from docx import Document
            #     doc = Document(uploaded_file)
            #     extracted_text = "\n".join([p.text for p in doc.paragraphs])
            # elif file_extension == 'doc':
            #     response_data['message'] = "'.doc' files require additional setup (e.g., textract) on the server. Please upload .pdf, .docx, or .txt."
            #     return JsonResponse(response_data, status=400)
            else:
                response_data['message'] = f"Unsupported file type: '.{file_extension}'. Please upload PDF, DOCX, or TXT."
                logger.warning(f"AJAX: Unsupported file upload attempt: {uploaded_file.name}")
                return JsonResponse(response_data, status=400)  # Bad Request

            if not extracted_text:
                response_data['message'] = "Could not extract text from the uploaded file. It might be empty, corrupted, or an unsupported format despite the extension."
                return JsonResponse(response_data, status=400)

            logger.info(f"AJAX: Successfully extracted text from {uploaded_file.name}")

            # --- YOUR ACTUAL AI CALL GOES HERE ---
            # Call your `analyze_brd` function from `gemini_client`
            gemini_raw_response = analyze_brd(extracted_text)
            response_data['raw_ai_response'] = gemini_raw_response  # Always pass raw for debugging

            logger.info("AJAX: Successfully received AI raw response.")

            # Attempt to parse the AI's JSON response
            try:
                # --- CRITICAL FIX: Extract JSON from Markdown code block ---
                match = re.search(r'```json\n(.*?)\n```', gemini_raw_response, re.DOTALL)
                if match:
                    json_string = match.group(1)
                else:
                    # If no markdown block is found, assume the entire output is JSON (less robust)
                    # This could happen if the AI sometimes doesn't wrap its JSON.
                    json_string = gemini_raw_response.strip()

                ai_analysis_data = json.loads(json_string)  # Attempt to parse the cleaned string

                # Check if the AI's JSON indicates an internal AI error, e.g., if it couldn't structure it
                if isinstance(ai_analysis_data, dict) and "error" in ai_analysis_data:
                    response_data['status'] = 'error'
                    response_data['message'] = f"AI reported an internal error: {ai_analysis_data.get('error_details', 'No details provided.')}"
                    response_data['analysis_data'] = ai_analysis_data  # Still send the data for client debugging
                    return JsonResponse(response_data, status=500)  # Internal Server Error
                
                response_data['status'] = 'success'
                response_data['message'] = 'BRD analyzed successfully.'
                response_data['analysis_data'] = ai_analysis_data
                response_data['extracted_text'] = extracted_text  # Send extracted text back for display/debugging
                logger.info("AJAX: AI response parsed as JSON successfully.")
                return JsonResponse(response_data)  # Default status is 200 OK

            except json.JSONDecodeError as e:
                response_data['message'] = f"AI response was not valid JSON. Please check prompt or BRD content. Error: {e}"
                logger.error(f"AJAX: JSON Decode Error: {e}. Raw AI response: {gemini_raw_response}")
                return JsonResponse(response_data, status=500)  # Internal Server Error
            
        except Exception as e:
            logger.exception(f"AJAX: An unexpected server-side error occurred during file processing or AI analysis for {filename}.")
            response_data['message'] = f"An internal server error occurred: {e}"
            return JsonResponse(response_data, status=500)  # Internal Server Error
    
    # For GET requests, render the initial HTML page
    return render(request, 'brd-upload.html')  # Ensure this is the correct template name