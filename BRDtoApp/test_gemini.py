import os
from dotenv import load_dotenv
import google.generativeai as genai
import json # Will be useful for structured output

# Load .env variables
load_dotenv()

# Read the API key
api_key = os.getenv("GEMINI_API_KEY")

# IMPORTANT: Check if it actually loaded
if not api_key:
    raise ValueError("API key not found. Make sure your .env file is set correctly.")

# Configure Gemini with your API key
genai.configure(api_key=api_key)

# Use Gemini Flash (fast & free)
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

# --- Sample BRD Content (You'll load this from actual BRDs later) ---
sample_brd_content = """
**Business Requirement Document for Dealership Recruitment Workflow**

**1. Introduction**
This document outlines the requirements for a new web-based application to streamline the recruitment process for automotive dealerships.

**2. Features**
    * **Job Posting Management:** Dealership HR can create, edit, and publish job postings. Each posting includes job title, description, requirements, and location.
    * **Applicant Tracking System (ATS):** Applicants can apply to jobs, upload resumes, and track their application status. HR can view applications, filter by status, and move candidates through different stages (e.g., New, Reviewed, Interview, Offer, Hired, Rejected).
    * **Interview Scheduling:** HR can schedule interviews with candidates, sending automated calendar invitations.
    * **Reporting:** Generate reports on applicant pipeline, time-to-hire, and source of hire.
    * **User Authentication:** Secure login for HR personnel and applicants.

**3. User Roles**
    * **HR Manager:** Full access to job postings, ATS, reporting, and user management.
    * **Applicant:** Can browse jobs, apply, and track application status.

**4. UI Requirements**
    * Dashboard for HR with quick stats.
    * Job application form with resume upload.
    * Responsive design for mobile and desktop.

**5. Technical Requirements**
    * Backend: Python/Django
    * Frontend: React
    * Database: PostgreSQL
"""

# --- Prompting for Feature Extraction ---
prompt_feature_extraction = f"""
You are an AI assistant specialized in parsing Business Requirement Documents (BRDs) and extracting key information.
Your task is to identify and list the distinct features mentioned in the provided BRD content.
For each feature, provide a concise summary.

Output the features as a JSON array of objects, where each object has "feature_name" and "summary" keys.

BRD Content:
---
{sample_brd_content}
---

JSON Output:
"""

try:
    response_features = model.generate_content(prompt_feature_extraction)
    print("\n--- Feature Extraction Response ---")
    print(response_features.text)

    # Attempt to parse the JSON output
    features = json.loads(response_features.text)
    print("\nParsed Features:")
    for feature in features:
        print(f"  - {feature['feature_name']}: {feature['summary']}")

except Exception as e:
    print(f"An error occurred during feature extraction: {e}")
    # This is where you'd log the error and possibly refine your prompt

# --- Prompting for Code Generation (Example: Django Model) ---
prompt_django_model = f"""
You are an AI software engineer.
Based on the following feature description, generate a Python Django model for a Job Posting.
Include common fields like `title`, `description`, `requirements`, `location`, `created_at`, `updated_at`, and `is_active`.
Ensure the code is clean, follows Django conventions, and includes necessary imports.

Feature Description:
"Job Posting Management: Dealership HR can create, edit, and publish job postings. Each posting includes job title, description, requirements, and location."

Python Django Model:
"""

try:
    response_django_model = model.generate_content(prompt_django_model)
    print("\n--- Django Model Generation Response ---")
    print(response_django_model.text)
except Exception as e:
    print(f"An error occurred during Django model generation: {e}")