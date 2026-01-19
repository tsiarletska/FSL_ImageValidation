# from classifier import CouponValidator
# import sys

# def main():
#     # Check if image path provided
#     if len(sys.argv) < 2:
#         print("Usage: python main.py <path_to_screenshot>")
#         print("Example: python main.py data/screenshots/test.png")
#         sys.exit(1)
    
#     screenshot_path = sys.argv[1]
    
#     # Initialize validator
#     print("Initializing Coupon Validator...")
#     validator = CouponValidator()
    
#     # Classify coupon
#     print(f"\nAnalyzing: {screenshot_path}")
#     print("-" * 50)
    
#     try:
#         result = validator.classify_coupon(screenshot_path)
        
#         print(f"Status:            {result['status']}")
#         print(f"Visibility:        {result['visibility']}")
#         print(f"Language:          {result['language']}")
#         print(f"Discount:          {result['discount']}")
#         print(f"Expiration Date:  {result['expiration_date']}")

        
#         if 'raw_response' in result:
#             print(f"\nRaw response: {result['raw_response']}")
            
#     except Exception as e:
#         print(f"\nError: {e}")
#         sys.exit(1)

# if __name__ == "__main__":
#     main()


from classifier import CouponValidator
import sys

def main():
    # Check if image path provided
    if len(sys.argv) < 2:
        print("Usage: python main.py <path_to_screenshot>")
        print("Example: python main.py data/screenshots/test.png")
        sys.exit(1)
    
    screenshot_path = sys.argv[1]
    
    # Initialize validator
    print("Initializing Coupon Validator...")
    validator = CouponValidator()
    
    # Classify coupon
    print(f"\nAnalyzing: {screenshot_path}")
    print("-" * 50)
    
    try:
        # result is now a raw string (e.g., "working|CODE|en|20%|date")
        result = validator.classify_coupon(screenshot_path)
        
        # Print the raw string directly
        print(result)
            
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()