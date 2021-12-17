
import pandas as pd
import json
import matplotlib.pyplot as plt
from matplotlib import cm
import streamlit as st
from PIL import Image


#******************************************DEFINISI AWAL-START********************************************

#READ DATA
data = pd.read_csv("produksi_minyak_mentah.csv")
df = pd.DataFrame(data)

#KODE JSON
list_json_kode = []
file = open("kode_negara_lengkap.json")
data_json = json.loads(file.read())
for i in range(len(data_json)):
    x = data_json[i]["alpha-3"]
    list_json_kode.append(x)

#KODE BUKAN NEGARA
list_bukan_negara = []
for i in list(df["kode_negara"].unique()):
    if not i in list_json_kode:
        list_bukan_negara.append(i)

#KODE NEGARA CSV
def list_satu_negara():
    list_satu_negara = []
    for i in list(df["kode_negara"].unique()):
        if not i in list_bukan_negara:
            list_satu_negara.append(i)
    return list_satu_negara


#KODE UBAH KE NAMA ASLI DAN SEBALIKNYA
list_negara_fix = []
list_pilihan = []
list_pilihan1 = []
for nama in list_satu_negara():
    for i in range(len(data_json)):
        if data_json[i]["alpha-3"]==nama:
            x = data_json[i]["name"]
            y = data_json[i]["alpha-3"]
            new = x,y
            new1 = y,x
            list_negara_fix.append(x)
            list_pilihan.append(new)
            list_pilihan1.append(new1)
list_negara_fix.sort()
list_pilihan.sort()
Inputan = dict(list_pilihan)#NAMA KE KODE
Inputan1 = dict(list_pilihan1)#KODE KE NAMA

#RENTANG TAHUN / UNTUK MENU 4
awal_tahun = df["tahun"][0]
akhir_tahun = df["tahun"][len(df.index)-1]
list_tahun_fix = [i+awal_tahun for i in range(akhir_tahun-awal_tahun+1)]

#CARI BIODATA SUATU NEGARA
def json(siapa_kode):#info negara
    import json
    x = open("kode_negara_lengkap.json")
    y = json.loads(x.read())
    for i in range(len(y)):
        if y[i]["alpha-3"]==siapa_kode:
            return i
#******************************************DEFINISI AWAL-END********************************************



#******************************************TAMPILAN AWAL-START********************************************
#SIDEBAR
#st.set_page_config(layout="wide")
st.set_page_config(page_title="JDX", layout="wide")

image = Image.open("rig.png")
st.sidebar.image(image)


#st.sidebar.subheader("Menu Utama")
list_menu = ["Deskripsi","Fitur A","Fitur B","Fitur C","Fitur D"]
menu_view = st.sidebar.radio("Pilih Fitur",list_menu)

def menu_main():
    if menu_view == "Deskripsi":
        return deskripsi()
    if menu_view == "Fitur A":
        return fitur_A()
    if menu_view == "Fitur B":
        return fitur_B()
    if menu_view == "Fitur C":
        return fitur_C()
    if menu_view == "Fitur D":
        return fitur_D()

def deskripsi(): 
    st.title("📄 Welcome !!!")
    st.sidebar.subheader("")
    st.subheader("Berikut penjelasan singkat mengenai fitur")
    
    st.subheader("📌 Fitur A :")
    st.markdown("Menampilkan dan memberikan info production history minyak mentah pada suatu negara tiap tahunnya.")
    st.markdown("---")
    st.subheader("📌 Fitur B :")
    st.markdown("Menampilkan dan memberikan info negara dengan urutan produksi minyak mentah terbesar ke terkecil (bukan nol) pada suatu tahun tertentu.")
    st.markdown("---")
    st.subheader("📌 Fitur C :")
    st.markdown("Menampilkan dan memberikan info negara dengan urutan produksi minyak mentah terbesar ke terkecil (bukan nol) berdasarkan produksi kumulatifnya (seluruh tahun).")
    st.markdown("---")
    st.subheader("📌 Fitur D :")
    st.markdown("Memberikan info negara yang memiliki produksi minyak mentah terbesar, terkecil, atau nol pada suatu tahun atau secara kumulatif (seluruh tahun)")


#******************************************TAMPILAN AWAL-END********************************************


