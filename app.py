import os
import cv2
from flask import Flask, render_template, request
from flask import send_from_directory
from werkzeug.utils import secure_filename


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory('uploads', filename)




@app.route('/', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return render_template('index.html', message='No file part')

    file = request.files['file']

    if file.filename == '':
        return render_template('index.html', message='No selected file')

    # Secure the filename before saving
    filename = secure_filename(file.filename)
    file_path = os.path.join('uploads', filename)
    file.save(file_path)

    # Read the image using OpenCV
    img = cv2.imread(file_path)

    # Blur the background
    blurred_img = cv2.GaussianBlur(img, (15, 15), 0)

    # Save the resized images
    resized_file_path = os.path.join('uploads', 'resized_' + filename)
    cv2.imwrite(resized_file_path, cv2.resize(img, (400, 300)))

    resized_blurred_file_path = os.path.join('uploads', 'resized_blurred_' + filename)
    cv2.imwrite(resized_blurred_file_path, cv2.resize(blurred_img, (400, 300)))

    print(f"Resized Original Image Path: {resized_file_path}")
    print(f"Resized Blurred Image Path: {resized_blurred_file_path}")

    return render_template('index.html',
                           message='File uploaded successfully',
                           resized_image=f"resized_{filename}",
                           resized_blurred_image=f"resized_blurred_{filename}")





if __name__ == '__main__':
    app.run(debug=True)

