import cv2
import numpy as np
import os
from barcode import get_barcode_class
from barcode.writer import ImageWriter
from PIL import Image, ImageEnhance

def preprocess_image(image_path):
    """Preprocess the image for better barcode detection"""
    try:
        # Read image
        img = cv2.imread(image_path)
        if img is None:
            return None, "Could not read the image file"
            
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Apply adaptive thresholding
        thresh = cv2.adaptiveThreshold(
            gray, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 11, 2
        )
        
        return thresh, None
    except Exception as e:
        return None, f"Error preprocessing image: {str(e)}"

def decode_maxicode(image_path):
    """
    Decode MaxiCode from an image file
    
    Args:
        image_path (str): Path to the image file containing MaxiCode
        
    Returns:
        dict: Decoded data from MaxiCode or error message
    """
    if not os.path.exists(image_path):
        return {"error": f"File not found - {image_path}"}
    
    try:
        # Preprocess the image
        processed_img, error = preprocess_image(image_path)
        if error:
            return {"error": error}
        
        # Save the processed image temporarily
        temp_path = "temp_processed.png"
        cv2.imwrite(temp_path, processed_img)
        
        # Try to read the barcode using python-barcode
        # Note: python-barcode's support for MaxiCode is limited
        try:
            # Try to read as MaxiCode (if supported)
            maxicode_reader = get_barcode_class('maxicode')
            with open(temp_path, 'rb') as f:
                maxicode = maxicode_reader(f)
            
            # If we get here, decoding was successful
            result = {
                "status": "success",
                "data": str(maxicode),
                "type": "MaxiCode"
            }
            
        except Exception as e:
            # Fallback to basic image processing if MaxiCode decoding fails
            img = cv2.imread(image_path)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Try to find the MaxiCode pattern (concentric circles)
            circles = cv2.HoughCircles(
                gray, cv2.HOUGH_GRADIENT, dp=1, minDist=20,
                param1=50, param2=30, minRadius=10, maxRadius=100
            )
            
            if circles is not None:
                circles = np.uint16(np.around(circles))
                result = {
                    "status": "MaxiCode pattern detected but could not decode",
                    "circles_found": len(circles[0, :]),
                    "note": "Full MaxiCode decoding requires specialized libraries"
                }
            else:
                result = {
                    "status": "error",
                    "message": "No MaxiCode pattern detected",
                    "note": "Try using a clearer image or a different barcode format"
                }
        
        # Clean up temporary file
        if os.path.exists(temp_path):
            os.remove(temp_path)
            
        return result
        
    except Exception as e:
        return {"error": f"Error decoding MaxiCode: {str(e)}"}

if __name__ == "__main__":
    # Example usage
    import sys
    
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
    else:
        # Look for any image in the current directory
        image_files = [f for f in os.listdir('.') 
                      if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))]
        
        if not image_files:
            print("No image files found in the current directory.")
            image_path = input("Enter the path to the MaxiCode image: ")
        else:
            print("Found the following image files:")
            for i, f in enumerate(image_files, 1):
                print(f"{i}. {f}")
            
            try:
                choice = int(input("Enter the number of the image to decode (or 0 to enter a custom path): "))
                if choice == 0:
                    image_path = input("Enter the path to the MaxiCode image: ")
                else:
                    image_path = image_files[choice - 1]
            except (ValueError, IndexError):
                print("Invalid selection. Using the first image by default.")
                image_path = image_files[0]
    
    print(f"\nProcessing image: {image_path}")
    result = decode_maxicode(image_path)
    print("\nDecoded data:")
    for key, value in result.items():
        print(f"{key}: {value}")
