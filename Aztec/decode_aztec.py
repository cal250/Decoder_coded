import os
import zxing

def decode_aztec(image_path):
    """Decode Aztec code from an image file using ZXing"""
    try:
        # Initialize ZXing barcode reader
        reader = zxing.BarCodeReader()
        
        # Try to read the barcode
        barcode = reader.decode(image_path)
        
        if barcode and barcode.parsed:
            return {
                'data': barcode.parsed,
                'format': barcode.format,
                'points': barcode.points
            }
        else:
            return {'error': 'No Aztec code detected in the image'}
            
    except Exception as e:
        return {'error': f'Error decoding Aztec code: {str(e)}'}

def print_result(result):
    """Print the decoding result in a user-friendly format"""
    if 'error' in result:
        print(f"\nError: {result['error']}")
    else:
        print("\nDecoded Aztec Code:")
        print(f"  Data: {result.get('data', 'N/A')}")
        print(f"  Format: {result.get('format', 'N/A')}")
        print(f"  Points: {result.get('points', 'N/A')}")

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
        result = decode_aztec(image_path)
        print_result(result)