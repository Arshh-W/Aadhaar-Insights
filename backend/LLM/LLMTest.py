import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app) 
# 1. Your Hugging Face Token
# Replace 'hf_...' with your actual WRITE token
HF_TOKEN = "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" 
API_URL = "https://router.huggingface.co/models/ArshRana258/LLAMA_ADHAAR_REPORTS_4BIT"
# 3. The Prompt 
PROMPT_TEMPLATE = """Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

### Instruction:
Generate a detailed District Aadhaar Performance Report based on the provided metrics.

### Input:
{input_data}

### Response:
"""

# --- HELPER FUNCTION ---
def query_huggingface_api(payload):
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    response = requests.post(API_URL, headers=headers, json=payload)
    
    # 1. Try to parse JSON (Success case)
    try:
        return response.json()
    except requests.exceptions.JSONDecodeError:
        # 2. If JSON fails, return the raw text (Error case)
        # This usually contains the "Model is loading" or "Time out" message
        print(f" Non-JSON Response: {response.text}")
        return {"error": f"Hugging Face Error: {response.text}"}

# --- ROUTES ---
@app.route('/')
def home():
    return " Aadhaar Report API is Online! Send POST requests to /generate"

@app.route('/generate', methods=['POST'])
def generate_report():
    try:
        # 1. Get Input
        data = request.json
        raw_input = data.get('input', '')

        if not raw_input:
            return jsonify({"error": "No 'input' provided"}), 400

        print(f"Processing request for: {raw_input[:30]}...")

        # 2. Format Prompt
        formatted_prompt = PROMPT_TEMPLATE.format(input_data=raw_input)

        # 3. Send to Hugging Face
        api_response = query_huggingface_api({
            "inputs": formatted_prompt,
            "parameters": {
                "max_new_tokens": 512,  
                "temperature": 0.1,     
                "return_full_text": False,
                "wait_for_model": True  # Crucial: Tells HF to wake up the model if sleeping
            }
        })

        # 4. Handle Potential API Errors
        if isinstance(api_response, dict) and "error" in api_response:
            return jsonify({"status": "error", "message": api_response["error"]}), 503
        
        # 5. Extract Text
        # The API returns a list: [{'generated_text': '...'}]
        generated_text = api_response[0]['generated_text']

        # Clean up output (remove the prompt if it leaked in)
        final_report = generated_text.split("### Response:")[-1].strip()

        return jsonify({
            "status": "success",
            "report": final_report
        })

    except Exception as e:
        print(f"Server Error: {str(e)}")
        return jsonify({"error": str(e)}), 500
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)