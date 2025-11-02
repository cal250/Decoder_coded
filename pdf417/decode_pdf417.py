import os
import cv2
import numpy as np
from pyzbar.pyzbar import decode, ZBarSymbol

def decode_pdf417(image_path):
    """Simple PDF417 decoder using pyzbar"""
    try:
        # Read the image
        img = cv2.imread(image_path)
        if img is None:
            return {'error': 'Could not read the image file'}
        
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Try different binarization methods
        for thresh_type in ['otsu', 'adaptive', 'simple']:
            if thresh_type == 'otsu':
                # Otsu's thresholding
                blur = cv2.GaussianBlur(gray, (5,5), 0)
                _, binary = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            elif thresh_type == 'adaptive':
                # Adaptive thresholding
                binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                            cv2.THRESH_BINARY, 11, 2)
            else:
                # Simple threshold
                _, binary = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)
            
            # Try to decode PDF417
            decoded_objects = decode((binary.tobytes(), binary.shape[1], binary.shape[0]), 
                                  symbols=[ZBarSymbol.PDF417])
            
            if decoded_objects:
                data = decoded_objects[0].data
                try:
                    return {'data': data.decode('utf-8'), 'method': thresh_type}
                except:
                    try:
                        return {'data': data.decode('latin-1'), 'method': thresh_type}
                    except:
                        return {'data': str(data), 'method': thresh_type}
        
        return {'error': 'No PDF417 barcode detected in the image'}
    
    except Exception as e:
        return {'error': f'Error decoding PDF417: {str(e)}'}

def print_result(result):
    """Print the decoding result in a user-friendly format"""
    if 'error' in result:
        print(f"\nError: {result['error']}")
    else:
        print("\nDecoded Barcode:")
        print(f"  Data: {result.get('data', 'N/A')}")
        print(f"  Method: {result.get('method', 'N/A')}")

if __name__ == "__main__":
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(script_dir, "image.png")
    
    if not os.path.exists(image_path):
        print(f"Error: 'image.png' not found in the script's directory: {script_dir}")
    else:
        print(f"Processing image: {image_path}")
        result = decode_pdf417(image_path)
        print_result(result)