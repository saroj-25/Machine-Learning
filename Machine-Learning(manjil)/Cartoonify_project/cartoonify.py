# import cv2
# import numpy as np

# def color_quantization(img, k=12):
#     """Reduce number of colors using K-Means clustering (anime style)."""
#     data = np.float32(img).reshape((-1, 3))

#     # define criteria, number of clusters(K) and apply kmeans()
#     criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 0.001)
#     ret, label, center = cv2.kmeans(
#         data, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS
#     )

#     center = np.uint8(center)
#     result = center[label.flatten()]
#     result = result.reshape(img.shape)
#     return result


# def cartoonify_image(img_path, output_path):
#     # Read the image
#     img = cv2.imread(img_path)
#     img = cv2.resize(img, (600, 600))

#     # Step 1: Apply color quantization
#     quantized = color_quantization(img, k=12)

#     # Step 2: Detect edges
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     gray = cv2.medianBlur(gray, 5)
#     edges = cv2.adaptiveThreshold(
#         gray, 255,
#         cv2.ADAPTIVE_THRESH_MEAN_C,
#         cv2.THRESH_BINARY,
#         9, 9
#     )

#     # Step 3: Combine quantized colors with edges
#     cartoon = cv2.bitwise_and(quantized, quantized, mask=edges)

#     # Step 4: Smooth with bilateral filter
#     cartoon = cv2.bilateralFilter(cartoon, d=9, sigmaColor=200, sigmaSpace=200)

#     # Step 5: Boost saturation for Ghibli-like colors
#     hsv = cv2.cvtColor(cartoon, cv2.COLOR_BGR2HSV)
#     hsv[..., 1] = cv2.multiply(hsv[..., 1], 1.3)  # boost saturation
#     cartoon = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

#     # Save cartoonified image
#     cv2.imwrite(output_path, cartoon)

#     return output_path











import cv2
import numpy as np

def color_quantization(img, k=12):
    """Reduce number of colors using K-Means clustering with improved parameters."""
    data = np.float32(img).reshape((-1, 3))
    
    # More iterations for better color clustering
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 50, 0.001)
    ret, label, center = cv2.kmeans(
        data, k, None, criteria, 10, cv2.KMEANS_PP_CENTERS
    )
    
    center = np.uint8(center)
    result = center[label.flatten()]
    result = result.reshape(img.shape)
    return result

def enhance_edges(img):
    """Enhanced edge detection for more cartoon-like appearance."""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Reduce noise while preserving edges better
    gray = cv2.bilateralFilter(gray, 9, 75, 75)
    
    # Detect edges with multiple methods and combine
    edges1 = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY, 9, 9
    )
    
    edges2 = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 11, 7
    )
    
    # Combine edge detections
    edges = cv2.bitwise_and(edges1, edges2)
    
    # Morphological operations to clean up edges
    kernel = np.ones((1, 1), np.uint8)
    edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
    
    return edges

def adjust_color_profile(img):
    """Adjust colors to mimic Ghibli's vibrant palette."""
    # Convert to LAB color space for better color manipulation
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    
    # Split LAB channels
    l, a, b = cv2.split(lab)
    
    # Apply CLAHE to L channel for better contrast
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    l = clahe.apply(l)
    
    # Increase color saturation in A and B channels
    a = cv2.multiply(a, 1.2)
    b = cv2.multiply(b, 1.1)
    
    # Merge channels back
    lab = cv2.merge((l, a, b))
    
    # Convert back to BGR
    enhanced = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
    
    # Additional saturation boost in HSV space
    hsv = cv2.cvtColor(enhanced, cv2.COLOR_BGR2HSV)
    hsv[:, :, 1] = cv2.multiply(hsv[:, :, 1], 1.5)  # Boost saturation more
    hsv[:, :, 1] = np.clip(hsv[:, :, 1], 0, 255)  # Ensure within valid range
    enhanced = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    
    return enhanced

def add_ghibli_glow(img):
    """Add a soft glow effect common in Ghibli artwork."""
    # Create a blurred version for glow
    glow = cv2.bilateralFilter(img, d=15, sigmaColor=40, sigmaSpace=40)
    
    # Blend original with glow
    result = cv2.addWeighted(img, 0.7, glow, 0.3, 0)
    return result

def cartoonify_image(img_path, output_path):
    # Read the image
    img = cv2.imread(img_path)
    if img is None:
        raise ValueError("Could not load image from path: " + img_path)
        
    # Resize for consistent processing
    img = cv2.resize(img, (600, 600))
    
    # Step 1: Enhance colors before quantization
    img = adjust_color_profile(img)
    
    # Step 2: Apply color quantization with more colors for smoother gradients
    quantized = color_quantization(img, k=16)
    
    # Step 3: Apply bilateral filter multiple times for smoother surfaces
    for _ in range(2):
        quantized = cv2.bilateralFilter(quantized, d=9, sigmaColor=12, sigmaSpace=12)
    
    # Step 4: Detect enhanced edges
    edges = enhance_edges(img)
    
    # Invert edges to use as mask (we want to keep areas without edges)
    edges_inv = cv2.bitwise_not(edges)
    
    # Step 5: Combine quantized colors with edges
    # First, create a version with solid colors only (no edges)
    color_only = cv2.bitwise_and(quantized, quantized, mask=edges_inv)
    
    # Then create a version with just the edges (black with white edges)
    edge_art = cv2.merge([edges, edges, edges])
    
    # Combine by adding (edges will appear on top of the color)
    cartoon = cv2.add(color_only, edge_art)
    
    # Step 6: Add Ghibli-style glow
    cartoon = add_ghibli_glow(cartoon)
    
    # Step 7: Final color adjustment
    cartoon = adjust_color_profile(cartoon)
    
    # Save cartoonified image
    cv2.imwrite(output_path, cartoon)
    
    return output_path

# Example usage
if __name__ == "__main__":
    input_image = "input.jpg"
    output_image = "ghibli_cartoon_output.jpg"
    
    try:
        result_path = cartoonify_image(input_image, output_image)
        print(f"Cartoonified image saved to: {result_path}")
    except Exception as e:
        print(f"Error: {e}")