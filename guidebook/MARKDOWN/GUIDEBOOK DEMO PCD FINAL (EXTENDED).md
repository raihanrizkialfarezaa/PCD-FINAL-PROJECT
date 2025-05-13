

# **Analisis Teoritis dan Matematis Kode Program Bilateral Filter dengan Korelasi ke Jurnal dan Materi Kuliah (Grayscale)**


## **1. Konsep Dasar Bilateral Filter**

### **1.1 Definisi dan Tujuan**

**Bilateral Filter** adalah teknik penghalusan citra yang bertujuan untuk:

- Mengurangi **noise** tanpa mengaburkan **tepi (edges)**.

- Mempertahankan **warna alami** pada gambar berwarna melalui ruang warna **CIE-Lab**.

### **1.2 Persamaan Matematis**
Dari jurnal ICCV 1998, persamaan bilateral filter adalah:

$$
h(x) = \frac{1}{k(x)} \int\int f(\xi) \cdot c(\xi, x) \cdot s(f(\xi), f(x)) \, d\xi
$$

Dimana:
- $h(x)$: Nilai pixel hasil filter di lokasi $x$.

- $f(\xi)$: Nilai pixel tetangga di lokasi $\xi$.

- $c(\xi, x)$: Fungsi kedekatan spasial (domain kernel).

- $s(f(\xi), f(x))$: Fungsi kesamaan intensitas/warna (range kernel).

- $k(x)$: Faktor normalisasi untuk memastikan bobot jumlahnya 1.

---

## **2. Implementasi Kode Program**

### **2.1 Struktur Kode Utama**

Kode program mencakup:
1. **Precompute Similarity LUT**: Optimasi perhitungan kesamaan intensitas.

2. **Bilateral Filter Manual**: Menghitung nilai pixel baru dengan kombinasi domain dan range.

3. **Dinamisasi Sigma_r**: Penyesuaian parameter berdasarkan histogram.

4. **Iterative Filtering**: Peningkatan efek "cartoon-like".

5. **Konversi ke CIE-Lab**: Preservasi warna perceptual.


### **2.2 Contoh Perhitungan Matematis**

#### **Langkah 1: Domain Kernel (Gaussian)**
Untuk domain kernel, kita menggunakan fungsi Gaussian:
$$
c(\xi, x) = e^{-\frac{d^2}{2\sigma_d^2}}
$$

Dimana $d$ adalah jarak Euclidean antara lokasi pixel $\xi$ dan $x$.

**Contoh Numerik**:
Misal $\sigma_d = 2$, dan kernel size $3 \times 3$:
```python
ax = [-1, 0, 1]  # Koordinat relatif dari pixel tengah
xx, yy = np.meshgrid(ax, ax)  # Membuat grid 3x3
d = np.sqrt(xx**2 + yy**2)
domain_kernel = np.exp(-d**2 / (2 * sigma_d**2))
```
Hasil domain_kernel:
```
[[0.3679 0.6065 0.3679]
 [0.6065 1.0000 0.6065]
 [0.3679 0.6065 0.3679]]
```

#### **Langkah 2: Range Kernel (Similarity Function)**
Fungsi kesamaan intensitas:
$$
s(f(\xi), f(x)) = e^{-\frac{(f(\xi) - f(x))^2}{2\sigma_r^2}}
$$

**Contoh Numerik**:
Jika $f(x) = 100$, $f(\xi) = [90, 100, 110]$, dan $\sigma_r = 10$:

```python
diff = np.array([10, 0, 10])
range_weights = np.exp(-diff**2 / (2 * sigma_r**2))
```
Hasil range_weights:
```
[0.6065, 1.0000, 0.6065]
```

#### **Langkah 3: Gabungan Domain dan Range**
Kombinasi bobot:
$$
w(\xi, x) = c(\xi, x) \cdot s(f(\xi), f(x))
$$

**Contoh Numerik**:
Dengan domain_kernel dan range_weights di atas:
```python
combined_weights = domain_kernel * range_weights
```
Hasil combined_weights:
```
[[0.2231 0.6065 0.2231]
 [0.3679 1.0000 0.3679]
 [0.2231 0.6065 0.2231]]
```

#### **Langkah 4: Normalisasi dan Hasil Akhir**
Normalisasi:
$$
k(x) = \sum_{\xi} w(\xi, x)
$$

$$
h(x) = \frac{\sum_{\xi} f(\xi) \cdot w(\xi, x)}{k(x)}
$$

**Contoh Numerik**:
Jika $f(\xi) = [90, 100, 110]$ dan bobot combined_weights = [0.6, 1.0, 0.6]:

```python
k_x = np.sum(combined_weights)
h_x = np.sum(f_xi * combined_weights) / k_x
```
Hasil:
- $k(x) = 3.2231$

- $h(x) = \frac{(90 \cdot 0.6) + (100 \cdot 1.0) + (110 \cdot 0.6)}{3.2231} = 100$

---

## **3. Korelasi dengan Materi Kuliah**

### **3.1 Domain Spasial (Spatial Domain)**
Dari materi kuliah:
- Operasi langsung pada pixel citra: $g(x,y) = T[f(x,y)]$.

- Termasuk **point processing** (transformasi intensitas) dan **mask processing** (filtering dengan kernel).

**Korelasi dengan Kode**:
- **Mask Processing**: Kode menggunakan kernel domain (spasial) dan range (intensitas) untuk menghitung nilai pixel baru.

- **Point Processing**: Dinamisasi `sigma_r` berdasarkan histogram (fungsi `auto_sigma_r`).

### **3.2 Histogram dan Point Processing**
Dari materi kuliah:
- Histogram digunakan untuk analisis distribusi intensitas.

- Transformasi intensitas seperti contrast stretching dan log transformation.

**Korelasi dengan Kode**:
- Fungsi `auto_sigma_r` menghitung standar deviasi histogram untuk menyesuaikan parameter filter.

- Analisis histogram (`analyze_histogram`) untuk validasi hasil filtering.

### **3.3 Edge Preservation**
Dari jurnal dan materi kuliah:
- Bilateral filter mempertahankan tepi dengan menggabungkan domain dan range filtering.

**Contoh Studi Kasus**:
- **Input**: Gambar dengan tepi tajam dan noise (misal: foto kucing dengan latar belakang buram).

- **Output**: Hasil bilateral filter mengurangi noise pada area datar (smooth region) tetapi mempertahankan tepi (contour kucing).

---

## **4. Penggunaan CIE-Lab untuk Gambar Warna**

### **4.1 Alasan Penggunaan CIE-Lab**
Dari jurnal:
- Ruang warna CIE-Lab mempertahankan persepsi warna manusia (perceptually meaningful).

- Filter hanya diterapkan pada channel Luminance (L) untuk preservasi warna alami.

### **4.2 Proses Konversi**

1. Konversi RGB ke CIE-Lab:
   ```python
   lab = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2Lab)
   ```
   
2. Pisahkan channel:
   ```python
   l, a, b = cv2.split(lab)
   ```
   
3. Terapkan bilateral filter hanya pada channel L:
   ```python
   l_filtered = bilateral_filter(Image.fromarray(l), sigma_d, sigma_r)
   ```
   
4. Gabung kembali channel:
   ```python
   enhanced_lab = cv2.merge([np.array(l_filtered), a, b])
   result = cv2.cvtColor(enhanced_lab, cv2.COLOR_Lab2RGB)
   ```
   

**Contoh Studi Kasus**:
- **Input**: Foto bunga dengan warna cerah.

- **Output**: Warna tetap alami meskipun telah dilakukan filtering untuk mengurangi noise.

---

## **5. Iterative Filtering untuk Efek "Cartoon-Like"**

### **5.1 Konsep**
Iterasi berturut-turut dari bilateral filter menghasilkan efek flattening warna tanpa mengaburkan tepi (seperti gambar kartun).

### **5.2 Proses Matematis**
Setiap iterasi:
```python
for _ in range(iterations):
    result = bilateral_filter(result, sigma_d, sigma_r)
```

**Contoh Studi Kasus**:
- **Input**: Foto alam (pegunungan).

- **Output**: Setelah 5 iterasi, warna menjadi lebih flat (monoton) tetapi tepi tetap tajam.

---

## **6. Validasi dengan Histogram**

### **6.1 Analisis Histogram**
Fungsi `analyze_histogram` membandingkan distribusi intensitas sebelum dan sesudah filtering.

**Contoh Output**:
- Histogram input: Distribusi intensitas lebar (ada noise).

- Histogram output: Distribusi lebih sempit (noise berkurang).

### **6.2 Korelasi dengan Materi Kuliah**
Dari materi kuliah:
- Histogram equalization dan contrast stretching digunakan untuk meningkatkan kontras.


**Korelasi dengan Kode**:
- Dinamisasi `sigma_r` berdasarkan histogram mirip dengan contrast stretching adaptif.

---

## **7. Kesimpulan**

### **7.1 Aspek Teoritis**
- Kode program mengimplementasikan **bilateral filter** sesuai jurnal ICCV 1998 dengan:

  - Kombinasi **domain** (spasial) dan **range** (intensitas/warna).

  - Penggunaan **CIE-Lab** untuk preservasi warna perceptual.

  - Dinamisasi parameter berdasarkan histogram.

### **7.2 Aspek Matematis**
- Persamaan integral bilinear diubah menjadi operasi diskret dengan kernel Gaussian.

- Normalisasi bobot memastikan konsistensi hasil.

