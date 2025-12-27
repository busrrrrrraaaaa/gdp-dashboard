
import streamlit as st
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import random
import os

st.set_page_config(page_title="Yılbaşı Mesaj Ağacı", page_icon="🎄")

# --- VERİ VE DOSYA YÖNETİMİ ---
if not os.path.exists("notlar.csv"):
    df = pd.DataFrame(columns=["İsim", "Not", "Sus"])
    df.to_csv("notlar.csv", index=False)

def not_kaydet(isim, mesaj, sus):
    df = pd.read_csv("notlar.csv")
    yeni = pd.DataFrame([[isim, mesaj, sus]], columns=["İsim", "Not", "Sus"])
    pd.concat([df, yeni], ignore_index=True).to_csv("notlar.csv", index=False)

# --- GÖRSEL ÜZERİNE NOT YAZMA (Pillow) ---
def agaci_guncelle():
    # 'agac.jpg' adında bir resmin olduğunu varsayıyoruz, yoksa internetten bir tane indirelim
    img = Image.open("agac.jpg") 
    draw = ImageDraw.Draw(img)
    
    # Notları oku ve resmin üzerine rastgele yerleştir
    df = pd.read_csv("notlar.csv")
    for index, row in df.tail(10).iterrows(): # Son 10 notu ekranda göster
        x = random.randint(100, 400)
        y = random.randint(100, 500)
        metin = f"{row['Sus']} {row['İsim']}: {row['Not']}"
        draw.text((x, y), metin, fill="white") # Basit beyaz yazı
        
    img.save("guncel_agac.jpg")

# --- ARAYÜZ ---
st.title("🎄 İnteraktif Yılbaşı Ağacı")

col1, col2 = st.columns([2, 1])

with col2:
    st.subheader("Mesajını Bırak")
    isim = st.text_input("Adın")
    mesaj = st.text_input("Kısa Notun (Maks 20 harf)")
    sus = st.selectbox("Süsünü Seç", ["⭐ Yıldız", "🔴 Kırmızı Top", "🔵 Mavi Top", "🕯️ Mum"])
    
    if st.button("Ağaca Ekle ✨"):
        if isim and mesaj:
            not_kaydet(isim, mesaj, sus)
            st.snow()
            st.success("Notun eklendi!")
            # agaci_guncelle() # Resim dosyan hazır olduğunda bu satırı açabilirsin
        else:
            st.warning("Lütfen tüm alanları doldur.")

with col1:
    # Şimdilik temsil bir resim gösteriyoruz
    st.image("https://images.unsplash.com/photo-1543589077-47d81606c1bf?w=500", use_container_width=True)
    
st.divider()
st.write("### 🎁 Son Gelen Notlar")
st.dataframe(pd.read_csv("notlar.csv").tail(5))