#****************************************** FITUR - START ********************************************
def fitur_A():
    st.title(":chart_with_upwards_trend: FITUR A")
    st.sidebar.markdown("**Deskripsi Fitur A : **")
    st.sidebar.markdown("Menampilkan dan memberikan info _production history_ **minyak mentah** pada suatu negara tiap tahunnya")
    negara_view = st.selectbox("Pilih Negara : ",list_negara_fix)
    
    list_tahun = []
    list_produksi = []
    for i in df.index:
        if df["kode_negara"][i]==Inputan[negara_view]:
            x=df["tahun"][i]
            y=df["produksi"][i]
            list_tahun.append(x)
            list_produksi.append(y)
    
    tahun = []
    for i in df.index:
        if df["kode_negara"][i]==Inputan[negara_view]:
            tahun.append(df["tahun"][i])
    
    #VISUALISASI
    plt.subplots(figsize=(12,7),dpi=200)
    #plt.axes().set_facecolor("whitesmoke")
    plt.fill_between(list_tahun,list_produksi,color="darkblue",alpha=0.7)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    plt.xlim([min(tahun),max(tahun)])
    plt.ylabel("Jumlah Produksi",fontsize = 18)
    plt.title("Grafik Produksi Minyak Mentah per Tahun Negara " + negara_view,fontsize = 20,fontweight="bold")
    plt.grid(axis="y",linestyle="--",color="black",linewidth=1)
    st.pyplot(plt)
    
    #LEGEND - UNTUK MELIHAT JUMLAH PRODUKSI
    st.markdown("*_Axis X pada grafik diatas berupa tahun.\nPilih tahun untuk melihat nilai produksi lebih detail._")
    
    left_col, right_col = st.columns(2)
    
    list_tahun = [i+tahun[0] for i in range(tahun[len(tahun)-1]-tahun[0]+1)]
    tahun_view = left_col.selectbox("Pilih tahun :",list_tahun)
    indeks = list_tahun.index(tahun_view)
    right_col.subheader("")
    right_col.subheader("**Produksi : **" + str(round(list_produksi[indeks],3)))
    
    st.markdown("---")
    
    left_col, right_col = st.columns(2)
    
    #SUMMARY:
    left_col.subheader("Summary:")
    if sum(list_produksi)==0.0:
        left_col.markdown("Berdasarkan data, negara " + negara_view + " tidak pernah memproduksikan minyak mentah.")
    if sum(list_produksi)!=0.0:
        tahun = list_tahun[list_produksi.index(max(list_produksi))]
        produksi = max(list_produksi)
        smallest = None
        for i in list_produksi:
            if i!=0.0:
                if smallest is None:
                    smallest = i
                if smallest > i:
                    smallest = i
        tahun1 = list_tahun[list_produksi.index(smallest)]
        produksi1 = smallest
        left_col.markdown("**Produksi terbesar : **"+ str(round(produksi,3)) + " (tahun " + str(tahun) + ")")
        left_col.markdown("**Produksi terkecil (bukan nol) **: "+ str(round(produksi1,3)) + " (tahun " + str(tahun1) + ")")
    
    
    #TABEL INFO NEGARA (JSON)
    right_col.subheader("Informasi Negara")
    x = data_json[json(Inputan[negara_view])]
    keys = []
    vals = []
    for key,val in x.items():
        keys.append(key)
        if val=="":
            vals.append("-")
        else:
            vals.append(val)

    df_A = pd.DataFrame({"Key":keys,"Value":vals})
    s = df_A.set_index("Key")
    right_col.dataframe(s.head(len(keys)))
    