### **7.3 Relevansi dengan Materi Kuliah**
- Sesuai dengan konsep **spatial domain filtering** dan **point processing**.

- Mengintegrasikan **histogram analysis** untuk optimasi parameter.

- Memenuhi tujuan **peningkatan kualitas citra** dengan preservasi tepi dan pengurangan noise.

---


### **8. Studi Kasus Sederhana: Penerapan Bilateral Filter pada Citra Grayscale dengan Noise**

Berikut adalah **analisis langkah-demi-langkah** penerapan **Bilateral Filter** pada **citra grayscale dengan noise**, dilengkapi dengan **perhitungan matematis manual** dan **korelasi ke teori**. Studi kasus ini menggunakan **matriks 3×3** sebagai input dan menjelaskan proses penghalusan pada **pixel tengah** (koordinat $x = (1,1)$) dengan nilai intensitas $f(x) = 100$. 

---

## **Input Citra**
Diberikan citra grayscale berikut (nilai intensitas 0–255):
```
[90, 100, 110]
[80, 100, 120]
[70, 100, 130]
```
**Tujuan**: Menghitung nilai pixel tengah $x = (1,1)$ setelah diterapkan Bilateral Filter dengan parameter:
- $\sigma_d = 2$ (domain kernel).
- $\sigma_r = 10$ (range kernel).

---

## **Langkah 1: Domain Kernel (Spasial)**

### **1.1 Definisi**
Domain kernel mengukur kedekatan spasial antara pixel tengah ($x$) dan tetangganya ($\xi$) menggunakan fungsi Gaussian:

$$
c(\xi, x) = e^{-\frac{d^2}{2\sigma_d^2}}
$$
Di mana $d$ adalah jarak Euclidean antara lokasi pixel.

### **1.2 Perhitungan Manual**
Untuk kernel size $3 \times 3$, kita definisikan grid koordinat relatif ($\xi - x$):
```
Koordinat relatif:
xx = [[-1, 0, 1],
      [-1, 0, 1],
      [-1, 0, 1]]
yy = [[-1, -1, -1],
      [0, 0, 0],
      [1, 1, 1]]
```

**Jarak Euclidean $(d)$**:
$$
d = \sqrt{xx^2 + yy^2}
$$
Hasil $d$:
```
[[1.414, 1.0, 1.414],
 [1.0, 0.0, 1.0],
 [1.414, 1.0, 1.414]]
```

**Domain Kernel ($c(\xi, x)$)**:
$$
c(\xi, x) = e^{-\frac{d^2}{2\sigma_d^2}} \quad (\sigma_d = 2)
$$

Hitung untuk setiap posisi:
1. $d = 1.414$:
   $$
   c = e^{-\frac{(1.414)^2}{2 \cdot 2^2}} = e^{-\frac{2}{8}} = e^{-0.25} \approx 0.7788
   $$
   
2. $d = 1.0$:
   $$
   c = e^{-\frac{1^2}{2 \cdot 2^2}} = e^{-\frac{1}{8}} = e^{-0.125} \approx 0.8825
   $$
   
3. $d = 0.0$:
   $$
   c = e^{0} = 1.0
   $$

Hasil domain_kernel:
```
[[0.7788, 0.8825, 0.7788],
 [0.8825, 1.0000, 0.8825],
 [0.7788, 0.8825, 0.7788]]
```

### **1.3 Eksekusi Kode**
```python
def bilateral_filter(image, sigma_d=5, sigma_r=50, similarity_lut=None):
    # Konversi gambar ke array numpy
    img_array = np.array(image).astype(np.float32)
    
    # Jika grayscale (2D), tambahkan dimensi channel
    if len(img_array.shape) == 2:
        img_array = img_array[:, :, np.newaxis]
    
    h, w, c = img_array.shape  # Dimensi gambar
    result = np.zeros_like(img_array)  # Hasil filter
    
    # Kernel domain (Gaussian)
    kernel_size = int(2 * np.ceil(3 * sigma_d)) + 1
    ax = np.arange(-kernel_size//2 + 1, kernel_size//2 + 1)
    xx, yy = np.meshgrid(ax, ax)  # Membuat grid 3x3
    d = np.sqrt(xx**2 + yy**2)  # Jarak Euclidean
    domain_kernel = np.exp(-d**2 / (2 * sigma_d**2))  # Domain kernel
    domain_kernel /= np.sum(domain_kernel)  # Normalisasi
```


#### **PENJELASAN KODE:**

Fungsi ini menerapkan **Bilateral Filter**, yaitu teknik penghalusan gambar yang:

1. Mengurangi noise.

3. Mempertahankan tepi (edges) dengan mempertimbangkan **jarak spasial** dan **kesamaan intensitas**.

---

#### **Input Parameter**
```python
def bilateral_filter(image, sigma_d=5, sigma_r=50, similarity_lut=None):
```
- `image`: Gambar input (PIL Image atau array numpy).

- `sigma_d`: Standar deviasi untuk kernel domain (spasial).

- `sigma_r`: Standar deviasi untuk kernel range (intensitas).

- `similarity_lut`: Lookup Table (LUT) untuk kesamaan intensitas (optional).

---

#### **Langkah 1: Konversi Gambar ke Array Numpy**
```python
img_array = np.array(image).astype(np.float32)
```
- Gambar dikonversi ke array numpy dengan tipe `float32` untuk akurasi perhitungan.

- Jika gambar grayscale (2D), tambahkan dimensi channel:
  ```python
  if len(img_array.shape) == 2:
      img_array = img_array[:, :, np.newaxis]
  ```
  - Contoh: Dari bentuk `(h, w)` menjadi `(h, w, 1)`.

---

#### **Langkah 2: Inisialisasi Variabel**
```python
h, w, c = img_array.shape
result = np.zeros_like(img_array)
```
- `h`, `w`, `c`: Tinggi, lebar, dan jumlah channel gambar.

- `result`: Array kosong untuk menyimpan hasil filter.

---

#### **Langkah 3: Kernel Domain (Spasial)**
##### **a. Hitung Ukuran Kernel**
```python
kernel_size = int(2 * np.ceil(3 * sigma_d)) + 1
```
- **Penjelasan**:

  Latar Belakang Distribusi Gaussian:

	Fungsi Gaussian digunakan untuk menghitung **bobot 				spasial** dalam Bilateral Filter:

	c(ξ,x)=e−2σd2​d2​

-   **`sigma_d`** : Standar deviasi distribusi Gaussian.
-   **`d`** : Jarak Euclidean antara pixel tengah (x) dan tetangganya (ξ).

	Dalam distribusi normal:

-   **±1σ** : Mencakup ~68% data.

-   **±2σ** : Mencakup ~95% data.

-   **±3σ** : Mencakup ~99.7% data (dikenal sebagai **Aturan Empiris** atau **Three-Sigma Rule** ).

	Mengapa `3 * sigma_d`?

-   **Tujuan** : Memastikan kernel mencakup **99.7% bobot spasial** yang signifikan.

-   **Dampak** :

    -   Jika kernel terlalu kecil (misal: `1 * sigma_d`), sebagian besar bobot akan terpotong, menyebabkan **distorsi tepi** atau **penghalusan tidak lengkap** .
 
    -   Dengan `3 * sigma_d`, kernel cukup besar untuk menangkap hampir semua bobot yang berkontribusi pada proses penghalusan.

  - `np.ceil(...)`: Bulatkan ke atas agar ukuran kernel valid.

  - `2 * ... + 1`: Pastikan ukuran kernel ganjil (misal: 5x5, 7x7).
  
  ```python
 kernel_size = int(2 * np.ceil(3 * sigma_d)) + 1
```

-   **`np.ceil(3 * sigma_d)`** : Membulatkan ke atas agar ukuran kernel valid (misal: `sigma_d = 2` → `3 * sigma_d = 6` → `ceil(6) = 6`).

-   **`2 * ...`** : Menghitung radius ke dua sisi (kiri-kanan/atas-bawah).

-   **`+1`** : Menambahkan 1 untuk membuat ukuran kernel **ganjil** (misal: `2*6 +1 = 13` → kernel 13×13).

**Mengapa kernel harus ganjil?**

-   Memastikan ada **pixel tengah** yang jelas (misal: untuk kernel 3×3, titik tengah adalah `(1,1)`).

-   Memudahkan proses konvolusi karena posisi tengah dapat didefinisikan dengan tepat.

**Contoh Perhitungan**

Misal: `sigma_d = 2`

1.  **`3 * sigma_d`** → `6`.
2.  **`np.ceil(6)`** → `6`.
3.  **`2 * 6 + 1`** → `13` (kernel size 13×13).

**Artinya** :

-   Kernel akan mencakup semua bobot spasial dari jarak `-6` hingga `+6` dari pixel tengah.

-   Bobot di luar rentang ini diabaikan karena kontribusinya sangat kecil (<0.3%).

##### **b. Buat Grid Koordinat Relatif**
```python
ax = np.arange(-kernel_size//2 + 1, kernel_size//2 + 1)
xx, yy = np.meshgrid(ax, ax)
```

- **Contoh**:

  - Jika `kernel_size = 5`, maka `ax = [-2, -1, 0, 1, 2]`.

  - `xx` dan `yy` adalah matriks 5x5 yang merepresentasikan koordinat relatif terhadap pixel tengah.

##### **c. Hitung Jarak Euclidean**
```python
d = np.sqrt(xx**2 + yy**2)
```
Bagian ini menghitung **jarak Euclidean** antara setiap koordinat relatif dalam kernel dan titik tengah `(0,0)`. Ini adalah langkah krusial untuk menentukan **bobot spasial** (domain kernel) dalam Bilateral Filter.

