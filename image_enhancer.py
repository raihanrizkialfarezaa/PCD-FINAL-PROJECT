import os
import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from tqdm import tqdm

# --- 1. Precompute Lookup Table untuk Similarity Function ---
def precompute_similarity_lut(max_intensity=256, sigma_r=50):
    """Precompute similarity weights untuk efisiensi."""
    lut = np.zeros(max_intensity)
    for i in range(max_intensity):
        lut[i] = np.exp(-(i**2) / (2 * sigma_r**2))
    return lut

# --- 2. Implementasi Bilateral Filter Manual (Domain + Range) ---
def bilateral_filter(image, sigma_d=5, sigma_r=50, similarity_lut=None):
    img_array = np.array(image).astype(np.float32)
    
    # Menambahkan dimensi channel jika grayscale
    if len(img_array.shape) == 2:
        img_array = img_array[:, :, np.newaxis]
    
    h, w, c = img_array.shape
    result = np.zeros_like(img_array)
    
    # Kernel domain dan perhitungan bobot
    kernel_size = int(2 * np.ceil(3 * sigma_d)) + 1
    ax = np.arange(-kernel_size//2 + 1, kernel_size//2 + 1)
    xx, yy = np.meshgrid(ax, ax)
    domain_kernel = np.exp(-(xx**2 + yy**2) / (2 * sigma_d**2))
    domain_kernel /= np.sum(domain_kernel)

    # Menggunakan LUT jika tersedia
    if similarity_lut is None:
        similarity_lut = precompute_similarity_lut(256, sigma_r)

    # Memproses setiap pixel
    for y in range(h):
        for x in range(w):
            i_min = max(0, y - kernel_size//2)
            i_max = min(h, y + kernel_size//2 + 1)
            j_min = max(0, x - kernel_size//2)
            j_max = min(w, x + kernel_size//2 + 1)
            
            for ch in range(c):
                local_window = img_array[i_min:i_max, j_min:j_max, ch]
                center_val = img_array[y, x, ch]
                
                # Range weights (dari LUT)
                diff = np.abs(local_window.astype(int) - int(center_val))
                range_weights = similarity_lut[diff]
                
                # Combined weights
                combined_weights = domain_kernel[:i_max-i_min, :j_max-j_min] * range_weights
                normalized_weights = combined_weights / np.sum(combined_weights)
                
                # Konvolusi terboboti
                result[y, x, ch] = np.sum(local_window * normalized_weights)
    
    # Menghapus dimensi channel jika grayscale
    if c == 1:
        result = np.squeeze(result, axis=2)  # Menghapus dimensi ke-3
    
    return Image.fromarray(result.astype(np.uint8))

# --- 3. Dinamisasi Sigma Berdasarkan Histogram ---
def auto_sigma_r(image):
    """Hitung sigma_r dinamis berdasarkan standar deviasi histogram."""
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY) if len(image.shape) == 3 else image
    hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
    std = np.std(gray)
    return max(int(std), 10)  # Minimum 10 untuk noise reduction

# --- 4. Iterative Bilateral Filtering (Efek "Cartoon-Like") ---
def iterative_bilateral_filter(image, sigma_d=5, sigma_r=50, iterations=5):
    """Iterasi bilateral filter untuk efek flattening warna tanpa blur tepi."""
    result = image.copy()
    for _ in range(iterations):
        result = bilateral_filter(result, sigma_d, sigma_r)
    return result

# --- 5. Mengonversi ke CIE-Lab untuk Preservasi Persepsi Warna (RGB) ---
def enhance_color_image(image_path, output_path, sigma_d=5, iterations=1):
    # Membaca gambar
    img = cv2.imread(image_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Jika gambar grayscale, maka diproses langsung
    if len(img_rgb.shape) == 2 or img_rgb.shape[2] == 1:
        l = img_rgb  # Jika sudah grayscale, gunakan langsung
        l_filtered = bilateral_filter(Image.fromarray(l), sigma_d=5, sigma_r=auto_sigma_r(l))
        
        # Memastikan bahwa hasil adalah grayscale 2D
        result = np.array(l_filtered)  # shape = (h, w)
    else:
        # Gambar warna: Konversi ke CIE-Lab
        lab = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2Lab)
        l, a, b = cv2.split(lab)
        
        # Dinamisasi sigma_r berdasarkan histogram
        sigma_r = auto_sigma_r(l)
        
        # Filter channel Luminance (L)
        l_filtered = bilateral_filter(Image.fromarray(l), sigma_d=5, sigma_r=sigma_r)
        
        # Iterasi jika diperlukan
        if iterations > 1:
            l_filtered = iterative_bilateral_filter(l_filtered, sigma_d=5, sigma_r=sigma_r, iterations=iterations)
        
        # Menggabungkan kembali channel
        enhanced_lab = cv2.merge([np.array(l_filtered), a, b])
        result = cv2.cvtColor(enhanced_lab, cv2.COLOR_Lab2RGB)
    
    # Memastikan bahwa hasil grayscale adalah 2D sebelum menyimpan
    if len(result.shape) == 3 and result.shape[2] == 1:
        result = np.squeeze(result, axis=2)  # Hapus dimensi ke-3
    
    # Menyimpan hasil
    Image.fromarray(result).save(output_path, "JPEG", quality=95, optimize=True)

# --- 6. Analisis Histogram untuk Validasi ---
def analyze_histogram(input_path, output_path):
    """Plot histogram sebelum dan sesudah filtering untuk validasi."""
    img_input = np.array(Image.open(input_path))
    img_output = np.array(Image.open(output_path))
    
    plt.figure(figsize=(12, 5))
    for i, title in enumerate(['Input', 'Output']):
        plt.subplot(1, 2, i+1)
        for ch, col in enumerate(['r', 'g', 'b']):
            plt.hist(img_output[..., ch].ravel(), bins=256, alpha=0.5, color=col)
        plt.title(title)
    plt.tight_layout()
    plt.savefig("histogram_comparison.png")

# --- 7. Pipeline Pemrosesan Direktori ---
def process_directory(input_dir, output_dir):
    """Proses semua gambar dalam direktori dengan bilateral filter."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    valid_extensions = [".jpg", ".jpeg", ".png", ".bmp", ".tiff"]
    for filename in tqdm(os.listdir(input_dir), desc="Processing Images"):
        ext = os.path.splitext(filename)[1].lower()
        if ext in valid_extensions:
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, os.path.splitext(filename)[0] + ".jpg")
            
            # Memproses gambar berwarna (RGB)
            enhance_color_image(input_path, output_path)
            
            # Melakukan analisis histogram (opsional)
            analyze_histogram(input_path, output_path)

# Main untuk menjalankan program
if __name__ == "__main__":
    process_directory(
        input_dir=r"B:\app\PCD\FINAL PROJECT\image_enhancements\input",
        output_dir=r"B:\app\PCD\FINAL PROJECT\image_enhancements\output"
    )