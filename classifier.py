# manual few-shot version
import google.generativeai as genai
from PIL import Image
import os
import json
from dotenv import load_dotenv

class CouponValidator:
    def __init__(self, training_folder="data_samples"):
        load_dotenv()
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found")
        
        genai.configure(api_key=api_key)
        
        # USE STANDARD FLASH
        self.model_name = 'models/gemini-2.5-flash' 
        self.training_folder = training_folder
        self.few_shot_prompt = []
  
        examples = [
            {
                "filename": "136667.png", 
                "json_output": {
                    "status": "working",
                    "visibility": "VALLEMOBILE",
                    "language": "sk",
                    "absolute_discount": 45.00,
                    "discount_percentage": "29%",
                    "expiration_date": "",
                    "basket_value_before_discount": 152.10,
                    "basket_value_after_discount": 107.10
                }
            },
            {
                "filename": "142119.png", 
                "json_output": {
                    "status": "working",
                    "visibility": "CRAZY25",
                    "language": "en",
                    "absolute_discount": 227.00,
                    "discount_percentage": "25%",
                    "expiration_date": "",
                    "basket_value_before_discount": 908.00,
                    "basket_value_after_discount": 681.00
                }
            },
            {
                "filename": "157231.png", 
                "json_output": {
                    "status": "not working",
                    "visibility": "WC03_XKQR4V",
                    "language": "en",   
                    "absolute_discount": None,
                    "discount_percentage": "",
                    "expiration_date": "",
                    "basket_value_before_discount": None,
                    "basket_value_after_discount": 252.00
                }
            },
            {
                "filename": "6573893.png", 
                "json_output": {
                    "status": "working",
                    "visibility": "TNACN12",
                    "language": "en",   
                    "absolute_discount": None ,
                    "discount_percentage": "15%",
                    "expiration_date": "31 Dec 2025 17:59",
                    "basket_value_before_discount": 140.78,
                    "basket_value_after_discount": 125.65
                }
            }
        ]

        print("Loading training examples into memory...")
        
        for ex in examples:
            path = os.path.join(self.training_folder, ex['filename'])
            if os.path.exists(path):
                img = Image.open(path)
                
                self.few_shot_prompt.append("Example Image:")
                self.few_shot_prompt.append(img)
                self.few_shot_prompt.append(f"Correct JSON Response: {json.dumps(ex['json_output'])}")
            else:
                print(f"[WARNING] Example not found: {path}")

        self.model = genai.GenerativeModel(
            self.model_name,
            generation_config={"response_mime_type": "application/json"}
        )
        print(f"Validator Ready. Loaded {len(self.few_shot_prompt) // 3} examples.")

    def classify_coupon(self, screenshot_path) -> dict:
        new_image = Image.open(screenshot_path)
        
        prompt_parts = [
            """
            SYSTEM RULES:
            You are a Coupon Validator. Extract data into this exact JSON structure:
            {
                "status": "working" | "not_working",
                "visibility": "exact_code",
                "language": "en" | "fr" | "de",
                "absolute_discount": 0.0,
                "discount_percentage": "20%" | "",
                "expiration_date": "dd/mm/yyyy" | "31 Dec 2025 5:59 PM"| "",
                "basket_value_before_discount": 0.0,
                "basket_value_after_discount": 0.0
            }
            Analyze the examples below to understand how to handle edge cases.
            Rules: 
            1. For "status": "working" requires green text/discount applied. There could be phrases such as 'coupon applied', 'you saved', etc. in ANY language.
            2. Fot "status": "not_working" requires red text/error. THere could be phrases such as 'invalid', 'expired', 'not applicable', "enter valid coupon" etc. in ANY language.
            3. "visibility": Exact coupon code case-sensitive.
            4. "language": 2-letter code (en, fr, de, etc). Empty string "" if uncertain.
            5. "absolute_discount": Extract exact amounts (float). Empty 0.0 if not visible or not working.
            6. "discount_percentage": % or absolute value. Empty string "" if not visible or not working.
            7. "expiration_date": Format as displayed on the screenshot. Empty string if "status" is "not_working" or not visible.
            8. "basket_value_before_discount": Extract exact amounts (float).
            10. "basket_value_after_discount": Extract exact amounts (float).
            """
        ]
        
        prompt_parts.extend(self.few_shot_prompt)
        prompt_parts.append("Now analyze this NEW image:")
        prompt_parts.append(new_image)

        try:
            response = self.model.generate_content(prompt_parts)
            return json.loads(response.text)
        except Exception as e:
            return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    validator = CouponValidator()
    # Make sure this path exists!
    result = validator.classify_coupon("75044.png")
    print(json.dumps(result, indent=2))