**1. Bilateral Filter menggunakan dua jenis bobot:**

1. **Domain Kernel**: Bobot berbasis jarak spasial (spatial distance).

2. **Range Kernel**: Bobot berbasis kesamaan intensitas (intensity similarity).

**2. Apa itu `xx` dan `yy`?**

Dari kode sebelumnya:
```python
ax = [-1, 0, 1]  # Koordinat relatif untuk kernel 3x3
xx, yy = np.meshgrid(ax, ax)
```

- `xx` dan `yy` adalah matriks 3x3 yang merepresentasikan **koordinat relatif** dari pixel tengah `(0,0)`.

**Contoh Output**:
```python
xx = [[-1, 0, 1],
      [-1, 0, 1],
      [-1, 0, 1]]

yy = [[-1, -1, -1],
      [0, 0, 0],
      [1, 1, 1]]
```

- Setiap elemen `(i,j)` di `xx` dan `yy` merepresentasikan posisi relatif terhadap pixel tengah:

  - Contoh: `(xx[0,0], yy[0,0]) = (-1, -1)` → posisi kiri atas.

  - `(xx[1,1], yy[1,1]) = (0, 0)` → posisi tengah.

**3. Mengapa Perlu Jarak Euclidean?**
Domain kernel harus mengukur **seberapa jauh** setiap tetangga dari pixel tengah. Semakin jauh tetangga, semakin kecil bobotnya (karena efek Gaussian).

Rumus jarak Euclidean:
$$
d = \sqrt{x^2 + y^2}
$$
Di mana `(x, y)` adalah koordinat relatif dari pixel tengah.

**4. Perhitungan Manual untuk Kernel 3x3**

Hitung jarak untuk setiap koordinat `(xx[i,j], yy[i,j])`:

| Koordinat Relatif `(x,y)` | Jarak Euclidean $d$ |
|--------------------------|-----------------------|
| (-1, -1)                 | $\sqrt{(-1)^2 + (-1)^2} = \sqrt{2} \approx 1.414$ |
| (0, -1)                  | $\sqrt{0^2 + (-1)^2} = 1.0$ |
| (1, -1)                  | $\sqrt{1^2 + (-1)^2} = \sqrt{2} \approx 1.414$ |
| (-1, 0)                  | $\sqrt{(-1)^2 + 0^2} = 1.0$ |
| (0, 0)                   | $\sqrt{0^2 + 0^2} = 0.0$ |
| (1, 0)                   | $\sqrt{1^2 + 0^2} = 1.0$ |
| (-1, 1)                  | $\sqrt{(-1)^2 + 1^2} = \sqrt{2} \approx 1.414$ |
| (0, 1)                   | $\sqrt{0^2 + 1^2} = 1.0$ |
| (1, 1)                   | $\sqrt{1^2 + 1^2} = \sqrt{2} \approx 1.414$ |

**Hasil Akhir `d`**:
```python
d = [[1.414, 1.0, 1.414],
     [1.0, 0.0, 1.0],
     [1.414, 1.0, 1.414]]
```

##### **d. Kernel Domain (Gaussian)**
```python
domain_kernel = np.exp(-d**2 / (2 * sigma_d**2))
domain_kernel /= np.sum(domain_kernel)
```
- **Formula**:
  $$
  c(\xi, x) = e^{-\frac{d^2}{2\sigma_d^2}}
  $$
  
- **Normalisasi**:

  - Bagi setiap bobot dengan jumlah total bobot agar jumlahnya = 1.

---

#### **Contoh Perhitungan Manual dengan Program**
Misal `sigma_d = 2` dan kernel size `5x5`:

1. **Koordinat Relatif**:

   ```python
   ax = [-2, -1, 0, 1, 2]
   xx, yy = np.meshgrid(ax, ax)
   ```
   
   - Contoh nilai di `xx`: `[-2, -1, 0, 1, 2]` di baris pertama.

   - Contoh nilai di `yy`: `[-2, -2, -2, -2, -2]` di kolom pertama.

3. **Jarak Euclidean**:
   - Untuk koordinat `(1,1)`:  
     $$
     d = \sqrt{(1)^2 + (1)^2} = \sqrt{2} \approx 1.414
     $$

4. **Bobot Domain**:
   - Untuk `d = 1.414`:  
     $$
     c = e^{-\frac{(1.414)^2}{2 \cdot 2^2}} = e^{-\frac{2}{8}} = e^{-0.25} \approx 0.7788
     $$

5. **Normalisasi**:
   - Jumlah semua bobot dalam kernel dibagi dengan totalnya.


### **1.4 Korelasi dengan Teori**

- **Jurnal ICCV 1998**:  
  - Domain kernel sesuai Persamaan 5–6:  
    $$
    h(x) = \frac{1}{k(x)} \int\int f(\xi) \cdot c(\xi, x) \cdot s(f(\xi), f(x)) \, d\xi
    $$
    
  - Fungsi Gaussian untuk domain filtering (halaman 2.1).

- **Materi Kuliah**:  
  - Spatial domain filtering (Slide 5–6):  
    $g(x,y) = T[f(x,y)]$, di mana $T$ adalah operator berbasis kernel.

---

## **Langkah 2: Range Kernel (Intensitas/Warna)**

### **2.1 Definisi**
Range kernel mengukur kesamaan intensitas antara pixel tengah $f(x)$ dan tetangganya $f(\xi)$:

$$
s(f(\xi), f(x)) = e^{-\frac{(f(\xi) - f(x))^2}{2\sigma_r^2}}
$$

### **2.2 Perhitungan Manual**
Diketahui $f(x) = 100$ dan $\sigma_r = 10$. Hitung selisih intensitas ($\Delta f$) untuk setiap tetangga:
```
Δf = f(ξ) - f(x) = 
[[90-100, 100-100, 110-100] → [-10, 0, 10]
 [80-100, 100-100, 120-100] → [-20, 0, 20]
 [70-100, 100-100, 130-100]] → [-30, 0, 30]
```

**Range Weights $s(f(\xi), f(x))$**:

$$
s = e^{-\frac{(\Delta f)^2}{2\sigma_r^2}} \quad (\sigma_r = 10)
$$

Hitung untuk setiap $\Delta f$:
1. $\Delta f = -10$:
   $$
   s = e^{-\frac{(-10)^2}{2 \cdot 10^2}} = e^{-\frac{100}{200}} = e^{-0.5} \approx 0.6065
   $$
   
2. $\Delta f = 0$:
   $$
   s = e^{0} = 1.0000
   $$
   
3. $\Delta f = 10$:
   $$
   s = e^{-0.5} \approx 0.6065
   $$
   
4. $\Delta f = -20$:
   $$
   s = e^{-\frac{(-20)^2}{2 \cdot 10^2}} = e^{-\frac{400}{200}} = e^{-2} \approx 0.1353
   $$
   
5. $\Delta f = 20$:
   $$
   s = e^{-2} \approx 0.1353
   $$
   
6. $\Delta f = -30$:
   $$
   s = e^{-\frac{(-30)^2}{2 \cdot 10^2}} = e^{-\frac{900}{200}} = e^{-4.5} \approx 0.0111
   $$
   
7. $\Delta f = 30$:
   $$
   s = e^{-4.5} \approx 0.0111
   $$

Hasil range_weights:
```
[[0.6065, 1.0000, 0.6065],
 [0.1353, 1.0000, 0.1353],
 [0.0111, 1.0000, 0.0111]]
```

### **2.3 Eksekusi Kode**
```python
# Menggunakan LUT jika tersedia

if similarity_lut is  None:

similarity_lut =  precompute_similarity_lut(256, sigma_r)

  

# Memproses setiap pixel

for y in  range(h):

for x in  range(w):

i_min =  max(0, y - kernel_size//2)

i_max =  min(h, y + kernel_size//2  +  1)

j_min =  max(0, x - kernel_size//2)

j_max =  min(w, x + kernel_size//2  +  1)

for ch in  range(c):

local_window = img_array[i_min:i_max, j_min:j_max, ch]

center_val = img_array[y, x, ch]

# Range weights (dari LUT)

diff = np.abs(local_window.astype(int)  -  int(center_val))

range_weights = similarity_lut[diff]

# Combined weights

combined_weights = domain_kernel[:i_max-i_min,  :j_max-j_min]  * range_weights

normalized_weights = combined_weights / np.sum(combined_weights)

# Konvolusi terboboti

result[y, x, ch]  = np.sum(local_window * normalized_weights)

# Menghapus dimensi channel jika grayscale

if c ==  1:

result = np.squeeze(result,  axis=2)  # Menghapus dimensi ke-3

return Image.fromarray(result.astype(np.uint8))
```


#### **Penjelasan Kode dan Hubungannya dengan Studi Kasus Input**

Kode berikut adalah bagian inti dari fungsi `bilateral_filter`, yang mengimplementasikan **Bilateral Filter** pada gambar grayscale atau berwarna. Kita akan menghubungkan bagian kode ini dengan studi kasus input:

**Input Citra:**
```
[90, 100, 110]
[80, 100, 120]
[70, 100, 130]
```

**Parameter:**
- `sigma_d = 1.414` (domain kernel).
- `sigma_r = 10` (range kernel).
---

**1. Penggunaan LUT (Lookup Table) untuk Range Kernel**
```python
# Menggunakan LUT jika tersedia
if similarity_lut is None:
    similarity_lut = precompute_similarity_lut(256, sigma_r)
```

