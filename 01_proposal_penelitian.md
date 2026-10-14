# Proposal Penelitian

**Judul:** Sistem Deteksi Anomali Kualitas Udara dan Deteksi Dini Asap Berbasis LSTM-Autoencoder

**Peneliti:** Dea Rajwa Zahra Athaya (NPM 23081010013)
**Pembimbing:** Prof. Dr. Basuki Rahmat, S.Si., MT., ITS-AI dan Dr. Firza Prima Aditiawan, S.Kom., MTI
**Instansi:** Program Studi Informatika, Fakultas Ilmu Komputer, UPN "Veteran" Jawa Timur, 2026

## 1. Latar Belakang

Ruang kerja dan laboratorium yang penuh perangkat elektronik punya risiko panas berlebih (overheat) pada komputer, kabel, dan perangkat pendukung yang menyala lama. Pada tahap awal, perubahan konsentrasi gas seperti VOC dan CO biasanya terdeteksi lebih cepat dibanding perubahan suhu, sehingga risiko ini sering lolos kalau hanya mengandalkan suhu atau persepsi manusia. Data BPBD DKI Jakarta mencatat 1.148 dari 1.653 kasus kebakaran sepanjang 2023 sampai 2024 (sekitar 69,5%) disebabkan korsleting listrik.

IoT memungkinkan data sensor dikumpulkan terus menerus, tetapi data time series yang besar sulit dipisahkan antara normal dan anomali hanya dengan threshold sederhana. LSTM kuat menangkap dependensi temporal, tetapi pemakaian mandirinya cenderung supervised dan butuh label anomali. Autoencoder konvensional unsupervised lewat reconstruction error, tetapi lemah pada dependensi antar waktu. Kombinasi LSTM-Autoencoder menjawab keduanya: model hanya dilatih dari data normal, lalu anomali terdeteksi dari reconstruction error yang tinggi.

## 2. Rumusan Masalah

1. Bagaimana merancang dan mengimplementasi sistem monitoring kualitas udara berbasis IoT menggunakan metode LSTM-Autoencoder?
2. Bagaimana menerapkan LSTM-Autoencoder untuk mempelajari pola data normal dan mendeteksi anomali pada data time series kualitas udara?

## 3. Batasan Masalah

1. Lokasi: Laboratorium komputer SCR, Fakultas Ilmu Komputer UPN "Veteran" Jawa Timur, pukul 08.00 sampai 16.00 WIB selama 5 hari.
2. Parameter: gas mudah terbakar, CO, VOC, suhu, kelembapan (sensor MQ-2, MQ-7, MQ-135, AHT10).
3. Metode dibatasi pada LSTM-Autoencoder unsupervised, tanpa membandingkan dengan seluruh metode deep learning atau machine learning lain.
4. Evaluasi memakai precision, recall, F1-score, dan reconstruction error, tanpa dataset dari luar lokasi penelitian.
5. Model dilatih hanya dari kondisi normal, sehingga pengujian anomali memakai simulasi atau pola yang direkayasa, bukan kebakaran sungguhan.

## 4. Tujuan Penelitian

1. Merancang dan membangun sistem monitoring kualitas udara berbasis IoT yang mengumpulkan data gas mudah terbakar, CO, VOC, suhu, dan kelembapan secara real time.
2. Menerapkan LSTM-Autoencoder untuk mempelajari pola normal dan mendeteksi anomali berdasarkan reconstruction error.

## 5. Manfaat Penelitian

1. Referensi pengembangan deteksi anomali berbasis IoT dan deep learning pada data time series kualitas udara.
2. Rujukan bagi penelitian lanjutan dengan cakupan ruangan, parameter, atau metode yang lebih luas.
3. Meningkatkan kewaspadaan dini di laboratorium lewat peringatan visual, suara, dan notifikasi jarak jauh.
4. Prototipe awal bagi pengelola ruangan untuk mempertimbangkan sistem monitoring serupa.

## 6. Tinjauan Pustaka Singkat

- **Statistik, ML klasik, deep learning.** ARIMA mudah diinterpretasi tetapi terbatas pada data kompleks dan non-linear. SVM dan Isolation Forest fleksibel, tetapi performanya tidak konsisten antar metrik dan dataset serta masih butuh feature engineering manual (Audibert dkk.). LSTM-Autoencoder dipilih karena menangani autokorelasi kompleks pada data kualitas udara indoor (Wei dkk.).
- **Indoor air quality.** Laboratorium komputer berventilasi minim sehingga polutan menumpuk lebih cepat saat ada sumber baru.
- **Univariate vs multivariate.** Anomali sering muncul dari kombinasi antar sensor, jadi pendekatan multivariate dipilih.
- **Supervised vs unsupervised.** Data anomali berlabel langka dan tidak seimbang, jadi pendekatan unsupervised berbasis reconstruction error dipilih.