def fitur_B():
    st.title(":bar_chart: FITUR B ")
    st.sidebar.markdown("**Deskripsi Fitur B : **")
    st.sidebar.markdown("Menampilkan dan memberikan info negara dengan urutan produksi **minyak mentah** terbesar ke terkecil (bukan nol) pada suatu tahun tertentu")
    
    left_col, right_col = st.columns(2)
    tahun_view = left_col.selectbox("Pilih Tahun : ",list_tahun_fix)
    
    tuple_besar_negara = []
    for i in df.index:
        if not df["kode_negara"][i] in list_bukan_negara:
            if df["tahun"][i]==tahun_view:
                if df["produksi"][i]!=0:
                    x=df["kode_negara"][i]
                    y=df["produksi"][i]
                    new=y,x
                    tuple_besar_negara.append(new)

    besar_view = right_col.number_input("Pilih Jumlah Negara : ",min_value=1,max_value=len(tuple_besar_negara),value=4)
    
    tuple_besar_negara.sort(reverse=True)
    list_nama_negara = [x for y,x in tuple_besar_negara[:besar_view]]
    list_produksi_negara = [y for y,x in tuple_besar_negara[:besar_view]]

    
    #VISUALISASI
    plt.subplots(figsize=(15,8),dpi=200)
    #plt.axes().set_facecolor("whitesmoke")
    cmap_name = "tab20b"
    cmap = cm.get_cmap(cmap_name)
    colors = cmap.colors[:len(list_nama_negara)]
    plt.bar(list_nama_negara,list_produksi_negara,color=colors)
    plt.xticks(list_nama_negara,fontsize=13,rotation = 45)
    plt.yticks(fontsize=15)
    plt.ylabel("Produksi",fontsize = 18)
    plt.title("Negara Produksi Minyak Mentah Terbesar",fontsize = 22,fontweight="bold")
    plt.grid(axis="y",linestyle="--")
    st.pyplot(plt)

    
    #LEGEND
    tuple_besar_negara1 = []
    for i in df.index:
        if not df["kode_negara"][i] in list_bukan_negara:
            if df["tahun"][i]==tahun_view:
                if df["produksi"][i] != 0:
                    x=df["kode_negara"][i]
                    y=df["produksi"][i]
                    new=y,x
                    tuple_besar_negara1.append(new)
    
    tuple_besar_negara1.sort(reverse=True)
    tabel = pd.DataFrame({"Negara" : pd.Series([Inputan1[x] for y,x in tuple_besar_negara1]),
                          "Kode" : pd.Series([x for y,x in tuple_besar_negara1]),
                          "Produksi" : pd.Series([y for y,x in tuple_besar_negara1])
                         })
    
    #LIAT URUTAN,NEGARA,PRODUKSI BERDASARKAN KODE
    
    st.markdown("*_Axis X pada grafik diatas berupa kode negara.\nPilih salah satu kode tersebut untuk melihat info lebih detail._")
    
    left_col, right_col = st.columns(2)
    
    list_nama_negara.sort()
    legend1 = left_col.selectbox("Pilih Kode Negara :",list_nama_negara)
    right_col.markdown("Negara : " + Inputan1[legend1])
    indeks1 = int(tabel[tabel["Negara"]==Inputan1[legend1]].index.values)
    right_col.markdown("Urutan : " + str(indeks1+1))
    right_col.markdown("Produksi : " + str(round(tabel["Produksi"][indeks1],3)))
    

    
    st.subheader("Info Seluruh Urutan Negara di Tahun " + str(tahun_view))
    st.markdown("Terdapat " + str(len(tabel["Negara"])) + " besar negara yang produksinya tidak nol.")
    st.markdown("Pilih negara untuk melihat urutannya  **ATAU**  pilih urutan untuk melihat info negaranya.")
    
    left_col, right_col = st.columns(2)
    
    #LIAT NEGARA,KODE,PRODUKSI BERDASARKAN URUTAN
    legend = right_col.number_input("Pilih Posisi/Urutan :",min_value=1,max_value=len(tuple_besar_negara1),value=1)
    nama_negara = [Inputan1[x] for y,x in tuple_besar_negara1][legend-1] 
    right_col.markdown("Negara : " + nama_negara)
    right_col.markdown("Kode : " + Inputan[nama_negara])
    indeks = [Inputan1[x] for y,x in tuple_besar_negara1].index(nama_negara)
    right_col.markdown("Produksi : " + str(round([y for y,x in tuple_besar_negara1][indeks],3)))

    
    #LIAT KODE,URUTAN,PRODUKSI BERDASARKAN NEGARA
    negara = [Inputan1[x] for y,x in tuple_besar_negara1]
    negara.sort()
    legend2 = left_col.selectbox("Pilih Negara :",negara)
    left_col.markdown("Kode : " + Inputan[legend2])
    indeks1 = int(tabel[tabel["Negara"]==legend2].index.values)
    left_col.markdown("Urutan : " + str(indeks1+1))
    left_col.markdown("Produksi : " + str(round(tabel["Produksi"][indeks1],3)))
    
    
    st.markdown("---")
    
    #TABEL LENGKAPNYA - PALING BAWAH
    st.markdown("*Berikut urutan negara dengan produksi terbesar hingga terkecil (bukan nol) pada tahun " + str(tahun_view))
    s = pd.Series([i+1 for i in range(len(tuple_besar_negara1))])
    st.dataframe((tabel.set_index(s)).head(len(tuple_besar_negara1)))