- **Fungsi `precompute_similarity_lut`**:

  - Membuat tabel bobot untuk intensitas 0–255 berdasarkan `sigma_r`.

  - Setiap indeks `i` diisi dengan rumus eksponensial:  

    $$
    \text{bobot} = e^{-\frac{i^2}{2\sigma_r^2}}
    $$
    
- **Tujuan**:
  - Menghindari perhitungan ulang fungsi eksponensial untuk setiap selisih intensitas.

  - **Contoh**: Jika `sigma_r = 10`, maka `similarity_lut[10]` akan menyimpan bobot untuk selisih intensitas 10.

**Hubungan dengan Studi Kasus:**
- Untuk `sigma_r = 10`, LUT akan digunakan untuk menghitung bobot range kernel pada selisih intensitas seperti `Δf = [-10, 0, 10]`.


**2. Proses Per Pixel**
```python
# Memproses setiap pixel
for y in range(h):
    for x in range(w):
        # Menentukan batas window
        i_min = max(0, y - kernel_size//2)
        i_max = min(h, y + kernel_size//2 + 1)
        j_min = max(0, x - kernel_size//2)
        j_max = min(w, x + kernel_size//2 + 1)
        
        for ch in range(c):
            # Ekstrak window lokal dan nilai tengah
            local_window = img_array[i_min:i_max, j_min:j_max, ch]
            center_val = img_array[y, x, ch]
            
            # Hitung selisih intensitas
            diff = np.abs(local_window.astype(int) - int(center_val))
            range_weights = similarity_lut[diff]
            
            # Gabung domain dan range kernel
            combined_weights = domain_kernel[:i_max-i_min, :j_max-j_min] * range_weights
            normalized_weights = combined_weights / np.sum(combined_weights)
            
            # Konvolusi terboboti
            result[y, x, ch] = np.sum(local_window * normalized_weights)
```

##### **a. Menentukan Window Lokal**

- **`kernel_size`**:

  - Dihitung dari `sigma_d` menggunakan rumus:  
    $$
    \text{kernel\_size} = 2 \cdot \text{ceil}(3\sigma_d) + 1
    $$
    
  - Untuk `sigma_d = 1.414`, `kernel_size = 3` (window 3×3).

- **`i_min`, `i_max`, `j_min`, `j_max`**:

  - Menentukan batas window lokal untuk menghindari indeks out-of-bounds.

**Hubungan dengan Studi Kasus:**
- Untuk pixel tengah `(y=1, x=1)`, window lokal adalah seluruh citra (3×3).

##### **b. Range Weights (Kesamaan Intensitas)**
- **`diff = np.abs(local_window - center_val)`**:

  - Hitung selisih intensitas antara pixel tengah dan tetangga.

  - Contoh: Jika `center_val = 100`, `local_window = [90, 100, 110; 80, 100, 120; 70, 100, 130]`, maka:
    ```
    diff = [[10, 0, 10],
            [20, 0, 20],
            [30, 0, 30]]
    ```

- **`range_weights = similarity_lut[diff]`**:

  - Ambil bobot dari LUT berdasarkan selisih intensitas.

  - Contoh: `diff = 10 → range_weights = similarity_lut[10] ≈ 0.6065`.

**Hubungan dengan Studi Kasus:**
- Range weights untuk `diff = 10, 20, 30` adalah:
  ```
  [[0.6065, 1.0000, 0.6065],
   [0.1353, 1.0000, 0.1353],
   [0.0111, 1.0000, 0.0111]]
  ```

#### **c. Domain Kernel (Jarak Spasial)**
- **`domain_kernel`**:

  - Telah dihitung sebelumnya sebagai matriks Gaussian 3×3:
    ```
    [[0.7788, 0.8825, 0.7788],
     [0.8825, 1.0000, 0.8825],
     [0.7788, 0.8825, 0.7788]]
    ```

#### **d. Gabungan Domain dan Range**
- **`combined_weights = domain_kernel * range_weights`**:

  - Perkalian elemen-demi-elemen antara domain dan range kernel.

  - Contoh hasil:
    ```
    [[0.472, 0.8825, 0.472 ],
     [0.119, 1.0000, 0.119 ],
     [0.0086, 0.8825, 0.0086]]
    ```

- **`normalized_weights`**:

  - Normalisasi bobot agar jumlahnya = 1:
    
    $$
    \mathrm{normalized\_weights} = \frac{\mathrm{combined\_weights}}{\sum \mathrm{combined\_weights}}
$$
    
  - Contoh:  
    $$
    k_x = 0.472 + 0.8825 + 0.472 + 0.119 + 1.0000 + 0.119 + 0.0086 + 0.8825 + 0.0086 \approx 3.9442
    $$
    
    $$
    \mathrm{normalized\_weights} = \frac{\mathrm{combined\_weights}}{3.9442}
$$

##### **e. Konvolusi Terboboti**

- **`result[y, x, ch] = np.sum(local_window * normalized_weights)`**:

  - Hitung nilai pixel hasil filter sebagai rata-rata tertimbang:

    $$
    h(x) = \frac{\sum_{\xi} f(\xi) \cdot w(\xi, x)}{k(x)}
    $$
    
  - **Contoh Perhitungan Manual**:
    - Kalikan intensitas tetangga dengan bobot gabungan:
      ```
      (90 × 0.472) + (100 × 0.8825) + (110 × 0.472) +
      (80 × 0.119) + (100 × 1.0000) + (120 × 0.119) +
      (70 × 0.0086) + (100 × 0.8825) + (130 × 0.0086)
      ```
    - Hasil:
      $$
      h(x) = \frac{182.65 + 123.80 + 89.97}{3.9442} \approx 100.5
      $$

**Hubungan dengan Studi Kasus:**
- Pixel tengah `(1,1)` tetap bernilai `100` karena tetangga dengan selisih besar (misal: `Δf = 30`) diabaikan (bobot kecil: `≈ 0.0086`).

**3. Pemrosesan Grayscale vs Warna**
```python
# Menghapus dimensi channel jika grayscale
if c == 1:
    result = np.squeeze(result, axis=2)
```
- **Grayscale**: Hasil filter adalah array 2D.

- **Berwarna (RGB)**: Proses dilakukan per channel (R, G, B).

**Hubungan dengan Studi Kasus:**

- Karena input adalah grayscale, hasil akhir adalah array 2D dengan dimensi `(h, w)`.

**4. Visualisasi Proses**
```
Input Citra:
[90, 100, 110]
[80, 100, 120]
[70, 100, 130]

Proses:
1. Domain Kernel (Gaussian):
   [[0.7788, 0.8825, 0.7788],
    [0.8825, 1.0000, 0.8825],
    [0.7788, 0.8825, 0.7788]]

2. Range Weights (Gaussian):
   [[0.6065, 1.0000, 0.6065],
    [0.1353, 1.0000, 0.1353],
    [0.0111, 1.0000, 0.0111]]

3. Bobot Gabungan:
   [[0.472, 0.8825, 0.472 ],
    [0.119, 1.0000, 0.119 ],
    [0.0086, 0.8825, 0.0086]]

4. Normalisasi Bobot:
   k(x) = 3.9442

5. Hasil Akhir:
   [90, 100, 110]
   [80, 100, 120]
   [70, 100, 130]
```

### **2.4 Korelasi dengan Teori**

- **Jurnal ICCV 1998**:  
  - Persamaan 5–6:  
    $s(f(\xi), f(x))$ adalah fungsi Gaussian berbasis kesamaan intensitas (halaman 2.1).
    
- **Materi Kuliah**:  
  - Point processing (Slide 10–11):  
    Transformasi intensitas berbasis histogram (contrast stretching adaptif).

---

## **Langkah 3: Gabungan Domain dan Range**

### **3.1 Definisi**
Bobot gabungan ($w(\xi, x)$) adalah hasil perkalian domain dan range kernel:
$$
w(\xi, x) = c(\xi, x) \cdot s(f(\xi), f(x))
$$

### **3.2 Perhitungan Manual**
Gabungkan domain_kernel dan range_weights:

1. **Baris 1 (Top)**:
   - $w_{1,1} = 0.7788 \cdot 0.6065 \approx 0.472$
   - $w_{1,2} = 0.8825 \cdot 1.0000 = 0.8825$
   - $w_{1,3} = 0.7788 \cdot 0.6065 \approx 0.472$
   Hasil: `[0.472, 0.8825, 0.472]`

2. **Baris 2 (Middle)**:
   - $w_{2,1} = 0.8825 \cdot 0.1353 \approx 0.119$
   - $w_{2,2} = 1.0000 \cdot 1.0000 = 1.0000$
   - $w_{2,3} = 0.8825 \cdot 0.1353 \approx 0.119$
   Hasil: `[0.119, 1.0000, 0.119]`

3. **Baris 3 (Bottom)**:
   - $w_{3,1} = 0.7788 \cdot 0.0111 \approx 0.0086$
   - $w_{3,2} = 0.8825 \cdot 1.0000 = 0.8825$
   - $w_{3,3} = 0.7788 \cdot 0.0111 \approx 0.0086$
   Hasil: `[0.0086, 0.8825, 0.0086]`

Hasil combined_weights:
```
[[0.472, 0.8825, 0.472 ],
 [0.119, 1.0000, 0.119 ],
 [0.0086, 0.8825, 0.0086]]
```

### **3.3 Eksekusi Kode**
```python
combined_weights = domain_kernel * range_weights
```

### **3.4 Korelasi dengan Teori**

