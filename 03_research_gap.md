# Research Gap

## 1. Ringkasan Penelitian Terdahulu

| Kelompok | Contoh | Kekuatan | Keterbatasan |
|---|---|---|---|
| Statistik konvensional | ARIMA (Pahari dan Kumain) | Ringan dan mudah diinterpretasi | Kurang baik pada data kompleks dan non-linear, biasanya perlu digabung dengan deep learning |
| Machine learning klasik | SVM, Isolation Forest (Audibert dkk.; Amanda dkk.) | Fleksibel, tanpa asumsi distribusi | Performa tidak konsisten antar metrik dan dataset, butuh feature engineering manual |
| Deep learning terawasi | LSTM untuk prediksi atau klasifikasi | Kuat pada pola temporal | Butuh label anomali yang memadai, padahal anomali langka dan data tidak seimbang |
| Autoencoder biasa | Fully-connected autoencoder | Unsupervised lewat reconstruction error | Lemah pada dependensi antar waktu |
| LSTM-Autoencoder indoor air quality | Wei dkk. (2023); Park dkk. (2023) | Unsupervised dan menangkap temporal dependency | Berfokus pada deteksi outlier kualitas udara umum, bukan indikasi awal asap pada ruang berisi perangkat elektronik |
| Deteksi kebakaran berbasis sensor gas IoT | Pietraru dkk. (2025); Daud dkk. | Memakai CO, VOC, suhu sebagai penanda dini | Banyak yang mengandalkan threshold sederhana atau aturan tetap |

## 2. Gap yang Diidentifikasi

**Gap 1: Threshold sederhana belum cukup untuk time series multivariat.**
Sistem IoT deteksi asap dan kebakaran umumnya memakai ambang batas pada nilai sensor. Pendekatan ini tidak melihat pola antar waktu dan korelasi antar sensor, sehingga anomali yang baru terlihat dari kombinasi parameter bisa terlewat.

**Gap 2: LSTM-Autoencoder untuk indoor air quality belum diarahkan ke deteksi dini asap akibat overheat perangkat elektronik.**
Penelitian LSTM-Autoencoder pada kualitas udara dalam ruangan berfokus pada deteksi outlier data kualitas udara. Konteks laboratorium komputer dengan risiko overheat, dengan sensor gas MQ-2, MQ-7, MQ-135 dan AHT10, belum banyak dibahas.

**Gap 3: Data anomali berlabel sulit diperoleh untuk kasus kebakaran.**
Pendekatan supervised butuh data anomali berlabel dalam jumlah besar. Pada kasus asap atau kebakaran data seperti itu langka dan berbahaya untuk dibuat. Penelitian ini memakai pendekatan unsupervised yang hanya dilatih dari data normal.

**Gap 4: Sistem sering berhenti di model, belum sampai peringatan end to end.**
Banyak studi berhenti pada akurasi model. Penelitian ini menghubungkan hasil deteksi ke LED, buzzer, LCD, dashboard Blynk, dan notifikasi WhatsApp bot, karena inference LSTM-Autoencoder dijalankan di laptop lewat komunikasi serial dengan ESP32.

## 3. Posisi Penelitian

Penelitian ini mengisi celah dengan kombinasi berikut:

1. Data multivariat lima fitur (gas mudah terbakar, CO, VOC, suhu, kelembapan) dari sensor murah berbasis ESP32.
2. LSTM-Autoencoder unsupervised yang hanya dilatih dari data kondisi normal.
3. Konteks laboratorium komputer sebagai ruang berisiko overheat.
4. Integrasi sampai peringatan lokal dan jarak jauh.

## 4. Pertanyaan Riset yang Muncul

1. Seberapa baik LSTM-Autoencoder membedakan kondisi normal dan anomali pada data sensor lab SCR?
2. Apakah threshold dari reconstruction error maksimum cukup stabil, atau terlalu longgar jika ada noise pada data latih?
3. Skenario anomali apa yang paling sulit terdeteksi (misalnya kenaikan suhu bertahap dibanding lonjakan gas)?

## 5. Keterbatasan yang Diakui

1. Data hanya dari satu lokasi dan 5 hari, sehingga generalisasi terbatas.
2. Anomali berupa simulasi, bukan kejadian kebakaran nyata.
3. Tidak ada perbandingan langsung dengan metode lain pada penelitian ini (sesuai batasan masalah). Perbandingan dengan baseline seperti Isolation Forest atau autoencoder biasa bisa jadi pengembangan lanjutan.
4. Sensor MQ sensitif terhadap suhu dan kelembapan serta butuh kalibrasi, sehingga drift sensor bisa memengaruhi pola normal.