#MENU 3
def fitur_C():
    st.title(":bar_chart: FITUR C ")
    st.sidebar.markdown("**Deskripsi Fitur C : **")
    st.sidebar.markdown("Menampilkan dan memberikan info negara dengan urutan produksi **minyak mentah** terbesar ke terkecil (bukan nol) berdasarkan produksi kumulatifnya (seluruh tahun)")
    
    df_grup_kumulatif = df.groupby("kode_negara")["produksi"].sum()
    tuple_besar_negaraC = []
    for i in df_grup_kumulatif.index:
        if not i in list_bukan_negara:
            if df_grup_kumulatif[i] != 0:
                x = i
                y = df_grup_kumulatif[i]
                new = y,x
                tuple_besar_negaraC.append(new)
    tuple_besar_negaraC.sort(reverse=True)
    
    besar_view = st.number_input("Pilih Besar Negara : ",min_value=1,max_value=len(tuple_besar_negaraC),value=4)
    list_nama_negaraC = [x for y,x in tuple_besar_negaraC[:besar_view]]
    list_produksi_kumulatif = [y for y,x in tuple_besar_negaraC[:besar_view]]
    
    
    #VISUALISASI
    plt.subplots(figsize=(15,8),dpi=200)
    #plt.axes().set_facecolor("whitesmoke")
    cmap_name = "tab20c"
    cmap = cm.get_cmap(cmap_name)
    colors = cmap.colors[:len(list_nama_negaraC)]
    plt.bar(list_nama_negaraC,list_produksi_kumulatif,color=colors)
    plt.xticks(list_nama_negaraC,fontsize=13,rotation = 45)
    plt.yticks(fontsize=15)
    plt.ylabel("Produksi Kumulatif",fontsize = 18)
    plt.title("Negara Produksi Kumulatif Minyak Mentah Terbesar",fontsize = 22,fontweight="bold")
    plt.grid(axis="y",linestyle="--")
    st.pyplot(plt)
  
    #LEGEND
    tabel = pd.DataFrame({"Negara" : pd.Series([Inputan1[x] for y,x in tuple_besar_negaraC]),
                          "Kode" : pd.Series([x for y,x in tuple_besar_negaraC]),
                          "Produksi" : pd.Series([y for y,x in tuple_besar_negaraC])
                         })
  
    st.markdown("*_Axis X pada grafik diatas berupa kode negara.\nPilih salah satu kode tersebut untuk melihat info lebih detail._")
    
    #LIAT NEGARA,URUTAN,PRODUKSI BERDASARKAN KODE GRAFIK
    left_col, right_col = st.columns(2)
    list_nama_negaraC.sort()
    legend1 = left_col.selectbox("Pilih Kode Negara :",list_nama_negaraC)
    right_col.markdown("Negara : " + Inputan1[legend1])
    indeks1 = int(tabel[tabel["Negara"]==Inputan1[legend1]].index.values)
    right_col.markdown("Urutan : " + str(indeks1+1))
    right_col.markdown("Produksi : " + str(round(tabel["Produksi"][indeks1],3)))
    
    #st.markdown("-----")
    
    st.subheader("Info Seluruh Urutan Negara")
    st.markdown("Terdapat " + str(len(tabel["Negara"])) + " besar negara yang produksi kumulatifnya tidak nol.")
    st.markdown("Pilih negara untuk melihat urutannya  **ATAU**  pilih urutan untuk melihat info negaranya.")
    
    left_col, right_col = st.columns(2)
    
    #LIAT NEGARA,KODE,PRODUKSI BERDASARKAN URUTAN
    legend = right_col.number_input("Pilih Posisi/Urutan :",min_value=1,max_value=len(tuple_besar_negaraC),value=1)
    nama_negara = [Inputan1[x] for y,x in tuple_besar_negaraC][legend-1] 
    right_col.markdown("Negara : " + nama_negara)
    right_col.markdown("Kode : " + Inputan[nama_negara])
    indeks = [Inputan1[x] for y,x in tuple_besar_negaraC].index(nama_negara)
    right_col.markdown("Produksi : " + str(round([y for y,x in tuple_besar_negaraC][indeks],3)))

    
    #LIAT KODE,URUTAN,PRODUKSI BERDASARKAN NEGARA
    negara = [Inputan1[x] for y,x in tuple_besar_negaraC]
    negara.sort()
    legend2 = left_col.selectbox("Pilih Negara :",negara)
    left_col.markdown("Kode : " + Inputan[legend2])
    indeks1 = int(tabel[tabel["Negara"]==legend2].index.values)
    left_col.markdown("Urutan : " + str(indeks1+1))
    left_col.markdown("Produksi : " + str(round(tabel["Produksi"][indeks1],3)))
    
    
    st.markdown("---")
    
    #TABEL LENGKAPNYA - PALING BAWAH
    st.markdown("*Berikut urutan negara dengan produksi kumulatif terbesar hingga terkecil (bukan nol) :")
    s = pd.Series([i+1 for i in range(len(tuple_besar_negaraC))])
    st.dataframe((tabel.set_index(s)).head(len(tuple_besar_negaraC)))