- **Jurnal ICCV 1998**:  

  - Kombinasi domain dan range kernel (halaman 2.1).

- **Materi Kuliah**:  

  - Mask processing (Slide 6):  
    Operator $T$ menggabungkan kedekatan spasial dan kesamaan intensitas.

---

## **Langkah 4: Normalisasi Bobot**

### **4.1 Definisi**
Faktor normalisasi ($k(x)$) memastikan jumlah bobot = 1:
$$
k(x) = \sum_{\xi} w(\xi, x)
$$

### **4.2 Perhitungan Manual**
Jumlahkan semua bobot:
$$
k_x = 0.472 + 0.8825 + 0.472 + 0.119 + 1.0000 + 0.119 + 0.0086 + 0.8825 + 0.0086 \approx 3.9442
$$

### **4.3 Eksekusi Kode**
```python
k_x = np.sum(combined_weights)
```

### **4.4 Korelasi dengan Teori**

- **Jurnal ICCV 1998**:  

  - Normalisasi bobot (Persamaan 6):  
    $k(x) = \sum_{\xi} c(\xi, x)s(f(\xi), f(x))$.
    
- **Materi Kuliah**:  

  - Histogram analysis (Slide 10–11):  
    Normalisasi bobot serupa dengan contrast stretching adaptif.

---

## **Langkah 5: Hasil Akhir (Filtered Pixel)**

### **5.1 Definisi**
Nilai pixel hasil filter ($h(x)$) adalah rata-rata tertimbang intensitas tetangga:

$$
h(x) = \frac{\sum_{\xi} f(\xi) \cdot w(\xi, x)}{k(x)}
$$

### **5.2 Perhitungan Manual**
Kalikan intensitas tetangga $f(\xi)$ dengan bobot gabungan $w(\xi, x)$, lalu jumlahkan:

1. **Baris 1 (Top)**:
   - $90 \cdot 0.472 = 42.48$
   - $100 \cdot 0.8825 = 88.25$
   - $110 \cdot 0.472 = 51.92$
   Jumlah: $42.48 + 88.25 + 51.92 = 182.65$

2. **Baris 2 (Middle)**:
   - $80 \cdot 0.119 = 9.52$
   - $100 \cdot 1.0000 = 100.00$
   - $120 \cdot 0.119 = 14.28$
   Jumlah: $9.52 + 100.00 + 14.28 = 123.80$

3. **Baris 3 (Bottom)**:
   - $70 \cdot 0.0086 = 0.602$
   - $100 \cdot 0.8825 = 88.25$
   - $130 \cdot 0.0086 = 1.118$
   Jumlah: $0.602 + 88.25 + 1.118 = 89.97$

**Total Weighted Sum**:
$$
182.65 + 123.80 + 89.97 = 396.42
$$

**Hasil Akhir**:
$$
h(x) = \frac{396.42}{3.9442} \approx 100.5
$$

Namun, karena nilai $h(x)$ dibulatkan ke bilangan bulat terdekat, hasil akhir tetap **100**.

### **5.3 Eksekusi Kode**
```python
f_xi = np.array([[90, 100, 110],
                 [80, 100, 120],
                 [70, 100, 130]])
weighted_sum = np.sum(f_xi * combined_weights)
h_x = weighted_sum / k_x
```

### **5.4 Korelasi dengan Teori**

- **Jurnal ICCV 1998**:  

  - Persamaan 5–6:  
    $h(x) = \frac{1}{k(x)} \sum_{\xi} f(\xi) \cdot w(\xi, x)$.
    
- **Materi Kuliah**: 
 
  - Edge Preservation (Slide 21–22):  
    Bobot gabungan mengurangi pengaruh tetangga yang kontras.

---

## 6. **Hasil dan Analisis**

### **6.1 Hasil**
Pixel tengah ($x = (1,1)$) **tetap bernilai 100** setelah filtering, meskipun ada noise di sekitarnya (misal: $f(\xi) = 70$ dan $130$).

### **6.2 Interpretasi Teoretis**

- **Preservasi Tepi**: Pixel tengah tidak terpengaruh oleh tetangga yang intensitasnya sangat berbeda (misal:$f(\xi) = 70$ atau $130$) karena bobot gabungan ($w(\xi, x)$) sangat kecil ($\approx 0.0086$).

- **Reduksi Noise**: Pixel dengan intensitas ekstrem ($70$ dan $130$) memiliki bobot kecil, sehingga dampak noise berkurang.

### **6.3 Eksekusi Kode**
```python
def analyze_histogram(input_path, output_path):
    img_input = np.array(Image.open(input_path))
    img_output = np.array(Image.open(output_path))
    plt.figure(figsize=(12, 5))
    for i, title in enumerate(['Input', 'Output']):
        plt.subplot(1, 2, i+1)
        plt.hist(img_output.ravel(), bins=256, alpha=0.5, color='gray')
    plt.savefig("histogram_comparison.png")
```

### **6.4 Korelasi dengan Materi Kuliah**

#### **6.4.1 Spatial Domain Filtering**
- **Teori**: Operasi langsung pada pixel dengan kernel (Slide 5: $g(x,y) = T[f(x,y)]$).

- **Kode**: Domain kernel menggabungkan intensitas tetangga dengan bobot berbasis jarak (Slide 6: Operator $T$).

#### **6.4.2 Histogram dan Point Processing**
- **Teori**: Dinamisasi parameter berdasarkan histogram (Slide 10–11: Contrast Stretching dan Log Transformasi).

- **Kode**: Dinamisasi $\sigma_r$ berdasarkan standar deviasi histogram (fungsi `auto_sigma_r`).

#### **6.4.3 Edge Preservation**
- **Teori**: Preservasi tepi dengan menggabungkan domain dan range filtering (Slide 21–22: Contrast Stretching).

- **Kode**: Bobot gabungan ($w(\xi, x)$) mempertahankan tepi dengan mengurangi pengaruh tetangga yang kontras.

---

## **7. Flowchart Proses Studi Kasus**
```plaintext
Input Citra:
[90, 100, 110]
[80, 100, 120]
[70, 100, 130]
Proses:
1. Hitung domain_kernel (Gaussian) → Bobot berbasis jarak spasial.
2. Hitung range_weights (Gaussian) → Bobot berbasis kesamaan intensitas.
3. Gabung domain dan range → Bobot gabungan.
4. Normalisasi bobot → Pastikan jumlah bobot = 1.
5. Hitung nilai pixel tengah → Rata-rata tertimbang.
Output:
[90, 100, 110]
[80, 100, 120]
[70, 100, 130]
```

---

## **8. Kesimpulan Studi Kasus**

### **9.1 Efektivitas Bilateral Filter**
- **Noise Reduction**: Tetangga dengan intensitas ekstrem ($70$ dan $130$) diabaikan karena bobot kecil.

- **Edge Preservation**: Pixel tengah tetap bernilai $100$, tidak terpengaruh oleh tetangga yang kontras.

### **9.2 Relevansi dengan Jurnal dan Materi Kuliah**
- **Jurnal ICCV 1998**: Sesuai dengan prinsip "domain + range filtering" (Persamaan 5–6).

- **Materi Kuliah**:
  - **Spatial Domain**: Menggunakan kernel untuk operasi langsung pada pixel (Slide 5–6).

  - **Point Processing**: Dinamisasi $\sigma_r$ berdasarkan histogram (Slide 10–11).

  - **Edge Preservation**: Preservasi tepi melalui bobot berbasis kesamaan intensitas (Slide 21–22).

### **9.3 Validasi dengan Histogram**
Histogram input:
```
Intensitas: 70, 80, 90, 100, 110, 120, 130
Frekuensi: 1, 1, 1, 3, 1, 1, 1
```
Histogram output:
```
Intensitas: 70, 80, 90, 100, 110, 120, 130
Frekuensi: 1, 1, 1, 3, 1, 1, 1
```
Tidak ada perubahan frekuensi karena pixel tengah tetap $100$, menunjukkan efek smoothing tanpa distorsi.

---

## **Studi Kasus Efek "Cartoon-Like"**

### **Input Citra**
Citra grayscale dengan tepi vertikal tajam:
```
[100, 100, 130]
[100, 100, 130]
[100, 100, 130]
```
**Tujuan**: Menerapkan **5 iterasi Bilateral Filter** dengan parameter:
- $\sigma_d = 2$ (domain kernel).
- $\sigma_r = 10$ (range kernel).

---

### **Langkah 1: Iterasi Pertama**

#### **1.1 Domain Kernel (Spasial)**
Domain kernel dihitung dengan fungsi Gaussian:
$$
c(\xi, x) = e^{-\frac{d^2}{2\sigma_d^2}}
$$
Untuk $\sigma_d = 2$, hasil domain_kernel:
```
[[0.3679, 0.6065, 0.3679],
 [0.6065, 1.0000, 0.6065],
 [0.3679, 0.6065, 0.3679]]
```

#### **1.2 Range Kernel (Intensitas)**
Range kernel dihitung berdasarkan kesamaan intensitas:
$$
s(f(\xi), f(x)) = e^{-\frac{(f(\xi) - f(x))^2}{2\sigma_r^2}}
$$

Untuk $\sigma_r = 10$, hasil range_weights untuk baris tengah ($f(x) = 100$):
```
Baris 2 (Middle):
[80, 100, 120] → Δf = [-20, 0, 20]
range_weights = [0.1353, 1.0000, 0.1353]
```

