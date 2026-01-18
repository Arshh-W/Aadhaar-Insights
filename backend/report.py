import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

#CONFIGURATION(.env bnakr usme GEMINI_API_KEY= krkr ek gemini api key paste krdena)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def generate_ai_report(input_stats):
    """
    Generates a text report using Google's Gemini API.
    """
    if not GEMINI_API_KEY:
        print(" Error: GEMINI_API_KEY is missing in .env file")
        return "Error: API Key missing. Please check backend configuration."

    try:
        # 2.Model 2.5 flash hi sahi h, baadme LLAMA krduna, fine tuned wala usspr thordhe errors resolve krne me time lgega
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-2.5-flash') 
        # 3. Create Prompt
        prompt = f"""
        You are an AI Analyst for the 'Adhaar Insights' dashboard.
        
        Task: Write a concise, professional executive summary (min 400 words) based on these daily statistics.
        Focus on operational risks and efficiency. Do not use markdown (no **bold** or # headers), just plain text.
        
        Statistics:
        {input_stats}
        """
        
        # 4. Generate
        print(" Asking Gemini...")
        response = model.generate_content(prompt)
        
        return response.text.strip()

    except Exception as e:
        print(f" Gemini API Error: {str(e)}")
        return "Report generation is temporarily unavailable."