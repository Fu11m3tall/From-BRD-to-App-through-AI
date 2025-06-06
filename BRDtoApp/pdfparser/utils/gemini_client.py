# pdfparser/utils/gemini_client.py

import google.generativeai as genai
import os
import logging

logger = logging.getLogger(__name__)

# Ensure your .env is loaded in settings.py before this runs
try:
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
except KeyError:
    logger.error("GEMINI_API_KEY environment variable not set. Please set it in your .env file or environment.")
    # You might want to raise an exception here or handle it gracefully
    raise EnvironmentError("GEMINI_API_KEY not found.")

# Use a more powerful model for complex BRDs if possible, e.g., gemini-1.5-pro
# However, stick to gemini-1.5-flash if you're hitting limits or concerned about cost for now.
# For local Ollama models, this file would be completely different.
model = genai.GenerativeModel("gemini-1.5-flash") 

def analyze_brd(parsed_text):
    prompt = f"""
    You are an AI project analyst. Break down the following Business Requirement Document (BRD) content into structured data.
    Identify the key elements: Themes, Epics, User Stories, and Tasks.
    
    For each section, provide clear and concise points.
    
    Format the entire output as a JSON object with the following structure:
    {{
      "project_summary": "A brief summary of the overall project.",
      "themes": [
        {{
          "theme_name": "Name of Theme 1",
          "description": "Description of Theme 1",
          "epics": [
            {{
              "epic_name": "Name of Epic 1.1",
              "description": "Description of Epic 1.1",
              "user_stories": [
                {{
                  "story_id": "US-001",
                  "title": "As a [user type], I want [goal], so that [reason/benefit].",
                  "acceptance_criteria": [
                    "Criterion 1",
                    "Criterion 2"
                  ],
                  "tasks": [
                    "Task 1.1.1",
                    "Task 1.1.2"
                  ]
                }}
                // ... more user stories for this epic
              ]
            }}
            // ... more epics for this theme
          ]
        }}
        // ... more themes
      ]
    }}

    BRD Content:
    ---
    {parsed_text}
    ---
    """
    
    try:
        response = model.generate_content(prompt)
        # Assuming the model returns text that is a valid JSON string
        return response.text
    except Exception as e:
        logger.error(f"Error generating content from Gemini: {e}")
        return f"AI analysis failed: {e}"