## 7. Metodologi

**Alur umum:** studi literatur, peninjauan lab SCR, perancangan dan fabrikasi alat IoT, kalibrasi dan uji sensor, pengambilan data, preprocessing, pemodelan LSTM-Autoencoder, penentuan threshold, integrasi alat, dashboard Blynk dan notifikasi WhatsApp bot, penyusunan laporan.

**Perangkat keras:** ESP32 DevKit V1, MQ-2, MQ-7, MQ-135, AHT10, LCD 20x4 I2C, LED merah dan hijau, buzzer.

**Pengambilan data:** interval 30 detik, 5 hari kerja, 08.00 sampai 16.00 WIB, sekitar 960 sampel per hari dan sekitar 4.800 sampel per parameter. Data dikirim dari ESP32 ke laptop lewat serial USB dan disimpan sebagai CSV.

**Preprocessing:**
1. Data cleaning: interpolasi linear untuk missing value, filter rentang fisis sensor, deteksi outlier rolling window, pemeriksaan rate of change, dan pencocokan dengan catatan kondisi ruangan.
2. Normalisasi Min-Max 0 sampai 1, statistik dihitung hanya dari data latih.
3. Sliding window 10 sampai 20 time step, stride 1.
4. Split: data latih 70% dan validasi 30% dari data normal. Data uji disusun terpisah dari data normal yang tidak dipakai latih ditambah data simulasi anomali.

**Arsitektur model:**
- Encoder: 2 layer LSTM (64 unit lalu bottleneck 8 sampai 16 unit), aktivasi tanh.
- RepeatVector sepanjang T.
- Decoder: 2 layer LSTM simetris, lalu TimeDistributed Dense 5 fitur dengan aktivasi linear.
- Dropout 0,1 sampai 0,2.
- Loss MAE, optimizer Adam (learning rate 0,001), 100 epoch dengan early stopping (patience 10), batch size 32.

**Threshold:** nilai reconstruction error maksimum pada data validasi. Sequence baru dengan error di atas threshold diklasifikasikan sebagai anomali dan memicu LED merah, buzzer, LCD, dashboard Blynk, serta notifikasi WhatsApp.

## 8. Evaluasi

Accuracy, precision, recall, dan F1-score dari confusion matrix, ditambah analisis reconstruction error. Rincian ada di [05_rencana_evaluation_metric.md](05_rencana_evaluation_metric.md).

## 9. Jadwal Penelitian (4 Bulan)

| Bulan | Kegiatan |
|---|---|
| 1 | Studi literatur, peninjauan lab, perancangan dan fabrikasi alat, kalibrasi sensor |
| 2 | Pengambilan data normal 5 hari, preprocessing, simulasi data anomali |
| 3 | Pemodelan LSTM-Autoencoder, tuning, penentuan threshold, evaluasi |
| 4 | Integrasi IoT, dashboard Blynk, notifikasi WhatsApp, pengujian, penyusunan laporan |

## 10. Daftar Pustaka Utama

Referensi lengkap mengikuti Daftar Pustaka pada dokumen pra-skripsi. Rujukan inti:

1. Y. Wei dkk., "LSTM-Autoencoder-Based Anomaly Detection for Indoor Air Quality Time-Series Data," IEEE Sensors Journal, vol. 23, no. 4, 2023.
2. J. Park, Y. Seo, J. Cho, "Unsupervised outlier detection for time-series data of indoor air quality using LSTM autoencoder with ensemble method," Journal of Big Data, vol. 10, 2023.
3. J. Audibert dkk., "Do Deep Neural Networks Contribute to Multivariate Time Series Anomaly Detection?" 2022.
4. M. A. Belay dkk., "Unsupervised Anomaly Detection for IoT-Based Multivariate Time Series," Sensors, 2023.
5. R. N. Pietraru dkk., "Contributions to the Development of Fire Detection and Intervention Capabilities Using an Indoor Air Quality IoT Monitoring System," Sensors, vol. 25, no. 20, 2025.
6. Z. Z. Darban dkk., "Deep Learning for Time Series Anomaly Detection: A Survey," ACM Computing Surveys, vol. 57, no. 1, 2024.