def fitur_D():
    st.title("📚 FITUR D ")
    st.sidebar.markdown("**Deskripsi Fitur D : **")
    st.sidebar.markdown("Memberikan info negara yang memiliki produksi **minyak mentah** terbesar, terkecil, atau nol pada suatu tahun atau secara kumulatif (seluruh tahun)")
    awal_tahun = df["tahun"][0]
    akhir_tahun = df["tahun"][len(df.index)-1]
    list_tahun_fix = [i+awal_tahun for i in range(akhir_tahun-awal_tahun+1)]
    tahun = st.selectbox("Pilih Tahun",["seluruh tahun"]+list_tahun_fix)
    
    tuple_max = []
    tuple_min = []
    tuple_nol = []
    
    for i in df.index:
        if not df["kode_negara"][i] in list_bukan_negara:
            #SELURUH TAHUN
            if tahun == "seluruh tahun":
                return fitur_D_seluruh_tahun()
            #TAHUN X / TERTENTU
            else:
                if df["tahun"][i]==tahun:
                    x = df["kode_negara"][i]
                    y = df["produksi"][i]
                    new = y,x
                    tuple_max.append(new)
                    if df["produksi"][i]!=0.0:
                        x = df["kode_negara"][i]
                        y = df["produksi"][i]
                        new = y,x
                        tuple_min.append(new)
                    if df["produksi"][i]==0.0:
                        x = df["kode_negara"][i]
                        tuple_nol.append(x)
                        
    
    #PENGOLAHAN DATA UNTUK TAHUN X / TERTENTU
    tuple_max.sort(reverse=True)
    tuple_min.sort()
    negara_max = [x for y,x in tuple_max[:1]]
    negara_min = [x for y,x in tuple_min[:1]]
    prod_max = [y for y,x in tuple_max[:1]]
    prod_min = [y for y,x in tuple_min[:1]]

    #SUMMARY
    left_col, right_col = st.columns(2)
    
    Nama = []
    Code = []
    Kode_negara = []
    Region = []
    Sub_region = []
    
    for kode in [negara_max[0],negara_min[0]]:
        for i in range(len(data_json)):
            if data_json[i]["alpha-3"]==kode:
                a = data_json[i]["name"]
                b = data_json[i]["alpha-3"]
                c = data_json[i]["country-code"]
                d = data_json[i]["region"]
                e = data_json[i]["sub-region"]
                Nama.append(a)
                Code.append(b)
                Kode_negara.append(c)
                Region.append(d)
                Sub_region.append(e)
    
    
    #SUMMARY - TABEL NEGARA TERBESAR  
    left_col.subheader("Produksi Maks : " + str(round(prod_max[0],3)))
    
    key_max = ["Name","Alpha-3","Country Code","Region","Sub-Region"]
    val_max = [Nama[0],Code[0],Kode_negara[0],Region[0],Sub_region[0]]
    
    df_max = pd.DataFrame({"Key":key_max,"Value":val_max})
    s = df_max.set_index("Key")
    left_col.dataframe(s)
    
    
    #SUMMARY - TABEL NEGARA TERKECIL
    right_col.subheader("Produksi Min : " + str(round(prod_min[0],3)))
    
    key_min = ["Name","Alpha-3","Country Code","Region","Sub-Region"]
    val_min = [Nama[1],Code[1],Kode_negara[1],Region[1],Sub_region[1]]
    
    df_min = pd.DataFrame({"Key":key_min,"Value":val_min})
    ss = df_min.set_index("Key")
    right_col.dataframe(ss)
    
    st.markdown("---")
    
    st.subheader("Tidak Berproduksi / Nol")
    st.markdown("Terdapat " + str(len(tuple_nol)) + " negara yang nilai produksinya nol atau tidak berproduksi pada tahun " + str(tahun) + ". Berikut list negaranya :")
    
    
    #SUMMARY - TABEL NEGARA YANG NOL PRODUKSI
    name = []
    alpha_3 = []
    country_code = []
    region = []
    sub_region = []
    nama = []
    for kode in tuple_nol:
        for i in range(len(data_json)):
            if data_json[i]["alpha-3"]==kode:
                x = data_json[i]["name"]
                nama.append(x)
    nama.sort()
    for n in nama:
        for i in range(len(data_json)):
            if data_json[i]["name"]== n :
                a = data_json[i]["name"]
                b = data_json[i]["alpha-3"]
                c = data_json[i]["country-code"]
                d = data_json[i]["region"]
                e = data_json[i]["sub-region"]
                name.append(a)
                alpha_3.append(b)
                country_code.append(c)
                region.append(d)
                sub_region.append(e)
    data = {"Name" : pd.Series(name),
            "Alpha-3" : pd.Series(alpha_3),
            "Country Code" : pd.Series(country_code),
            "Region" : pd.Series(region),
            "Sub-Region" : pd.Series(sub_region)
            }

    df_data = pd.DataFrame(data)
    sss = pd.Series([i+1 for i in range(len(name))])
    st.dataframe((df_data.set_index(sss)).head(len(name)))

    
