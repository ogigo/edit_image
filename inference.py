import cv2
import numpy as np

def blur_background(image_path, model_path):
    # Load pre-trained model for foreground segmentation
    net = cv2.dnn.readNetFromModelOptimizer(model=model_path)

    # Read the image
    image = cv2.imread(image_path)

    # Create a mask for foreground segmentation
    blob = cv2.dnn.blobFromImage(image, 1/255.0, (320, 320), swapRB=True, crop=False)
    net.setInput(blob)
    output = net.forward()
    mask = output[0, 0, :, :]

    # Resize mask to match image dimensions
    mask = cv2.resize(mask, (image.shape[1], image.shape[0]))

    # Convert mask to binary
    mask = (mask > 0.5).astype(np.uint8)

    # Apply Gaussian blur to the background
    blurred_image = cv2.GaussianBlur(image, (25, 25), 0)

    # Replace background with blurred image using the mask
    result = image.copy()
    result[mask == 0] = blurred_image[mask == 0]

    return result

if __name__=="__main__":
    image_path = 'example_image.jpg'
    model_path = 'pretrained_model.xml'  # Path to the pre-trained model for foreground segmentation
    result_image = blur_background(image_path, model_path)
    cv2.imshow('Blurred Background', result_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
