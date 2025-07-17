import os
import subprocess
import time
from nanonets import NANONETSOCR
from dotenv import load_dotenv
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pyperclip import copy

ss_path = r"C:\Users\akhil\OneDrive\Pictures\Screenshots"

class _ScreenshotHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()
        self.new_image = None

    def on_created(self, event):
        if event.is_directory:
            return
        f = os.path.basename(event.src_path)
        image_extensions = {'.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff'}
        if any(f.lower().endswith(ext) for ext in image_extensions):
            self.new_image = event.src_path

def wait_for_new_screenshot(directory, timeout=30):
    if not os.path.exists(directory):
        return None

    handler = _ScreenshotHandler()
    observer = Observer()
    observer.schedule(handler, directory, recursive=False)
    observer.start()

    try:
        start = time.time()
        while time.time() - start < timeout and handler.new_image is None:
            time.sleep(0.1)
    finally:
        observer.stop()
        observer.join()

    if handler.new_image is None:
        print("Timeout: No new screenshot detected")
    return handler.new_image

def OCR(image_path):
    load_dotenv()
    model = NANONETSOCR()
    API_KEY = os.getenv('API_KEY')
    model.set_token(API_KEY)
    string = model.convert_to_string(image_path)
    return string

def snip_and_ocr():
    screenshots_dir = ss_path
    
    if not os.path.exists(screenshots_dir):
        print(f"Screenshots directory does not exist: {screenshots_dir}")
        return None
    
    print("Waiting for new screenshot...")
    try:
        subprocess.run('start ms-screenclip:', shell=True, check=True)
    except subprocess.CalledProcessError:
        print("Failed to open snipping tool.")
        return None
    
    new_screenshot = wait_for_new_screenshot(screenshots_dir)
    
    if new_screenshot is None:
        print("No new screenshot detected.")
        return None
    
    print(f"New screenshot detected: {new_screenshot}")
    time.sleep(1)
    
    try:
        print("Performing OCR...")
        text = OCR(new_screenshot)
        os.remove(new_screenshot)
        print(f"Screenshot deleted: {new_screenshot}")
        return text
    except Exception as e:
        print(f"Error processing screenshot: {e}")
        
        try:
            os.remove(new_screenshot)
            print(f"Screenshot deleted after error: {new_screenshot}")
        except:
            print(f"Could not delete screenshot file: {new_screenshot}")
        return None

if __name__ == "__main__":
    print('Lanching in 3 seconds...')
    time.sleep(3)
    try:
        result = snip_and_ocr()
        copy(result)
        print('Result copied to clipboard')
    except:
        print("No text recognized or operation cancelled")