def fitur_D_seluruh_tahun():
    #SELURUH TAHUN
    biggest = None
    smallest = None
    for i in df.index:
        if not df["kode_negara"][i] in list_bukan_negara:
            if biggest is None:
                biggest = df["produksi"][i]
            if biggest < df["produksi"][i] :
                biggest = df["produksi"][i]
            if df["produksi"][i]!=0.0:
                if smallest is None:
                    smallest = df["produksi"][i]
                if smallest > df["produksi"][i] :
                    smallest = df["produksi"][i]
    index_min = df[df["produksi"]==smallest].index.values[0]   
    index_max = df[df["produksi"]==biggest].index.values[0]
   
    #KUMULATIF PRODUKSI 
    negara_nol = []
    negara_prod = []
    negara_kode = []
    df_new = df.groupby("kode_negara")["produksi"].sum()
    for i in df_new.index:
        if not i in list_bukan_negara:
            if df_new[i]==0.0:
                negara_nol.append(i)
            else:
                negara_kode.append(i)
                negara_prod.append(df_new[i])

    st.markdown("Berikut info mengenai **produksi tahunan maksimum dan minimum yang pernah ada** berdasarkan data : ")
    
    #SUMMARY
    left_col, right_col = st.columns(2)
    
    Nama = []
    Code = []
    Kode_negara = []
    Region = []
    Sub_region = []


    for kode in [df["kode_negara"][index_max],df["kode_negara"][index_min],negara_kode[negara_prod.index(max(negara_prod))],negara_kode[negara_prod.index(min(negara_prod))]]:
        for i in range(len(data_json)):
            if data_json[i]["alpha-3"]==kode:
                a = data_json[i]["name"]
                b = data_json[i]["alpha-3"]
                c = data_json[i]["country-code"]
                d = data_json[i]["region"]
                e = data_json[i]["sub-region"]
                Nama.append(a)
                Code.append(b)
                Kode_negara.append(c)
                Region.append(d)
                Sub_region.append(e)
    
    
    #SUMMARY - TABEL NEGARA TERBESAR - TAHUNAN
    left_col.subheader("Produksi Maks. :")

    key_max = ["Produksi","Tahun","Name","Alpha-3","Country Code","Region","Sub-Region"]
    val_max = [str(round(df["produksi"][index_max],3)),str(df["tahun"][index_max]),Nama[0],Code[0],Kode_negara[0],Region[0],Sub_region[0]]
    
    df_max = pd.DataFrame({"Key":key_max,"Value":val_max})
    s = df_max.set_index("Key")
    left_col.dataframe(s)
    
    #SUMMARY - TABEL NEGARA TERKECIL - TAHUNAN
    right_col.subheader("Produksi Min. :")
    
    key_min = ["Produksi","Tahun","Name","Alpha-3","Country Code","Region","Sub-Region"]
    val_min = [str(round(df["produksi"][index_min],3)),str(df["tahun"][index_min]),Nama[1],Code[1],Kode_negara[1],Region[1],Sub_region[1]]
    
    df_min = pd.DataFrame({"Key":key_min,"Value":val_min})
    ss = df_min.set_index("Key")
    right_col.dataframe(ss)
    
    st.markdown("---")
    
    st.markdown("Berikut info mengenai **produksi kumulatif tiap negara yang maksimum, minimum, dan nol berdasarkan data : **")
    
    left_col, right_col = st.columns(2)


    #SUMMARY - TABEL NEGARA TERBESAR - KUMULATIF TAHUN
    left_col.subheader("Kumulatif Maks.")

    key_max_kum = ["Produksi","Name","Alpha-3","Country Code","Region","Sub-Region"]
    val_max_kum = [str(round(max(negara_prod),3)),Nama[2],Code[2],Kode_negara[2],Region[2],Sub_region[2]]
    
    df_max_kum = pd.DataFrame({"Key":key_max_kum,"Value":val_max_kum})
    index_max = df_max_kum.set_index("Key")
    left_col.dataframe(index_max)
    
    #SUMMARY - TABEL NEGARA TERKECIL - KUMULATIF TAHUN
    right_col.subheader("Kumulatif Min.")
    
    key_min_kum = ["Produksi","Name","Alpha-3","Country Code","Region","Sub-Region"]
    val_min_kum = [str(round(min(negara_prod),3)),Nama[3],Code[3],Kode_negara[3],Region[3],Sub_region[3]]
    
    df_min_kum = pd.DataFrame({"Key":key_min_kum,"Value":val_min_kum})
    index_min = df_min_kum.set_index("Key")
    right_col.dataframe(index_min)
    
    st.markdown("_*Tabel urutan produksi kumulatif terbesar ke terkecil (bukan nol) secara lengkap beserta negaranya terdapat di fitur C._")

    st.subheader("Tidak Berproduksi / Nol")
    st.markdown("Terdapat " + str(len(negara_nol)) + " negara yang produksi kumulatifnya nol atau tidak pernah berproduksi. Berikut list negaranya :")
    
    
    #SUMMARY - TABEL NEGARA YANG NOL PRODUKSI
    name = []
    alpha_3 = []
    country_code = []
    region = []
    sub_region = []
    nama = []
    for kode in negara_nol:
        for i in range(len(data_json)):
            if data_json[i]["alpha-3"]==kode:
                x = data_json[i]["name"]
                nama.append(x)
    nama.sort()
    for n in nama:
        for i in range(len(data_json)):
            if data_json[i]["name"]== n :
                a = data_json[i]["name"]
                b = data_json[i]["alpha-3"]
                c = data_json[i]["country-code"]
                d = data_json[i]["region"]
                e = data_json[i]["sub-region"]
                name.append(a)
                alpha_3.append(b)
                country_code.append(c)
                region.append(d)
                sub_region.append(e)
    data = {"Name" : pd.Series(name),
            "Alpha-3" : pd.Series(alpha_3),
            "Country Code" : pd.Series(country_code),
            "Region" : pd.Series(region),
            "Sub-Region" : pd.Series(sub_region)
            }

    df_data = pd.DataFrame(data)
    sss = pd.Series([i+1 for i in range(len(name))])
    st.dataframe((df_data.set_index(sss)).head(len(name)))


menu_main()
