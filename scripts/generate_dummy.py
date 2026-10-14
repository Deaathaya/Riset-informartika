"""
Generator dataset DUMMY untuk riset deteksi anomali kualitas udara.
Data ini sintetis, bukan hasil pengukuran sensor asli. Gunakan hanya untuk
menguji pipeline (preprocessing, windowing, LSTM-Autoencoder, evaluasi)
sebelum data asli dari Laboratorium SCR terkumpul.

Keluaran:
  data/raw/dataset_dummy_normal.csv            5 hari, kondisi normal (data latih dan validasi)
  data/test_anomaly/dataset_dummy_uji.csv      1 hari, normal + anomali simulasi (data uji)
  data/test_anomaly/log_skenario_anomali.csv   catatan waktu dan jenis anomali

Jalankan dari root repo:  python scripts/generate_dummy.py
"""
import os
import numpy as np
import pandas as pd

SEED = 42
INTERVAL_DETIK = 30
JAM_MULAI, JAM_SELESAI = 8, 16          # 08.00 sampai 16.00 WIB
SAMPEL_PER_HARI = (JAM_SELESAI - JAM_MULAI) * 3600 // INTERVAL_DETIK   # 960
HARI_LATIH = 5
TANGGAL_MULAI_LATIH = "2026-10-05"       # Senin
TANGGAL_UJI = "2026-10-12"               # Senin berikutnya
PERSEN_MISSING = 0.003                   # sebagian kecil NaN untuk latihan data cleaning

rng = np.random.default_rng(SEED)


def ar1(n, phi, sigma):
    """Noise autokorelasi (AR1) agar data tidak terlalu acak."""
    e = rng.normal(0, sigma, n)
    x = np.zeros(n)
    for i in range(1, n):
        x[i] = phi * x[i - 1] + e[i]
    return x


def satu_hari_normal(tanggal):
    n = SAMPEL_PER_HARI
    t = np.arange(n)
    waktu = pd.date_range(f"{tanggal} {JAM_MULAI:02d}:00:00", periods=n, freq=f"{INTERVAL_DETIK}s")
    frac = t / n                                   # 0 sampai 1 sepanjang hari

    # Suhu: naik pelan sepanjang hari + siklus AC kecil
    base_suhu = rng.uniform(25.0, 26.0)
    suhu = base_suhu + 1.2 * frac + 0.35 * np.sin(2 * np.pi * t / 120) + ar1(n, 0.95, 0.03)

    # Kelembapan: berlawanan arah dengan suhu
    base_rh = rng.uniform(58.0, 62.0)
    rh = base_rh - 4.5 * frac - 1.2 * np.sin(2 * np.pi * t / 120) + ar1(n, 0.95, 0.12)

    # Gas: baseline stabil, sedikit terpengaruh suhu, plus noise
    mq2 = 310 + 6 * (suhu - suhu.mean()) + ar1(n, 0.9, 2.0)
    mq135 = 520 + 25 * frac + 8 * (suhu - suhu.mean()) + ar1(n, 0.92, 2.5)
    mq7 = 4.5 + 0.25 * (suhu - suhu.mean()) + ar1(n, 0.9, 0.08)

    return pd.DataFrame({
        "timestamp": waktu,
        "mq2_ppm": mq2,
        "mq135_ppm": mq135,
        "mq7_ppm": mq7,
        "suhu_c": suhu,
        "rh_persen": rh,
    })


