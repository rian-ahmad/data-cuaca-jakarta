# Sumber data cuaca: BMKG (Badan Meteorologi, Klimatologi, dan Geofisika) https://data.bmkg.go.id/prakiraan-cuaca/
# Sumber data kode wilayah: https://kodewilayah.id/

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import pandas as pd
import json
import time
import logging
from tqdm import tqdm
import config


# ---------------- Logging ----------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("pipeline.log")
    ]
)


# ---------------- Retry Session ----------------
def buat_session(max_retries=config.MAX_RETRIES, backoff_factor=config.BACKOFF_FACTOR):
    """Buat requests session dengan retry otomatis"""
    session = requests.Session()
    retries = Retry(
        total=max_retries,
        backoff_factor=backoff_factor,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"]
    )
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    return session


# ---------------- Data Functions ----------------
def prakiraan_cuaca(data, kode_adm4):
    df_lokasi = pd.json_normalize(data["data"][0]["lokasi"])
    df_lokasi["Kode adm4"] = kode_adm4

    cuaca = [c for d in data["data"][0]["cuaca"] for c in d]
    df_cuaca = pd.json_normalize(cuaca)

    df_prakiraan_cuaca = df_lokasi.join(df_cuaca, how="right")
    df_prakiraan_cuaca.fillna(df_lokasi.iloc[0], inplace=True)

    return df_prakiraan_cuaca


def ambil_kode_wilayah_jakarta():
    """Ambil kode wilayah desa/kelurahan di DKI Jakarta dari dataset permendagri"""
    df_kode_wilayah = pd.read_csv(
        "https://raw.githubusercontent.com/kodewilayah/permendagri-72-2019/main/dist/base.csv",
        header=None,
        names=["Kode", "Wilayah"]
    )

    df_jakarta = (
        df_kode_wilayah
        .query("Kode.str.startswith('31') and Kode.str.len() == 13")
        .reset_index(drop=True)
    )

    return df_jakarta


def ambil_data_cuaca(df_kode_wilayah_jakarta, delay=config.REQUEST_DELAY):
    """Ambil data cuaca BMKG untuk seluruh kode wilayah Jakarta"""
    all_data = []
    session = buat_session()

    for kode in tqdm(df_kode_wilayah_jakarta["Kode"], desc="Mengambil data cuaca"):
        try:
            res = session.get(f"{config.API_URL}?adm4={kode}", timeout=10)
            res.raise_for_status()
            data = res.json()
            all_data.append(prakiraan_cuaca(data, kode))

        except requests.RequestException as e:
            logging.error(f"Gagal ambil data untuk kode {kode}: {e}")

        finally:
            time.sleep(delay)

    return pd.concat(all_data, ignore_index=True)


def bersihkan_data(df):
    rename_map = {
        "provinsi": "Provinsi",
        "kotkab": "Kota/Kabupaten",
        "kecamatan": "Kecamatan",
        "desa": "Desa",
        "local_datetime": "Waktu Lokal",
        "t": "Suhu Udara (c)",
        "hu": "Kelembapan",
        "weather_desc": "Kondisi Cuaca",
        "ws": "Kecepatan Angin (Km/Jam)",
        "vs": "Jarak Pandang (m)",
    }
    df = df.rename(columns=rename_map)
    return df[
        ["Provinsi", "Kota/Kabupaten", "Kecamatan", "Desa", "Kode adm4",
         "Waktu Lokal", "Suhu Udara (c)", "Kelembapan", "Kondisi Cuaca",
         "Kecepatan Angin (Km/Jam)", "Jarak Pandang (m)"]
    ]


def buat_docs(df):
    def make_doc(row):
        return {
            "id": f"{row['Kode adm4']}_{row['Waktu Lokal'].replace(' ', '_')}",
            "text": (
                f"Cuaca di desa {row['Desa']} (kode {row['Kode adm4']}) "
                f"pada {row['Waktu Lokal']} adalah {row['Kondisi Cuaca']} "
                f"dengan suhu {row['Suhu Udara (c)']}°C, "
                f"kelembapan {row['Kelembapan']}%, "
                f"dan kecepatan angin {row['Kecepatan Angin (Km/Jam)']} km/jam."
            ),
            "metadata": row.to_dict()
        }
    return df.apply(make_doc, axis=1).tolist()


def simpan_json(docs, filename=config.OUTPUT_FILE):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(docs, f, ensure_ascii=False, indent=2)


# ---------------- Main ----------------
if __name__ == "__main__":
    logging.info("Pipeline dimulai")
    try:
        logging.info("Mengambil dataset kode wilayah dari permendagri")
        df_kode = ambil_kode_wilayah_jakarta()

        logging.info("Mengambil data cuaca dari BMKG")
        df_raw = ambil_data_cuaca(df_kode)

        logging.info("Membersihkan data")
        df_bersih = bersihkan_data(df_raw)

        logging.info("Menyimpan JSON")
        docs = buat_docs(df_bersih)
        simpan_json(docs)

        logging.info(f"Pipeline selesai. Data cuaca disimpan ke {config.OUTPUT_FILE}")
    
    except Exception as e:
        logging.exception(f"Pipeline gagal: {e}")