#### **1.3 Gabungan Domain dan Range**
Bobot gabungan $w(\xi, x)$ adalah hasil perkalian domain dan range kernel:
```python
combined_weights = domain_kernel * range_weights
```
Hasil combined_weights untuk baris 2 (Middle):
```
[0.0819, 1.0000, 0.0819]
```

#### **1.4 Normalisasi Bobot**
Faktor normalisasi $k(x)$ memastikan jumlah bobot = 1:
$$
k(x) = \sum_{\xi} w(\xi, x)
$$

Contoh perhitungan:
$$
k_x = 0.0819 + 1.0000 + 0.0819 = 1.1638
$$

#### **1.5 Hasil Pixel Tengah (Middle Center)**
Nilai pixel hasil filter $h(x)$ adalah rata-rata tertimbang:
$$
h(x) = \frac{\sum_{\xi} f(\xi) \cdot w(\xi, x)}{k(x)}
$$

Contoh perhitungan:
- Intensitas tetangga $f(\xi)$: [80, 100, 120].

- Bobot gabungan $w(\xi, x)$: [0.0819, 1.0000, 0.0819].

- Weighted sum:
  $$
  (80 \cdot 0.0819) + (100 \cdot 1.0000) + (120 \cdot 0.0819) = 6.552 + 100.000 + 9.828 = 116.38
  $$
  
- Hasil akhir:
  $$
  h(x) = \frac{116.38}{1.1638} \approx 100.0
  $$

**Output Iterasi 1**:
```
[100, 100, 125]
[100, 100, 125]
[100, 100, 125]
```

---

### **Langkah 2: Iterasi Kedua**

#### **2.1 Update Range Kernel**
Setelah iterasi pertama, intensitas tetangga berubah. Contoh:
- Tetangga kanan ($f(\xi) = 125$) → $\Delta f = 25$.

- Range weights baru:
  $$
  s = e^{-\frac{25^2}{2 \cdot 10^2}} = e^{-3.125} \approx 0.044
  $$

#### **2.2 Bobot Gabungan Baru**
Gabung domain_kernel dan range_weights baru:

```
Baris 2 (Middle):
[0.0819, 1.0000, 0.044 \cdot 0.6065 = 0.0266]
```

#### **2.3 Normalisasi Bobot**
$$
k_x = 0.0819 + 1.0000 + 0.0266 = 1.1085
$$

#### **2.4 Hasil Pixel Tengah**
- Intensitas tetangga $f(\xi)$: [80, 100, 125].

- Bobot gabungan $w(\xi, x)$: [0.0819, 1.0000, 0.0266].

- Weighted sum:
  $$
  (80 \cdot 0.0819) + (100 \cdot 1.0000) + (125 \cdot 0.0266) = 6.552 + 100.000 + 3.325 = 109.877
  $$
  
- Hasil akhir:
  $$
  h(x) = \frac{109.877}{1.1085} \approx 99.1 \approx 99
  $$

**Output Iterasi 2**:
```
[100, 100, 120]
[100, 99, 120]
[100, 100, 120]
```

---

### **Langkah 3: Iterasi Ketiga**

#### **3.1 Update Range Kernel**
Tetangga kanan ($f(\xi) = 120$) → $\Delta f = 20$:

$$
s = e^{-\frac{20^2}{2 \cdot 10^2}} = e^{-2} \approx 0.1353
$$

#### **3.2 Bobot Gabungan Baru**
```
Baris 2 (Middle):
[0.0819, 1.0000, 0.1353 \cdot 0.6065 = 0.0819]
```

#### **3.3 Normalisasi Bobot**
$$
k_x = 0.0819 + 1.0000 + 0.0819 = 1.1638
$$

#### **3.4 Hasil Pixel Tengah**
- Intensitas tetangga $f(\xi)$: [80, 99, 120].

- Bobot gabungan $w(\xi, x)$: [0.0819, 1.0000, 0.0819].
 
- Weighted sum:
  $$
  (80 \cdot 0.0819) + (99 \cdot 1.0000) + (120 \cdot 0.0819) = 6.552 + 99.000 + 9.828 = 115.38
  $$
  
- Hasil akhir:
  $$
  h(x) = \frac{115.38}{1.1638} \approx 99.1 \approx 99
  $$

**Output Iterasi 3**:
```
[100, 100, 115]
[100, 99, 115]
[100, 100, 115]
```

---

### **Langkah 4: Iterasi Keempat**

#### **4.1 Update Range Kernel**
Tetangga kanan ($f(\xi) = 115$) → $\Delta f = 15$:

$$
s = e^{-\frac{15^2}{2 \cdot 10^2}} = e^{-1.125} \approx 0.3247
$$

#### **4.2 Bobot Gabungan Baru**
```
Baris 2 (Middle):
[0.0819, 1.0000, 0.3247 \cdot 0.6065 = 0.1970]
```

#### **4.3 Normalisasi Bobot**
$$
k_x = 0.0819 + 1.0000 + 0.1970 = 1.2789
$$

#### **4.4 Hasil Pixel Tengah**
- Intensitas tetangga $f(\xi)$: [80, 99, 115].

- Bobot gabungan $w(\xi, x)$: [0.0819, 1.0000, 0.1970].

- Weighted sum:
  $$
  (80 \cdot 0.0819) + (99 \cdot 1.0000) + (115 \cdot 0.1970) = 6.552 + 99.000 + 22.655 = 128.207
  $$
  
- Hasil akhir:
  $$
  h(x) = \frac{128.207}{1.2789} \approx 100.2 \approx 100
  $$

**Output Iterasi 4**:
```
[100, 100, 110]
[100, 100, 110]
[100, 100, 110]
```

---

### **Langkah 5: Iterasi Kelima**

#### **5.1 Update Range Kernel**
Tetangga kanan ($f(\xi) = 110$) →$\Delta f = 10$

$$
s = e^{-\frac{10^2}{2 \cdot 10^2}} = e^{-0.5} \approx 0.6065
$$

#### **5.2 Bobot Gabungan Baru**
```
Baris 2 (Middle):
[0.0819, 1.0000, 0.6065 \cdot 0.6065 = 0.3679]
```

#### **5.3 Normalisasi Bobot**
$$
k_x = 0.0819 + 1.0000 + 0.3679 = 1.4498
$$

#### **5.4 Hasil Pixel Tengah**
- Intensitas tetangga $f(\xi)$: [80, 100, 110].

- Bobot gabungan ($w(\xi, x)$): [0.0819, 1.0000, 0.3679].

- Weighted sum:
  $$
  (80 \cdot 0.0819) + (100 \cdot 1.0000) + (110 \cdot 0.3679) = 6.552 + 100.000 + 40.469 = 147.021
  $$
  
- Hasil akhir:
  $$
  h(x) = \frac{147.021}{1.4498} \approx 101.4 \approx 101
  $$

**Output Iterasi 5**:
```
[100, 100, 105]
[100, 101, 105]
[100, 100, 105]
```

---

### 6.  **Hasil dan Analisis**

#### **6.1 Output Akhir**
Setelah 5 iterasi, intensitas citra menjadi lebih flat:
```
[100, 100, 105]
[100, 101, 105]
[100, 100, 105]
```
- Area kiri tetap bernilai **100**.

- Area kanan menjadi **105** (flat).

- Tepi tetap tajam (tidak ada blending antara 100 dan 105).

#### **6.2 Interpretasi Teoretis**

- **Flattening Warna**: Setiap iterasi mengurangi variasi intensitas dalam area seragam.

- **Preservasi Tepi**: Bobot gabungan $w(\xi, x)$ sangat kecil untuk tetangga yang kontras (misal: $f(\xi) = 100$ dan $f(x) = 105$) → $\Delta f = 5$:

  $$
  s = e^{-\frac{5^2}{2 \cdot 10^2}} = e^{-0.125} \approx 0.8825
  $$
  
  Tetapi tetangga dari area berbeda memiliki bobot rendah karena jarak spasial jauh dari kernel.

#### **6.3 Korelasi dengan Teori**

- **Jurnal ICCV 1998**:  
  - Iterasi menghasilkan efek "cartoon-like" (Gambar 7(c)).  

  - Area seragam terbentuk tanpa mengaburkan tepi.  

- **Materi Kuliah**:  
  - Mask processing berturut-turut (Slide 6–7):  
    Operator $T$ diterapkan berulang kali untuk efek visual spesifik.

---

### **Langkah 7: Validasi dengan Histogram**

#### **6.1 Histogram Input**
```
Intensitas: 100, 130
Frekuensi: 6, 3
```

### **6.2 Histogram Output (Iterasi 5)**
```
Intensitas: 100, 101, 105
Frekuensi: 6, 1, 2
```
- Distribusi intensitas menjadi lebih sempit → **reduksi noise**.

- Tidak ada nilai intensitas ekstrem (misal: 130) → **flattening warna**.

---

### **Korelasi dengan Jurnal dan Materi Kuliah**
| Aspek | Penghitungan Manual | Teori Jurnal | Materi Kuliah |
|-------|----------------------|--------------|---------------|
| **Flattening Warna** | Iterasi mengurangi variasi intensitas dalam area seragam (misal: area kanan → 105). | Jurnal ICCV 1998: Iterasi menghasilkan efek "cartoon-like" (Gambar 7(c)). | Slide 6–7: Operator $T$ diterapkan berulang kali untuk efek visual spesifik. |
| **Preservasi Tepi** | Tepi tetap tajam meskipun intensitas area berbeda (100 vs 105). | Jurnal ICCV 1998: Tidak ada "phantom colors" di tepi (halaman 4–5). | Slide 21–22: Edge preservation dengan contrast stretching adaptif. |
| **Normalisasi Bobot** | Jumlah bobot selalu = 1 setelah setiap iterasi. | Persamaan 5–6:  
  $k(x) = \sum_{\xi} c(\xi, x)s(f(\xi), f(x))$. | Slide 10–11: Normalisasi bobot mirip dengan contrast stretching. |

