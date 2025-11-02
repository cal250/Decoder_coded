import cv2
import numpy as np
import os
from pyzbar.pyzbar import decode

def decode_aztec(image_path):
    """
    Decode Aztec code from an image file
    
    Args:
        image_path (str): Path to the image file containing Aztec code
        
    Returns:
        str: Decoded data from Aztec code or error message
    """
    if not os.path.exists(image_path):
        return f"Error: File not found - {image_path}"
    
    try:
        # Read the image
        img = cv2.imread(image_path)
        if img is None:
            return "Error: Could not read the image file"
            
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Try to enhance the image for better detection
        # Apply adaptive thresholding
        thresh = cv2.adaptiveThreshold(
            gray, 255, 
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY, 11, 2
        )
        
        # Try to decode Aztec code
        decoded_objects = decode((thresh.tobytes(), thresh.shape[1], thresh.shape[0]), symbols=[pyzbar.pyzbar.ZBarSymbol.AZTEC])
        
        if not decoded_objects:
            # If no Aztec code found, try with the original grayscale image
            decoded_objects = decode((gray.tobytes(), gray.shape[1], gray.shape[0]), symbols=[pyzbar.pyzbar.ZBarSymbol.AZTEC])
        
        if not decoded_objects:
            return "No Aztec code detected in the image"
            
        # Collect all decoded data
        results = []
        for obj in decoded_objects:
            try:
                data = obj.data.decode('utf-8')
            except UnicodeDecodeError:
                data = obj.data.decode('latin-1')  # Try alternative encoding
                
            results.append({
                'data': data,
                'type': obj.type,
                'rect': obj.rect,
                'polygon': obj.polygon
            })
            
        return results if len(results) > 1 else results[0]['data']
        
    except Exception as e:
        return f"Error decoding Aztec code: {str(e)}"

if __name__ == "__main__":
    # Look for image.png in the current directory
    image_path = "image.png"
    
    if not os.path.exists(image_path):
        print(f"Error: 'image.png' not found in the current directory.")
    else:
        print(f"Processing image: {image_path}")
        result = decode_aztec(image_path)
        print("\nDecoded data:")
        print(result)