# Dataset dan Rencana Riset Kecil

## 1. Gambaran Dataset

Dataset dikumpulkan sendiri (primer) dari Laboratorium Komputer SCR, Fakultas Ilmu Komputer UPN "Veteran" Jawa Timur memakai alat IoT berbasis ESP32. Data berupa time series multivariat dengan lima fitur dan penanda waktu.

| Atribut | Keterangan |
|---|---|
| Sumber | Alat IoT buatan sendiri (ESP32 + MQ-2, MQ-7, MQ-135, AHT10) |
| Lokasi | Lab komputer SCR |
| Waktu | 5 hari kerja, 08.00 sampai 16.00 WIB |
| Interval sampling | 30 detik |
| Sampel per hari | sekitar 960 |
| Total sampel | sekitar 4.800 per parameter |
| Format | CSV (dari serial USB ESP32 ke laptop) |
| Sifat data | Tidak berlabel, kondisi normal untuk pelatihan |

## 2. Skema Kolom

| Kolom | Tipe | Satuan | Sensor | Keterangan |
|---|---|---|---|---|
| timestamp | datetime | WIB | ESP32 / laptop | Penanda waktu pembacaan |
| mq2_ppm | float | ppm | MQ-2 | Gas mudah terbakar dan asap |
| mq135_ppm | float | ppm | MQ-135 | Kualitas udara umum (VOC) |
| mq7_ppm | float | ppm | MQ-7 | Karbon monoksida (CO) |
| suhu_c | float | °C | AHT10 | Suhu ruangan |
| rh_persen | float | %RH | AHT10 | Kelembapan relatif |
| label | int | 0/1 | Anotasi | Hanya untuk data uji (0 normal, 1 anomali). Kosong pada data latih |

## 3. Pembagian Data

| Subset | Isi | Proporsi |
|---|---|---|
| Data latih | Sequence kondisi normal | 70% dari data normal |
| Data validasi | Sequence kondisi normal, dipakai untuk memantau loss dan menentukan threshold | 30% dari data normal |
| Data uji | Data normal yang tidak dipakai latih ditambah data simulasi anomali | Disusun terpisah |

Pembagian dilakukan secara berurutan menurut waktu agar tidak ada kebocoran data antar window.

## 4. Skenario Data Anomali (Data Uji)

Karena kebakaran sungguhan berisiko dan langka, anomali disimulasikan secara terkendali dan aman, lalu dilabeli manual berdasarkan catatan waktu kejadian.

| Skenario | Tujuan | Contoh pelaksanaan (aman) |
|---|---|---|
| Lonjakan gas | Menguji respons MQ-2 dan MQ-7 | Paparan sumber gas atau asap buatan dalam jumlah kecil dan terkendali |
| Lonjakan VOC | Menguji MQ-135 | Paparan uap VOC ringan di dekat sensor |
| Kenaikan suhu bertahap | Meniru overheat perangkat | Perangkat atau sumber panas aman didekatkan ke sensor |
| Anomali multivariat | Menguji korelasi antar sensor | Kombinasi kenaikan gas, suhu, dan penurunan RH secara bersamaan |

Setiap kejadian dicatat dengan waktu mulai, waktu selesai, dan jenis skenario di sebuah berkas log.

## 5. Rencana Preprocessing

1. Cek missing value, tangani dengan interpolasi linear.
2. Filter nilai di luar rentang fisis sensor menurut datasheet.
3. Deteksi outlier dengan rolling window dan cek rate of change.
4. Cocokkan titik mencurigakan dengan catatan aktivitas ruangan.
5. Normalisasi Min-Max 0 sampai 1 (parameter dari data latih saja).
6. Sliding window 10 sampai 20 time step, stride 1, bentuk tensor (jumlah sampel, T, 5).

## 6. Estimasi Ukuran

Dengan 4.800 sampel mentah dan window 10 sampai 20 dengan stride 1, jumlah sequence yang terbentuk sekitar 4.780 sampai 4.790. Kira kira 70% untuk latih dan 30% untuk validasi. Jumlah ini kecil, jadi dropout 0,1 sampai 0,2 dan early stopping dipakai untuk menekan overfitting.

## 7. Rencana Riset Kecil (Pilot)

Sebelum pengambilan data penuh 5 hari, dilakukan riset kecil untuk memvalidasi alur.

| Tahap | Kegiatan | Keluaran |
|---|---|---|
| 1 | Uji alat dan kalibrasi sensor MQ di lab selama 1 hari | Nilai baseline dan kestabilan sensor |
| 2 | Pengambilan data pilot 1 sampai 2 hari | Dataset kecil CSV |
| 3 | Preprocessing dan windowing pada data pilot | Pipeline yang berjalan |
| 4 | Latih LSTM-Autoencoder awal pada data pilot | Kurva training dan validation loss |
| 5 | Uji dengan satu skenario anomali sederhana | Bukti awal bahwa reconstruction error naik |
| 6 | Evaluasi dan perbaikan pipeline sebelum data penuh | Catatan perbaikan |

## 8. Struktur Folder Data di Repo

```
data/
  raw/          # CSV mentah dari serial
  clean/        # hasil cleaning
  test_anomaly/ # data uji + log skenario anomali
  README.md     # deskripsi dataset
```

Data mentah belum ada di repo ini. Berkas CSV ditambahkan setelah pengambilan data selesai.

## 9. Etika dan Keselamatan

Simulasi anomali dilakukan dalam skala kecil, di bawah pengawasan, dengan ventilasi memadai, dan tidak memakai api terbuka. Pengambilan data di lab dilakukan dengan izin pengelola laboratorium.
