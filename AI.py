import google.generativeai as genai
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

def get_gemini_response(query):
    try:
        # Configure the model with safety settings
        model = genai.GenerativeModel('gemini-pro')
        
        # Provide context that encourages flexible understanding
        context = """You are a helpful AI assistant for Rangsit University (RSU) in Thailand. You should:
        1. Understand and respond to questions even if they contain spelling errors or typos
        2. Focus on providing helpful information about RSU
        3. Be conversational and friendly
        4. If you're not sure about something, say so politely

        Key facts about RSU:
        - Academic Calendar: Semester 1 (August-December), Semester 2 (January-May), Summer (June-July)
        - Admission Requirements: High School completion, IELTS 5.5 or equivalent
        - Contact: Email rsuip@rsu.ac.th, Phone +662 997 2200 ext. 4012, 4019
        - Facilities: Libraries, labs, computer centers, sports facilities, accommodation, dining halls
        - Scholarships: Merit-based, need-based, and special talent scholarships available
        - International Support: Visa assistance, orientation, academic advising, language support
        - RIC (Rangsit International College): Led by Dean AJ Todsanai, offers international programs

        Even if a question isn't perfectly written or contains spelling mistakes, try to understand what they're asking and provide helpful information about RSU."""

        # Generate response with temperature setting for more natural responses
        response = model.generate_content(
            f"{context}\n\nUser's question (please understand even if it has spelling errors): {query}",
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                candidate_count=1,
                stop_sequences=None,
                max_output_tokens=2048,
                top_p=0.8,
                top_k=40,
            )
        )
        
        if response and response.text:
            return response.text
        return "I apologize, but I couldn't generate a response. Please try rephrasing your question."
    
    except Exception as e:
        print(f"Gemini API Error: {str(e)}")
        # Only fall back to predefined responses for actual API errors
        return get_predefined_response(query)

def get_predefined_response(query):
    # Keep existing predefined responses as fallback
    responses = {
        "academic calendar": """RSU Academic Calendar:
            Semester 1: August - December
            Semester 2: January - May
            Summer: June - July""",
            
        "admission": """Admission Requirements for Rangsit University:
            1. Academic Requirements:
               - Completed Upper Secondary School (M.6) or equivalent
               - High School Grade 12 (US System)
               - Cambridge IGCSE/O-Level (5 subjects, Grade C or above)
            2. English Requirements:
               - IELTS 5.5 or
               - TOEFL: PBT 500, CBT 173, IBT 60 or
               - Pass RSU English Placement Test""",
            
        "contact": """You can contact Rangsit University through:
            - Email: rsuip@rsu.ac.th
            - Phone: +662 997 2200 ext. 4012, 4019
            - Social Media: Facebook, Line, Instagram, and Twitter""",
            
        "facilities": """Rangsit University facilities include:
            - Modern libraries with online databases
            - Well-equipped laboratories
            - Computer centers
            - Sports facilities and gymnasiums
            - Student accommodation
            - Dining halls and cafeterias
            - Recreational areas""",
            
        "scholarships": """Rangsit University offers various scholarships:
            - Merit-based scholarships
            - Need-based financial aid
            - Special talent scholarships
            Contact the admissions office for current opportunities.""",
            
        "support": """International student support services include:
            - Visa assistance
            - Orientation programs
            - Academic advising
            - Language support
            - Cultural integration programs""",

        "dean": """The dean of RIC (Rangsit International College) is AJ Todsanai.""",
    }
    query = query.lower()
    
    # Check for specific keywords and return appropriate response
    if "dean" in query or "head" in query or "director" in query:
        if "ric" in query or "international" in query:
            return responses["dean"]
    elif "calendar" in query or "semester" in query or "term" in query:
        return responses["academic calendar"]
    elif "admission" in query or "requirements" in query or "apply" in query:
        return responses["admission"]
    elif "contact" in query or "email" in query or "phone" in query:
        return responses["contact"]
    elif "facilities" in query or "campus" in query:
        return responses["facilities"]
    elif "scholarship" in query or "financial" in query:
        return responses["scholarships"]
    elif "support" in query or "help" in query or "international" in query:
        return responses["support"]
    elif any(school in query for school in ["other university", "other school", "different university"]):
        return "I apologize, but I am designed to provide information specifically about Rangsit University. If you have any inquiries regarding Rangsit University, feel free to ask."
    elif not any(keyword in query for keyword in ["university", "school", "education", "study", "student", "course", "program", "ric", "rangsit", "dean", "international"]):
        return "Sorry, I am designed to answer questions related to Rangsit University only."
    else:
        return "I understand you're asking about Rangsit University. Could you please be more specific about what information you need? You can ask about admissions, academic calendar, facilities, scholarships, or support services."

def ai_function(request):
    """Handle the chat request"""
    try:
        if request.method == 'POST':
            try:
                req_body = request.json
            except Exception:
                return {
                    "success": False,
                    "message": "Invalid request format"
                }

            if not req_body or 'message' not in req_body or not req_body['message']:
                return {
                    "success": False,
                    "message": "Please enter a question about Rangsit University"
                }

            # Try to get response from Gemini API
            gemini_response = get_gemini_response(req_body['message'])
            
            if gemini_response:
                return {
                    "success": True,
                    "message": gemini_response
                }
            else:
                # Fallback to predefined responses if API fails
                predefined_response = get_predefined_response(req_body['message'])
                return {
                    "success": True,
                    "message": predefined_response
                }
    except Exception as e:
        return {
            "success": False,
            "message": "I'm having trouble processing your request. Please try again."
        }