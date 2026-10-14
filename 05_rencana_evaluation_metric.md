# Rencana Evaluation Metric

Anomali diposisikan sebagai kelas positif. Model dilatih tanpa label, sedangkan label hanya dipakai pada data uji untuk mengukur performa.

## 1. Confusion Matrix

| | Prediksi anomali | Prediksi normal |
|---|---|---|
| **Aktual anomali** | TP | FN |
| **Aktual normal** | FP | TN |

- TP: anomali yang berhasil diprediksi sebagai anomali
- TN: normal yang diprediksi normal
- FP: normal yang salah diprediksi anomali (alarm palsu)
- FN: anomali yang salah diprediksi normal (bahaya terlewat)

## 2. Metrik Utama (sesuai proposal)

**Accuracy**

```
Accuracy = (TP + TN) / (TP + TN + FP + FN)
```

**Precision**: dari semua yang diprediksi anomali, berapa yang benar benar anomali.

```
Precision = TP / (TP + FP)
```

**Recall**: dari semua anomali sebenarnya, berapa yang berhasil terdeteksi.

```
Recall = TP / (TP + FN)
```

**F1-score**: rata rata harmonik precision dan recall.

```
F1 = 2 x Precision x Recall / (Precision + Recall)
```

Accuracy saja tidak cukup karena data tidak seimbang (data normal jauh lebih banyak dari anomali), jadi precision, recall, dan F1 menjadi acuan utama. Pada konteks deteksi dini asap, recall diprioritaskan karena FN lebih berbahaya daripada FP.

## 3. Metrik Reconstruction Error

**Loss training (MAE)**

```
MAE = (1/n) x sum(|x_i - x_hat_i|)
```

dengan x_i nilai input ternormalisasi dan x_hat_i hasil rekonstruksi decoder. Kurva training loss dan validation loss dipantau selama pelatihan. Jika validation loss jauh di atas training loss, itu tanda overfitting.

**Threshold**

```
Threshold = max(RE pada sequence data validasi)
```

Sequence dengan RE di atas threshold diklasifikasikan sebagai anomali.

## 4. Metrik Tambahan yang Direncanakan

Metrik ini melengkapi metrik utama dan tidak mengubah batasan masalah di proposal.

| Metrik | Fungsi |
|---|---|
| False alarm rate = FP / (FP + TN) | Mengukur seberapa sering alarm palsu muncul pada kondisi normal |
| Detection delay | Selisih waktu antara awal anomali simulasi dan alarm pertama, penting untuk klaim deteksi dini |
| Rata rata RE normal vs anomali | Melihat seberapa jauh pemisahan distribusi error |
| Recall per skenario anomali | Melihat skenario mana yang paling sulit terdeteksi |
| ROC-AUC dan PR-AUC | Menilai kualitas skor RE tanpa bergantung pada satu threshold |

## 5. Rencana Pelaporan

1. Tabel confusion matrix pada data uji.
2. Tabel accuracy, precision, recall, F1, dan false alarm rate.
3. Grafik reconstruction error terhadap waktu dengan garis threshold.
4. Histogram RE data normal vs anomali.
5. Kurva training dan validation loss.
6. Tabel recall dan detection delay per skenario anomali.

## 6. Analisis Sensitivitas Threshold

Karena threshold berupa nilai maksimum, ia sensitif terhadap outlier pada data validasi. Sebagai pembanding, nilai threshold alternatif (misalnya persentil 99 dari RE validasi) dapat diuji, lalu hasil precision, recall, dan F1 dibandingkan.

## 7. Catatan Konsistensi dengan Proposal

Persamaan (2.5) di Bab II menyebut threshold diambil dari seluruh sequence data latih, sedangkan Subbab 3.4.7 menyebut data validasi. Dokumen ini memakai data validasi agar konsisten dengan Bab III.