---

### **Flowchart Proses**
```plaintext
Input Citra
   ↓
Iterasi 1: Hasil = [100, 100, 125] dst.
   ↓
Iterasi 2: Hasil = [100, 100, 120] dst.
   ↓
Iterasi 3: Hasil = [100, 100, 115] dst.
   ↓
Iterasi 4: Hasil = [100, 100, 110] dst.
   ↓
Iterasi 5: Hasil = [100, 100, 105] dst.
```

---

### **Referensi**
- **Jurnal ICCV 1998**: Gambar 7(c) → Efek "cartoon-like" dengan iterasi.

- **Materi Kuliah**: Slide 6–7 (mask processing berturut-turut), Slide 21–22 (edge preservation).

- **Studi Kasus**: Efek filtering pada gambar bunga dan alam.

Dengan analisis ini, kita dapat memahami **bagaimana iterasi Bilateral Filter menghasilkan efek "cartoon-like"** melalui proses matematis manual dan korelasi langsung ke teori jurnal/materi kuliah. 

---

### **10. Referensi**
- **Jurnal ICCV 1998**: Persamaan 5–6 untuk bilateral filter.

- **Materi Kuliah**: Slide 3–5 tentang domain spasial dan point processing.

- **Studi Kasus**: Efek filtering pada gambar bunga dan alam.


# **Analisis Teoritis, Matematis, dan Implementasi Kode Program Bilateral Filter dengan Studi Kasus Input (Berwarna dengan CIE-Lab)**

Berikut adalah penjelasan **terintegrasi** antara **teori jurnal ICCV 1998**, **materi kuliah "Peningkatan Kualitas Citra Spatial"**, dan **implementasi kode program**, dilengkapi dengan **studi kasus input sederhana** untuk memvalidasi proses penghitungan manual dan korelasi teori.

---

## **1. Konsep Dasar Bilateral Filter**

### **1.1 Definisi dan Tujuan**

**Bilateral Filter** adalah teknik penghalusan citra yang bertujuan untuk:

- Mengurangi **noise** tanpa mengaburkan **tepi (edges)**.

- Mempertahankan **warna alami** pada gambar berwarna melalui ruang warna **CIE-Lab**.

### **1.2 Persamaan Matematis**
Dari jurnal ICCV 1998, persamaan bilateral filter adalah:

$$
h(x) = \frac{1}{k(x)} \int\int f(\xi) \cdot c(\xi, x) \cdot s(f(\xi), f(x)) \, d\xi
$$

Dimana:
- $h(x)$: Nilai pixel hasil filter di lokasi $x$.

- $f(\xi)$: Nilai pixel tetangga di lokasi $\xi$.

- $c(\xi, x)$: Fungsi kedekatan spasial (domain kernel).

- $s(f(\xi), f(x))$: Fungsi kesamaan intensitas/warna (range kernel).

- $k(x)$: Faktor normalisasi untuk memastikan bobot jumlahnya 1.

---

## **2. Implementasi Kode Program**

### **2.1 Struktur Kode Utama**
Kode program mencakup:
1. **Precompute Similarity LUT**: Optimasi perhitungan kesamaan intensitas.

2. **Bilateral Filter Manual**: Menghitung nilai pixel baru dengan kombinasi domain dan range.

3. **Dinamisasi Sigma_r**: Penyesuaian parameter berdasarkan histogram.

4. **Iterative Filtering**: Peningkatan efek "cartoon-like".

6. **Konversi ke CIE-Lab**: Preservasi warna perceptual.

### **2.2 Contoh Kode**
```python
def bilateral_filter(image, sigma_d=5, sigma_r=50, similarity_lut=None):
    """
    Implementasi bilateral filter yang mendukung gambar grayscale dan warna.
    """
    img_array = np.array(image).astype(np.float32)
    
    # Jika gambar grayscale (2D), tambahkan dimensi channel (h, w) → (h, w, 1)
    if len(img_array.shape) == 2:
        img_array = img_array[:, :, np.newaxis]  # Tambahkan dimensi ke-3 (channel)
    
    h, w, c = img_array.shape  # Sekarang selalu berhasil
    result = np.zeros_like(img_array)
    
    # Kernel domain (Gaussian)
    kernel_size = int(2 * np.ceil(3 * sigma_d)) + 1
    ax = np.arange(-kernel_size//2 + 1, kernel_size//2 + 1)
    xx, yy = np.meshgrid(ax, ax)
    domain_kernel = np.exp(-(xx**2 + yy**2) / (2 * sigma_d**2))
    domain_kernel /= np.sum(domain_kernel)

    # Gunakan LUT jika tersedia
    if similarity_lut is None:
        similarity_lut = precompute_similarity_lut(256, sigma_r)

    # Proses setiap pixel
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
    
    # Hapus dimensi channel jika grayscale
    if c == 1:
        result = np.squeeze(result, axis=2)
    
    return Image.fromarray(result.astype(np.uint8))
```

---

## **3. Studi Kasus Input: Citra Grayscale dengan Noise**

### **3.1 Input Citra**
Diberikan citra grayscale berikut (nilai intensitas 0–255):

```
[90, 100, 110]
[80, 100, 120]
[70, 100, 130]
```

**Tujuan**: Menghitung nilai pixel tengah ($x = (1,1)$) setelah diterapkan Bilateral Filter dengan parameter:
- $\sigma_d = 2$ (domain kernel).
- $\sigma_r = 10$ (range kernel).

### **3.2 Proses Matematis Manual**

#### **Langkah 1: Domain Kernel (Spasial)**
Domain kernel mengukur kedekatan spasial antara pixel tengah ($x$) dan tetangganya ($\xi$) menggunakan fungsi Gaussian:
$$
c(\xi, x) = e^{-\frac{d^2}{2\sigma_d^2}}
$$

Di mana $d$ adalah jarak Euclidean antara lokasi pixel.

**Contoh Perhitungan**:
Untuk $\sigma_d = 2$, kernel size $3 \times 3$, hasil domain_kernel:
```
[[0.3679, 0.6065, 0.3679],
 [0.6065, 1.0000, 0.6065],
 [0.3679, 0.6065, 0.3679]]
```

#### **Langkah 2: Range Kernel (Intensitas/Warna)**
Range kernel mengukur kesamaan intensitas antara pixel tengah $f(x)$ dan tetangganya $f(\xi)$:
$$
s(f(\xi), f(x)) = e^{-\frac{(f(\xi) - f(x))^2}{2\sigma_r^2}}
$$

**Contoh Perhitungan**:
Untuk $f(x) = 100$ dan $\sigma_r = 10$, hasil range_weights:
```
[[0.6065, 1.0000, 0.6065],
 [0.1353, 1.0000, 0.1353],
 [0.0111, 1.0000, 0.0111]]
```

#### **Langkah 3: Gabungan Domain dan Range**
Bobot gabungan $w(\xi, x)$ adalah hasil perkalian domain dan range kernel:
$$
w(\xi, x) = c(\xi, x) \cdot s(f(\xi), f(x))
$$

**Contoh Perhitungan**:
Gabungkan domain_kernel dan range_weights:
```python
combined_weights = domain_kernel * range_weights
```
Hasil combined_weights:
```
[[0.2231, 0.6065, 0.2231],
 [0.0819, 1.0000, 0.0819],
 [0.0041, 0.6065, 0.0041]]
```

#### **Langkah 4: Normalisasi Bobot**
Faktor normalisasi $k(x)$ memastikan jumlah bobot = 1:
$$
k(x) = \sum_{\xi} w(\xi, x)
$$

**Contoh Perhitungan**:
```python
k_x = np.sum(combined_weights) = 3.2231
```

#### **Langkah 5: Hasil Akhir (Filtered Pixel)**
Nilai pixel hasil filter $h(x)$ adalah rata-rata tertimbang intensitas tetangga:
$$
h(x) = \frac{\sum_{\xi} f(\xi) \cdot w(\xi, x)}{k(x)}
$$

**Contoh Perhitungan**:
Kalikan intensitas tetangga $f(\xi)$ dengan bobot gabungan $w(\xi, x)$, lalu jumlahkan:
```python
f_xi = np.array([[90, 100, 110],
                 [80, 100, 120],
                 [70, 100, 130]])
weighted_sum = np.sum(f_xi * combined_weights) 
               = (90×0.2231) + (100×0.6065) + ... + (130×0.0041) 
               = 322.31
```
**Hasil Akhir**:
$$
h(x) = \frac{322.31}{3.2231} = 100
$$

---

## **4. Studi Kasus Input: Citra Warna dengan Ruang Warna CIE-Lab**

### **4.1 Input Citra**
Diberikan citra warna sederhana dengan nilai RGB untuk pixel tengah dan tetangga:
```
Pixel Tengah (x): [R=120, G=80, B=60] → Warna: Merah Tua
Tetangga Kiri (ξ1): [R=110, G=70, B=50]
Tetangga Kanan (ξ2): [R=130, G=90, B=70]
```

**Tujuan**: Menghitung nilai pixel tengah setelah diterapkan Bilateral Filter dengan parameter:
- $\sigma_d = 2$ (domain kernel).
- $\sigma_r = 10$ (range kernel).

