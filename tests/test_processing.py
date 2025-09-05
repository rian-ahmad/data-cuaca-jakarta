import json
import pandas as pd
from processing_cuaca_jakarta import bersihkan_data, buat_docs

def test_bersihkan_data():
    df = pd.DataFrame([{
        "provinsi": "DKI Jakarta",
        "kotkab": "Jakarta Selatan",
        "kecamatan": "Tebet",
        "desa": "Manggarai",
        "Kode adm4": "3175070001002001",
        "local_datetime": "2025-09-05 10:00:00",
        "t": 30,
        "hu": 75,
        "weather_desc": "Cerah",
        "ws": 5,
        "vs": 6000
    }])
    df_clean = bersihkan_data(df)
    assert "Provinsi" in df_clean.columns
    assert df_clean.loc[0, "Suhu Udara (c)"] == 30

def test_buat_docs():
    df = pd.DataFrame([{
        "Provinsi": "DKI Jakarta",
        "Kota/Kabupaten": "Jakarta Selatan",
        "Kecamatan": "Tebet",
        "Desa": "Manggarai",
        "Kode adm4": "3175070001002001",
        "Waktu Lokal": "2025-09-05 10:00:00",
        "Suhu Udara (c)": 30,
        "Kelembapan": 75,
        "Kondisi Cuaca": "Cerah",
        "Kecepatan Angin (Km/Jam)": 5,
        "Jarak Pandang (m)": 6000
    }])
    docs = buat_docs(df)
    assert isinstance(docs, list)
    assert "text" in docs[0]
    assert "metadata" in docs[0]
