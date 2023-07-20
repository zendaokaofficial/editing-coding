import streamlit as st
import pandas as pd
from datetime import date
import time
from streamlit_js_eval import streamlit_js_eval
import gspread
import streamlit as st
from google.oauth2 import service_account
from oauth2client.service_account import ServiceAccountCredentials
from gsheetsdb import connect
import datetime
import json
import pytz

tzInfo = pytz.timezone('Asia/Hong_Kong')
# Create a connection object.
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('st2023-tabanan-ebaa52f9499e.json', scope)
client = gspread.authorize(creds)

# Make sure you use the right name here.
sheet = client.open("Editing-Coding")
worksheet1 = sheet.worksheet('Sheet1')

## Membaca db asal
sheet_url = "https://docs.google.com/spreadsheets/d/13BbpP9ox-XCo3xB74eTTG0oFoI_aIt6w_BP-4hU3Sjg/edit#gid=0"
url_1 = sheet_url.replace('/edit#gid=', '/export?format=csv&gid=')

df = pd.read_csv(url_1, header=0, )
df["ID SLS"] = df["ID SLS"].astype(str)
hari = date.today()

if __name__ == "__main__":
    st.markdown("<h1 style='text-align: center; color: green;'>Isikan Form Editing Coding</h1>", unsafe_allow_html=True)
    st.subheader(f"Tanggal: {hari}")

    lstKecamatan = list(df["Nama Kecamatan"].unique())
    lstKecamatan.insert(0, "PILIH KECAMATAN")
              
    FirstFilter = st.selectbox("Nama Kecamatan", lstKecamatan, 0)

    if FirstFilter != 'PILIH KECAMATAN':

        df2 = df[df["Nama Kecamatan"] == FirstFilter]  

        lstDesa = list(df2["Nama Desa"].unique())
        lstDesa.insert(0, "PILIH DESA")

        SecondFilter = st.selectbox("Nama Desa", lstDesa, 0)

        if SecondFilter != 'PILIH DESA':

            df3 = df2[df2["Nama Desa"] == SecondFilter]

            lstSLS = list(df3["Nama SLS"].unique())
            lstSLS.insert(0, "PILIH SLS")

            ThirdFilter = st.selectbox("Nama SLS", lstSLS, 0)

            if ThirdFilter != "PILIH SLS":

                df4 = df3[df3["Nama SLS"] == ThirdFilter]

                lstIDSLS = list(df4["ID SLS"].unique())
                lstIDSLS.insert(0, "PILIH ID SLS")

                ThirdForthFilter = st.selectbox("ID SLS", lstIDSLS, 0)

                if ThirdForthFilter != "PILIH ID SLS":

                    nmpetugas = ["PILIH NAMA PETUGAS", "I Gede Putu Sopyan Adina Putra",
                                 "Luh Ade Resi Puspitasari",
                                 "Ni Putu Eka Arini",
                                 "Ni Komang Ayu Rimayani",
                                 "I Gusti Made Saputra Landep",
                                 "Ni Luh Putu Sintia Dewi",
                                 "Ni Kadek Chita Dwi Chayani",
                                 "I Made Yuda Prana Cita",
                                 "Ni Nyoman Mona Purwaningtias",
                                 "Ni Luh Putu Ayu Sri Wulandari",
                                 "I Gusti Ayu Made Desi Dwi Yanti"]
                    
                    statusdok = ["PILIH STATUS DOKUMEN", "Selesai Editing Coding", "Dikembalikan ke Koseka"]
                    
                    nmpetugasselect = st.selectbox("NAMA PETUGAS EDITING CODING", nmpetugas, 0)

                    jumlahL2 = st.text_input('Jumlah dokumen L2', )

                    statusdokumen = st.selectbox('STATUS DOKUMEN', statusdok, 0)

                    lstPML = list(df4["Nama PML"].unique())
                    lstPML.insert(0, "PILIH PML")

                    namaPML = st.selectbox('NAMA PML', lstPML, 0)

                    skor = st.text_input('Nilai PML untuk SLS/Sub SLS ini. Rentang 1-10')

                    if ((nmpetugasselect != "PILIH NAMA PETUGAS") and len(jumlahL2) != 0 and (statusdokumen != "PILIH STATUS DOKUMEN") and (namaPML != "PILIH PML") and len(skor) != 0):
                        if st.button("Submit"):
                            st.success(f'Data berhasil tersubmit', icon="✅")
                            worksheet1.append_row([datetime.datetime.now(tz=tzInfo).isoformat(), FirstFilter, SecondFilter, ThirdFilter, ThirdForthFilter, nmpetugasselect, int(jumlahL2), statusdokumen, namaPML, skor])
                            time.sleep(3)
                            streamlit_js_eval(js_expressions="parent.window.location.reload()")
