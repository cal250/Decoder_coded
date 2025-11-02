import cv2
from pylibdmtx import pylibdmtx
import os

def decode_datamatrix(image_path):
    """
    Decode DataMatrix code from an image file
    
    Args:
        image_path (str): Path to the image file containing DataMatrix
        
    Returns:
        dict: Dictionary containing decoded data and metadata
    """
    if not os.path.exists(image_path):
        return {'error': f"File not found: {image_path}"}
    
    try:
        # Read the image
        img = cv2.imread(image_path)
        if img is None:
            return {'error': 'Could not read the image file'}

        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Try to decode DataMatrix
        decoded_objects = pylibdmtx.decode(gray)
        
        if not decoded_objects:
            # Try with thresholding if no results
            _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            decoded_objects = pylibdmtx.decode(thresh)
            
        if not decoded_objects:
            return {'error': 'No DataMatrix code detected in the image'}
            
        # Process results
        results = []
        for obj in decoded_objects:
            try:
                data = obj.data.decode('utf-8')
            except UnicodeDecodeError:
                try:
                    data = obj.data.decode('latin-1')
                except:
                    data = str(obj.data)
            
            results.append({
                'data': data,
                'type': 'DataMatrix',
                'rect': {
                    'left': obj.rect.left,
                    'top': obj.rect.top,
                    'width': obj.rect.width,
                    'height': obj.rect.height
                }
            })
        
        return results[0]  # Return first result
        
    except Exception as e:
        return {'error': f'Error decoding DataMatrix: {str(e)}'}

def print_result(result):
    """Print the decoding result in a user-friendly format"""
    if 'error' in result:
        print(f"\nError: {result['error']}")
    else:
        print("\nDecoded DataMatrix:")
        print(f"  Data: {result.get('data', 'N/A')}")
        print(f"  Type: {result.get('type', 'N/A')}")
        rect = result.get('rect', {})
        if rect:
            print(f"  Position: (x:{rect['left']}, y:{rect['top']}, width:{rect['width']}, height:{rect['height']})")

if __name__ == "__main__":
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(script_dir, "image.png")
    
    # Print the exact path being used for debugging
    print(f"Looking for image at: {image_path}")
    
    if not os.path.exists(image_path):
        print(f"Error: 'image.png' not found in the script's directory: {script_dir}")
    else:
        print(f"Processing image: {image_path}")
        result = decode_datamatrix(image_path)
        print_result(result)