def tambah_anomali(df):
    """Suntik anomali simulasi ke satu hari data. Mengembalikan df berlabel dan log."""
    df = df.copy()
    df["label"] = 0
    df["skenario"] = ""
    log = []

    def segmen(mulai_menit, durasi_menit):
        a = mulai_menit * 60 // INTERVAL_DETIK
        b = a + durasi_menit * 60 // INTERVAL_DETIK
        return a, b

    def profil(m, naik_frac=0.25):
        """Naik cepat, bertahan, lalu turun. Bentuk 0 sampai 1."""
        p = np.ones(m)
        k = max(int(m * naik_frac), 1)
        p[:k] = np.linspace(0, 1, k)
        p[-k:] = np.linspace(1, 0, k)
        return p

    skenario = [
        # nama, mulai (menit dari 08.00), durasi menit
        ("lonjakan_gas", 60, 8),
        ("lonjakan_voc", 150, 10),
        ("suhu_naik_bertahap", 240, 20),
        ("multivariat", 380, 12),
    ]

    for nama, mulai, dur in skenario:
        a, b = segmen(mulai, dur)
        m = b - a
        p = profil(m, 0.5 if nama == "suhu_naik_bertahap" else 0.25)
        if nama == "lonjakan_gas":
            df.loc[a:b - 1, "mq2_ppm"] += 380 * p
            df.loc[a:b - 1, "mq7_ppm"] += 9 * p
        elif nama == "lonjakan_voc":
            df.loc[a:b - 1, "mq135_ppm"] += 260 * p
        elif nama == "suhu_naik_bertahap":
            df.loc[a:b - 1, "suhu_c"] += 5.5 * p
            df.loc[a:b - 1, "rh_persen"] -= 9 * p
            df.loc[a:b - 1, "mq2_ppm"] += 60 * p
        elif nama == "multivariat":
            df.loc[a:b - 1, "mq2_ppm"] += 220 * p
            df.loc[a:b - 1, "mq7_ppm"] += 5 * p
            df.loc[a:b - 1, "mq135_ppm"] += 140 * p
            df.loc[a:b - 1, "suhu_c"] += 3.0 * p
            df.loc[a:b - 1, "rh_persen"] -= 5 * p
        df.loc[a:b - 1, "label"] = 1
        df.loc[a:b - 1, "skenario"] = nama
        log.append({
            "skenario": nama,
            "waktu_mulai": df.loc[a, "timestamp"],
            "waktu_selesai": df.loc[b - 1, "timestamp"],
            "jumlah_sampel": m,
        })
    return df, pd.DataFrame(log)


def bulatkan(df):
    df["mq2_ppm"] = df["mq2_ppm"].round(2)
    df["mq135_ppm"] = df["mq135_ppm"].round(2)
    df["mq7_ppm"] = df["mq7_ppm"].round(3)
    df["suhu_c"] = df["suhu_c"].round(2)
    df["rh_persen"] = df["rh_persen"].round(2)
    return df


def main():
    os.makedirs("data/raw", exist_ok=True)
    os.makedirs("data/test_anomaly", exist_ok=True)

    # Data normal 5 hari kerja berturut-turut
    hari = pd.bdate_range(TANGGAL_MULAI_LATIH, periods=HARI_LATIH)
    latih = pd.concat([satu_hari_normal(d.strftime("%Y-%m-%d")) for d in hari], ignore_index=True)
    latih = bulatkan(latih)

    # Sisipkan missing value acak pada sensor gas dan AHT10 (untuk latihan interpolasi)
    kolom_sensor = ["mq2_ppm", "mq135_ppm", "mq7_ppm", "suhu_c", "rh_persen"]
    for k in kolom_sensor:
        idx = rng.choice(len(latih), size=int(len(latih) * PERSEN_MISSING), replace=False)
        latih.loc[idx, k] = np.nan
    latih.to_csv("data/raw/dataset_dummy_normal.csv", index=False)

    # Data uji: satu hari terpisah dengan anomali simulasi
    uji = bulatkan(satu_hari_normal(TANGGAL_UJI))
    uji, log = tambah_anomali(uji)
    uji = bulatkan(uji)
    uji.drop(columns=["skenario"]).to_csv("data/test_anomaly/dataset_dummy_uji.csv", index=False)
    log.to_csv("data/test_anomaly/log_skenario_anomali.csv", index=False)

    print("Data latih :", latih.shape)
    print("Data uji   :", uji.shape, "| anomali:", int(uji['label'].sum()))
    print(log.to_string(index=False))


if __name__ == "__main__":
    main()
