import cv2
import numpy as np
from pyzbar.pyzbar import decode
import os

def preprocess_image(img):
    """Apply various preprocessing techniques to improve QR code detection"""
    # Convert to grayscale if not already
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img.copy()
    
    # Apply different preprocessing techniques
    preprocessed = []
    
    # 1. Original grayscale
    preprocessed.append(('original', gray))
    
    # 2. Adaptive thresholding
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                 cv2.THRESH_BINARY, 11, 2)
    preprocessed.append(('adaptive_threshold', thresh))
    
    # 3. Bilateral filter
    bilateral = cv2.bilateralFilter(gray, 9, 75, 75)
    preprocessed.append(('bilateral', bilateral))
    
    # 4. Histogram equalization
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    equalized = clahe.apply(gray)
    preprocessed.append(('equalized', equalized))
    
    return preprocessed

def decode_qr_code(image_path):
    """
    Decode QR code from an image file with multiple preprocessing techniques
    
    Args:
        image_path (str): Path to the image file containing QR code
        
    Returns:
        dict: Decoded data and processing information
    """
    if not os.path.exists(image_path):
        return {'error': f"File not found: {image_path}"}
    
    try:
        # Read the image
        img = cv2.imread(image_path)
        if img is None:
            return {'error': 'Could not read the image file'}
        
        # Get different preprocessed versions
        processed_versions = preprocess_image(img)
        
        results = []
        for method, processed in processed_versions:
            # Try to decode
            decoded_objects = decode(processed)
            
            if decoded_objects:
                for obj in decoded_objects:
                    try:
                        data = obj.data.decode('utf-8')
                    except UnicodeDecodeError:
                        data = str(obj.data)
                        
                    result = {
                        'data': data,
                        'type': obj.type,
                        'method': method,
                        'rect': obj.rect,
                        'polygon': obj.polygon
                    }
                    results.append(result)
            
        if not results:
            # If no QR code found, try with resized images
            for scale in [0.5, 0.75, 1.25, 1.5]:
                h, w = img.shape[:2]
                resized = cv2.resize(img, (int(w * scale), int(h * scale)))
                resized_versions = preprocess_image(resized)
                
                for method, processed in resized_versions:
                    decoded_objects = decode(processed)
                    if decoded_objects:
                        for obj in decoded_objects:
                            try:
                                data = obj.data.decode('utf-8')
                            except UnicodeDecodeError:
                                data = str(obj.data)
                                
                            result = {
                                'data': data,
                                'type': obj.type,
                                'method': f"{method} (resized {scale}x)",
                                'rect': obj.rect,
                                'polygon': obj.polygon
                            }
                            results.append(result)
                            
                            # If we found something, no need to try other methods
                            break
                    
                    if results:
                        break
                
                if results:
                    break
        
        if not results:
            return {'error': 'No QR code detected in the image after multiple attempts'}
            
        # Return all found results with their methods
        return results if len(results) > 1 else results[0]
        
    except Exception as e:
        return {'error': f'Error decoding QR code: {str(e)}'}

def print_result(result):
    """Print the decoding result in a readable format"""
    if isinstance(result, dict) and 'error' in result:
        print(f"\nError: {result['error']}")
        return
        
    if isinstance(result, list):
        print("\nFound multiple QR codes:")
        for i, r in enumerate(result, 1):
            print(f"\nQR Code {i}:")
            print(f"  Data: {r.get('data', 'N/A')}")
            print(f"  Type: {r.get('type', 'N/A')}")
            print(f"  Method: {r.get('method', 'N/A')}")
    else:
        print("\nDecoded QR Code:")
        print(f"  Data: {result.get('data', 'N/A')}")
        print(f"  Type: {result.get('type', 'N/A')}")
        print(f"  Method: {result.get('method', 'N/A')}")

if __name__ == "__main__":
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(script_dir, "image.png")
    
    if not os.path.exists(image_path):
        print(f"Error: 'image.png' not found in the script's directory: {script_dir}")
    else:
        print(f"Processing image: {image_path}")
        result = decode_qr_code(image_path)
        print_result(result)