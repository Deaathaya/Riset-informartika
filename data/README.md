# Dataset Dummy

Data di folder ini SINTETIS (hasil generator `scripts/generate_dummy.py`, seed 42), bukan pengukuran sensor asli. Fungsinya untuk menguji pipeline sebelum data asli Laboratorium SCR terkumpul. Ganti dengan data asli saat sudah ada.

| Berkas | Isi |
|---|---|
| `raw/dataset_dummy_normal.csv` | 5 hari kerja, 08.00 sampai 16.00, interval 30 detik, 4.800 baris, kondisi normal. Ada sekitar 0,3% nilai kosong per kolom untuk latihan interpolasi |
| `test_anomaly/dataset_dummy_uji.csv` | 1 hari terpisah, 960 baris, berisi 4 skenario anomali, kolom `label` (0 normal, 1 anomali) |
| `test_anomaly/log_skenario_anomali.csv` | Waktu mulai, selesai, dan jenis tiap skenario anomali |

## Kolom

| Kolom | Satuan | Sensor |
|---|---|---|
| timestamp | WIB | penanda waktu |
| mq2_ppm | ppm | MQ-2 (gas mudah terbakar dan asap) |
| mq135_ppm | ppm | MQ-135 (VOC) |
| mq7_ppm | ppm | MQ-7 (CO) |
| suhu_c | °C | AHT10 |
| rh_persen | %RH | AHT10 |
| label | 0/1 | hanya pada data uji |

Jalankan ulang dengan `python scripts/generate_dummy.py` dari root repo (butuh numpy dan pandas).