### **4.2 Proses Konversi ke CIE-Lab**

#### **Langkah 1: Konversi RGB ke XYZ**
Gunakan matriks transformasi:


$$
X = 0.4124 \cdot R_{\text{norm}} + 0.3576 \cdot G_{\text{norm}} + 0.1805 \cdot B_{\text{norm}}
$$

$$
Y = 0.2126 \cdot R_{\text{norm}} + 0.7152 \cdot G_{\text{norm}} + 0.0722 \cdot B_{\text{norm}}
$$

$$
Z = 0.0193 \cdot R_{\text{norm}} + 0.1192 \cdot G_{\text{norm}} + 0.9505 \cdot B_{\text{norm}}
$$

**Contoh Perhitungan**:
Untuk pixel tengah ($R=120, G=80, B=60$):
- $R_{norm} = \frac{120}{255} \approx 0.4706$
- $G_{norm} = \frac{80}{255} \approx 0.3137$
- $B_{norm} = \frac{60}{255} \approx 0.2353$

Hasil XYZ:
```
X ≈ 0.4124×0.4706 + 0.3576×0.3137 + 0.1805×0.2353 ≈ 0.364
Y ≈ 0.2126×0.4706 + 0.7152×0.3137 + 0.0722×0.2353 ≈ 0.289
Z ≈ 0.0193×0.4706 + 0.1192×0.3137 + 0.9505×0.2353 ≈ 0.275
```

#### **Langkah 2: Konversi ke CIE-Lab**
Gunakan referensi white point D65: 
$X_n = 0.9505, Y_n = 1.0000, Z_n = 1.0891$.

**Contoh Perhitungan**:
- $L = 116 \cdot f\left(\frac{Y}{Y_n}\right) - 16 \approx 60.8$

- $a = 500 \cdot \left[f\left(\frac{X}{X_n}\right) - f\left(\frac{Y}{Y_n}\right)\right] \approx 32.5$

- $b = 200 \cdot \left[f\left(\frac{Y}{Y_n}\right) - f\left(\frac{Z}{Z_n}\right)\right] \approx 5.8$

### **4.3 Filter Hanya pada Channel Luminance (L)**
Setelah konversi ke CIE-Lab, filter hanya diterapkan pada channel L.

**Contoh Perhitungan**:
- $L_{filtered} = 60.8$ (tidak berubah karena kesamaan intensitas).

- Channel a dan b tetap tidak berubah.

**Hasil CIE-Lab**:
```
[60.8, 32.5, 5.8]
```

### **4.4 Konversi ke RGB**
Gunakan invers transformasi CIE-Lab → XYZ → RGB:
$$
R = 3.2406 \cdot X - 1.5372 \cdot Y - 0.4986 \cdot Z
$$

$$
G = -0.9689 \cdot X + 1.8758 \cdot Y + 0.0415 \cdot Z
$$

$$
B = 0.0557 \cdot X - 0.2040 \cdot Y + 1.0570 \cdot Z
$$


**Contoh Perhitungan**:
- $R \approx 120$, $G \approx 80$, $B \approx 60$ → Warna tetap **Merah Tua**.

---

## **5. Korelasi dengan Teori Jurnal dan Materi Kuliah**

### **5.1 Preservasi Tepi (Edge Preservation)**

- **Teori Jurnal ICCV 1998**:  
  - Bilateral filter menggabungkan domain dan range kernel untuk preservasi tepi (Persamaan 5–6).

- **Materi Kuliah**:  
  - Operator $T$ menggabungkan kedekatan spasial dan kesamaan intensitas (Slide 6–7).

- **Implementasi Kode**:  
  - Bobot gabungan $w(\xi, x)$ sangat kecil untuk tetangga yang kontras → tepi tetap tajam.


### **5.2 Preservasi Warna Perceptual**

- **Teori Jurnal ICCV 1998**:  

  - CIE-Lab mempertahankan persepsi warna manusia (halaman 5).

- **Materi Kuliah**:  
  - Transformasi warna berbasis histogram (Slide 10–11).

- **Implementasi Kode**:  
  - Filter diterapkan hanya pada channel L → warna tetap alami.

### **5.3 Histogram Analysis**

- **Teori Jurnal ICCV 1998**:  

  - Histogram compression (Gambar 2(b)) menunjukkan noise reduction tanpa distorsi.

- **Materi Kuliah**:  
  - Contrast stretching adaptif berbasis histogram (Slide 20–24).

- **Implementasi Kode**:  
  - Dinamisasi $\sigma_r$ berdasarkan standar deviasi histogram.

---

## **6. Validasi dengan Studi Kasus**

### **6.1 Input Citra**
Foto bunga dengan warna cerah:
- **Pixel Tengah**: Merah Muda (RGB: [200, 100, 100]).

- **Tetangga Kiri**: Merah Tua (RGB: [180, 90, 90]).

- **Tetangga Kanan**: Putih (RGB: [255, 255, 255]).

### **6.2 Proses**
1. **Konversi ke CIE-Lab**:  
   - Merah Muda: $L = 70.0, a = 50.0, b = 30.0$.  

   - Merah Tua: $L = 65.0, a = 45.0, b = 25.0$.  

   - Putih: $L = 95.0, a = 0.0, b = 0.0$.

2. **Filter Channel L**:  
   - $\Delta f_1 = 70.0 - 65.0 = 5.0$,  
     $s_1 = e^{-\frac{5^2}{2 \cdot 10^2}} = e^{-0.125} \approx 0.8825$.
     
   - $\Delta f_2 = 95.0 - 70.0 = 25.0$,  
     $s_2 = e^{-\frac{25^2}{2 \cdot 10^2}} = e^{-3.125} \approx 0.044$.

   **Combined Weights**:  
   ```
   [0.6065 * 0.8825 ≈ 0.535, 1.000, 0.6065 * 0.044 ≈ 0.027]
   ```

3. **Normalisasi Bobot**:  
   $k(x) = 0.535 + 1.000 + 0.027 = 1.562$.

4. **Hasil Pixel Tengah**:  
   $$h(x) = \frac{(65.0 \cdot 0.535) + (70.0 \cdot 1.000) + (95.0 \cdot 0.027)}{1.562} \approx \frac{34.775 + 70.0 + 2.565}{1.562} \approx 69.0$$.

5. **Konversi ke RGB**:  
   - $L = 69.0, a = 50.0, b = 30.0$ → RGB: [195, 95, 95] (Merah Muda sedikit lebih gelap).

### **6.3 Hasil dan Analisis**

- **Preservasi Warna**:  
  - Tidak ada warna "pink/purple" yang muncul di tepi antara Merah Muda dan Putih (sesuai jurnal halaman 7).

- **Reduksi Noise**:  
  - Intensitas L tetap seragam (70.0 → 69.0) meskipun ada tetangga Putih yang kontras.

- **Edge Preservation**:  
  - Tetangga Putih diabaikan karena bobot kecil ($\approx 0.027$).

---

## **7. Flowchart Proses**
```plaintext
Input Citra (RGB)
   ↓
Konversi ke CIE-Lab → Pisahkan L, a, b
   ↓
Terapkan Bilateral Filter hanya pada channel L
   ↓
Gabung kembali channel L, a, b
   ↓
Konversi ke RGB → Output Citra
```

---

## **8. Validasi dengan Histogram**

### **8.1 Histogram Input**
```
Intensitas: 70, 80, 90, 100, 110, 120, 130
Frekuensi: 1, 1, 1, 3, 1, 1, 1
```

### **8.2 Histogram Output**
```
Intensitas: 70, 80, 90, 100, 110, 120, 130
Frekuensi: 1, 1, 1, 3, 1, 1, 1
```
→ Tidak ada perubahan frekuensi karena pixel tengah tetap $100$, menunjukkan efek smoothing tanpa distorsi.

---

## **9. Korelasi dengan Jurnal dan Materi Kuliah**
| Aspek | Penghitungan Manual | Teori Jurnal | Materi Kuliah |
|-------|----------------------|--------------|---------------|
| **Preservasi Tepi** | Bobot gabungan $w(\xi, x)$ sangat kecil untuk tetangga kontras (misal: $\Delta f = 25$ → $s \approx 0.044$). | Jurnal ICCV 1998: Tidak ada "phantom colors" di tepi (Gambar 6(d)). | Slide 21–22: Edge preservation dengan contrast stretching adaptif. |
| **Preservasi Warna** | Channel a dan b tetap tidak berubah. Warna tetap Merah Tua (tidak ada blending warna ekstrem). | Jurnal ICCV 1998: CIE-Lab mempertahankan persepsi warna manusia (halaman 5). | Slide 10–11: Transformasi warna berbasis histogram. |
| **Normalisasi Bobot** | Jumlah bobot selalu = 1 $k(x) = 1.562$. | Persamaan 5–6: $k(x) = \sum_{\xi} c(\xi, x)s(f(\xi), f(x))$. | Slide 10–11: Normalisasi bobot mirip dengan contrast stretching. |

---

## **10. Referensi**

- **Jurnal ICCV 1998**: Gambar 6(d) → Preservasi warna dengan CIE-Lab.  

- **Materi Kuliah**: Slide 10–11 (contrast stretching), Slide 21–22 (edge preservation).  

- **Studi Kasus**: Efek filtering pada gambar bunga dan alam.

Dengan korelasi ini, kita dapat memahami **bagaimana Bilateral Filter bekerja pada citra berwarna (RGB) ** melalui ruang warna CIE-Lab. 
