import cv2
from pylibdmtx import pylibdmtx
import os

def decode_datamatrix(image_path):
    """
    Decode DataMatrix code from an image file
    
    Args:
        image_path (str): Path to the image file containing DataMatrix
        
    Returns:
        str: Decoded data from DataMatrix or error message
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
        
        # Decode DataMatrix
        decoded_objects = pylibdmtx.decode(gray)
        
        if not decoded_objects:
            return "No DataMatrix code detected in the image"
            
        # Collect all decoded data
        results = []
        for obj in decoded_objects:
            results.append({
                'data': obj.data.decode('utf-8'),
                'rect': obj.rect,
                'polygon': obj.polygon
            })
            
        return results if len(results) > 1 else results[0]['data']
        
    except Exception as e:
        return f"Error decoding DataMatrix: {str(e)}"

if __name__ == "__main__":
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(script_dir, "image.png")
    
    if not os.path.exists(image_path):
        print(f"Error: 'image.png' not found in the script's directory: {script_dir}")
    else:
        print(f"Processing image: {image_path}")
        result = decode_datamatrix(image_path)
        print("\nDecoded data:")
        print(result)
