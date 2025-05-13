### **1. Input Citra Berwarna (Matriks RGB)**
Asumsikan setiap channel (R, G, B) memiliki nilai intensitas yang sama untuk menyederhanakan contoh. Matriks input:

```
Pixel Intensitas (R, G, B):
[
  [(90, 90, 90),   (85, 85, 85),  (95, 95, 95)],
  [(105, 105, 105), (100, 100, 100), (110, 110, 110)],
  [(80, 80, 80),   (95, 95, 95),  (105, 105, 105)]
]
```

**Keterangan**:
- Posisi tengah `(1,1)` adalah `f(x) = 100` (intensitas R/G/B = 100).

- Nilai intensitas lainnya dibuat bervariasi sekitar 100 untuk simulasi.

---

### **2. Domain Kernel (σ_d = 2)**
Kernel domain menghitung jarak spasial dari titik tengah. Dengan σ_d=2, rumusnya:
```
W_d = exp(-(d²)/(2σ_d²))
```

**Langkah**:
1. Hitung jarak Euclidean kuadrat (`d²`) dari titik tengah (posisi `(1,1)`).

3. Hitung bobot domain untuk setiap posisi.

**Matriks Jarak Kuadrat**:
```
[
  [2, 1, 2],   # (0,0): d² = (1-0)² + (1-0)² = 2
  [1, 0, 1],   # (1,1): d² = 0
  [2, 1, 2]
]
```

**Domain Kernel (σ_d = 2)**:
```
[
  [exp(-2/(2*4)), exp(-1/(2*4)), exp(-2/(2*4))],
  [exp(-1/(2*4)), exp(0), exp(-1/(2*4))],
  [exp(-2/(2*4)), exp(-1/(2*4)), exp(-2/(2*4))]
]
```

**Hasil Numerik**:
```
[
  [0.7788, 0.8825, 0.7788],
  [0.8825, 1.0000, 0.8825],
  [0.7788, 0.8825, 0.7788]
]
```

**Normalisasi Domain Kernel**:
Jumlahkan semua bobot domain:  

`0.7788 + 0.8825 + 0.7788 + 0.8825 + 1.0000 + 0.8825 + 0.7788 + 0.8825 + 0.7788 ≈ 7.7252` 
 
Bagi setiap bobot dengan 7.7252:
```
[
  [0.1008, 0.1142, 0.1008],
  [0.1142, 0.1294, 0.1142],
  [0.1008, 0.1142, 0.1008]
]
```

---

### **3. Range Kernel (σ_r = 10)**
Kernel range menghitung perbedaan intensitas dengan titik tengah `(1,1)` (intensitas = 100). Rumus:
```
W_r = exp(-(ΔI²)/(2σ_r²))
```

**Langkah**:
1. Hitung perbedaan intensitas `ΔI = |I(x,y) - I_center|`.

3. Hitung bobot range untuk setiap posisi.

**Contoh Perhitungan**:
- Posisi `(0,0)` (intensitas = 90):  
  `ΔI = |90 - 100| = 10 → W_r = exp(-(10²)/(2*10²)) = exp(-0.5) ≈ 0.6065`

- Posisi `(1,2)` (intensitas = 110):  
  `ΔI = |110 - 100| = 10 → W_r = 0.6065`

**Range Kernel (σ_r = 10)**:
```
[
  [0.6065, 0.9284, 0.9284],  # ΔI: 10, 15, 5
  [0.3521, 1.0000, 0.3521],  # ΔI: 5, 0, 10
  [0.1353, 0.9284, 0.3521]   # ΔI: 20, 5, 5
]
```

---

### **4. Combined Weights**
Gabungkan domain dan range kernel dengan perkalian elemen-wise:
```
[
  [0.1008 * 0.6065, 0.1142 * 0.9284, 0.1008 * 0.9284],
  [0.1142 * 0.3521, 0.1294 * 1.0000, 0.1142 * 0.3521],
  [0.1008 * 0.1353, 0.1142 * 0.9284, 0.1008 * 0.3521]
]
```

**Hasil Numerik**:
```
[
  [0.0612, 0.1060, 0.0936],
  [0.0402, 0.1294, 0.0402],
  [0.0136, 0.1060, 0.0355]
]
```

**Normalisasi Combined Weights**:

Jumlahkan semua bobot:  

`0.0612 + 0.1060 + 0.0936 + 0.0402 + 0.1294 + 0.0402 + 0.0136 + 0.1060 + 0.0355 ≈ 0.6257`  

Bagi setiap bobot dengan 0.6257:
```
[
  [0.0978, 0.1694, 0.1496],
  [0.0643, 0.2068, 0.0643],
  [0.0217, 0.1694, 0.0567]
]
```

---

### **5. Filtered Value (Output)**
Kalikan bobot normalisasi dengan intensitas setiap pixel dan jumlahkan:
```
Filtered Value = Σ (Bobot * Intensitas)
```

**Perhitungan**:
```
(0.0978*90) + (0.1694*85) + (0.1496*95) +
(0.0643*105) + (0.2068*100) + (0.0643*110) +
(0.0217*80) + (0.1694*95) + (0.0567*105)
```

**Hasil**:
```
≈ 8.80 + 14.40 + 14.21 + 6.75 + 20.68 + 7.07 + 1.74 + 16.09 + 5.95 ≈ **95.7**
```

---

### **6. Kesimpulan**
- **Input Center Pixel**: 100 (R/G/B).

- **Output Setelah Filtering**: ~95.7 (dibulatkan ke 96).

- **Efek Filter**:

  - Menurunkan intensitas pixel dengan tetangga yang lebih gelap.

  - Mempertahankan tepi karena penggunaan range kernel.

Contoh ini menunjukkan bagaimana bilateral filter menggabungkan informasi spasial dan intensitas untuk mempertahankan tepi sambil menghaluskan noise.
