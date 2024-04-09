import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw, ImageFont
import requests

# SentiSight.ai API credentials and project details
token = "sd0rpskicmbccuqhgbds4k3mgv"
project_id = "60985"
model = "object-detection-model-2"

# API endpoint and headers
api_url = 'https://platform.sentisight.ai/api/predict/{}/{}/'.format(project_id, model)
headers = {"X-Auth-token": token, "Content-Type": "application/octet-stream"}

# Define colors for each label (adjust as needed)
label_colors = {
    "Apple": "blue",
    "Banana": "GreenYellow",
    "Orange": "red"
}

# Define font size for labels (adjust as needed)
font_size = 15

# Define the maximum width and height for displaying images
max_image_width = 800
max_image_height = 600

def classify_image():
    global image_filename
    if image_filename:
        with open(image_filename, 'rb') as handle:
            # Send image data to SentiSight.ai API for classification
            r = requests.post(api_url, headers=headers, data=handle)
        
        if r.status_code == 200:
            json_response = r.json()
            img = Image.open(image_filename)
            draw = ImageDraw.Draw(img)
            
            for prediction in json_response:
                label = prediction["label"]
                score = prediction["score"]
                x0, y0, x1, y1 = prediction["x0"], prediction["y0"], prediction["x1"], prediction["y1"]
                color = label_colors.get(label, "red")  # Default to red if label not found
                
                # Load font
                font = ImageFont.truetype("arial.ttf", font_size)
                
                draw.rectangle([(x0, y0), (x1, y1)], outline=color, width=1)
                draw.text((x0 + 10, y0 + 3), f"{label}", fill=color, font=font)
                draw.text((x1 - 185, y1 - 35), f"Score: {score:.1f}%", fill=color, font=font)
                
            # Resize image to fit within the maximum width and height while maintaining aspect ratio
            img.thumbnail((max_image_width, max_image_height))
            
            img = ImageTk.PhotoImage(img)
            panel.configure(image=img)
            panel.image = img  # Keep a reference to the image to prevent garbage collection
        else:
            result_label.config(text='Error occurred with REST API.\nStatus code: {}\nError message: {}'.format(r.status_code, r.text))
    else:
        result_label.config(text='Please select an image first.')

def browse_image():
    global image_filename
    image_filename = filedialog.askopenfilename()
    if image_filename:
        image = Image.open(image_filename)
        # Resize image to fit within the maximum width and height while maintaining aspect ratio
        image.thumbnail((max_image_width, max_image_height))
        photo = ImageTk.PhotoImage(image)
        panel.configure(image=photo)
        panel.image = photo  # Keep a reference to the image to prevent garbage collection
        result_label.config(text='Image selected: {}'.format(image_filename))
        root.geometry(f"{image.width}x{image.height}")
    else:
        result_label.config(text='No image selected.')

# Create main window
root = tk.Tk()
root.title("Image Classifier")

# Calculate screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set window size to occupy approximately 80% of the screen
window_width = int(screen_width * 0.8)
window_height = int(screen_height * 0.8)
root.geometry(f"{window_width}x{window_height}")

# Create widgets
browse_button = tk.Button(root, text="Select image to upload", command=browse_image)
classify_button = tk.Button(root, text="Detect objects", command=classify_image)
panel = tk.Label(root)
result_label = tk.Label(root, text="")

# Layout widgets
browse_button.pack(pady=10)
classify_button.pack(pady=5)
panel.pack(padx=10, pady=10, fill="both", expand=True)  # Expand to fill available space
result_label.pack()

# Run the application
root.mainloop()
