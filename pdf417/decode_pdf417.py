import cv2
import pyzbar.pyzbar as pyzbar
import os

def decode_pdf417(image_path):
    """
    Decode PDF417 barcode from an image file
    
    Args:
        image_path (str): Path to the image file containing PDF417 barcode
        
    Returns:
        str: Decoded data from PDF417 or error message
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
        
        # Decode PDF417
        decoded_objects = pyzbar.decode(gray, symbols=[pyzbar.pyzbar.ZBarSymbol.PDF417])
        
        if not decoded_objects:
            return "No PDF417 barcode detected in the image"
            
        # Collect all decoded data
        results = []
        for obj in decoded_objects:
            results.append({
                'data': obj.data.decode('utf-8'),
                'type': obj.type,
                'rect': obj.rect,
                'polygon': obj.polygon
            })
            
        return results if len(results) > 1 else results[0]['data']
        
    except Exception as e:
        return f"Error decoding PDF417: {str(e)}"

if __name__ == "__main__":
    # Example usage
    image_path = input("Enter the path to the PDF417 image: ")
    result = decode_pdf417(image_path)
    print("Decoded data:", result)
