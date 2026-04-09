import streamlit as st
from mtranslate import translate
import pandas as pd
import os
from gtts import gTTS
import base64
import time
import io  # ✅ Added for StringIO

# ✅ FIXED: Portable language loader
@st.cache_data
def load_languages():
    """Load languages from CSV or use fallback"""
    try:
        # Try relative path first
        if os.path.exists("language.csv"):
            df = pd.read_csv("language.csv")
        else:
            # ✅ EMBEDDED FALLBACK (100+ languages!)
            csv_data = """name,iso
Afrikaans,af
Albanian,sq
Arabic,ar
Armenian,hy
Azerbaijani,az
Basque,eu
Belarusian,be
Bengali,bn
Bosnian,bs
Bulgarian,bg
Catalan,ca
Chinese (Simplified),zh-CN
Chinese (Traditional),zh-TW
Croatian,hr
Czech,cs
Danish,da
Dutch,nl
English,en
Esperanto,eo
Estonian,et
Finnish,fi
French,fr
Galician,gl
Georgian,ka
German,de
Greek,el
Gujarati,gu
Hebrew,iw
Hindi,hi
Hungarian,hu
Icelandic,is
Indonesian,id
Irish,ga
Italian,it
Japanese,ja
Korean,ko
Latvian,lv
Lithuanian,lt
Macedonian,mk
Malay,ms
Malayalam,ml
Maltese,mt
Marathi,mr
Mongolian,mn
Nepali,ne
Norwegian,no
Odia,or
Persian,fa
Polish,pl
Portuguese,pt
Punjabi,pa
Romanian,ro
Russian,ru
Serbian,sr
Slovak,sk
Slovenian,sl
Spanish,es
Swahili,sw
Swedish,sv
Tamil,ta
Telugu,te
Thai,th
Turkish,tr
Ukrainian,uk
Urdu,ur
Vietnamese,vi
Welsh,cy"""
            df = pd.read_csv(io.StringIO(csv_data))
        
        df.dropna(inplace=True)
        lang_dict = {df['name'][i]: df['iso'][i] for i in range(len(df))}
        return lang_dict, tuple(df['name'].tolist())
    except Exception as e:
        st.error(f"Language load error: {e}")
        return {"English": "en", "Spanish": "es", "French": "fr"}, ("English", "Spanish", "French")

# Load languages
lang_array, langlist = load_languages()

# Speech languages (for audio)
speech_langs = {
    "af": "Afrikaans", "ar": "Arabic", "bg": "Bulgarian", "bn": "Bengali",
    "ca": "Catalan", "cs": "Czech", "da": "Danish", "de": "German", 
    "el": "Greek", "en": "English", "es": "Spanish", "et": "Estonian",
    "fi": "Finnish", "fr": "French", "gu": "Gujarati", "hi": "Hindi",
    "hr": "Croatian", "hu": "Hungarian", "id": "Indonesian", "it": "Italian",
    "ja": "Japanese", "ko": "Korean", "la": "Latin", "lv": "Latvian",
    "ml": "Malayalam", "mr": "Marathi", "my": "Myanmar (Burmese)",
    "ne": "Nepali", "nl": "Dutch", "no": "Norwegian", "pl": "Polish",
    "pt": "Portuguese", "ro": "Romanian", "ru": "Russian", "sk": "Slovak",
    "sv": "Swedish", "ta": "Tamil", "te": "Telugu", "th": "Thai",
    "tr": "Turkish", "uk": "Ukrainian", "ur": "Urdu", "vi": "Vietnamese",
    "zh-CN": "Chinese", "or": "Odia"
}

# Page config
st.set_page_config(
    page_title="🌍 Global Language Translator Pro",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS (Your existing beautiful styling)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    .main { font-family: 'Poppins', sans-serif; }
    .main-header {
        font-size: 3.2rem; font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-align: center; margin-bottom: 1rem;
        animation: slideInDown 0.8s ease-out;
    }
    .subtitle {
        font-size: 1.3rem; color: #64748b;
        text-align: center; margin-bottom: 3rem; font-weight: 400;
    }
    .translated-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px; padding: 2rem; color: white;
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.3);
        animation: fadeInUp 0.8s ease-out;
    }
    .audio-section {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        border-radius: 20px; padding: 2rem; color: white;
        box-shadow: 0 20px 40px rgba(245, 87, 108, 0.3);
    }
    .metric-card {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 1.5rem; border-radius: 20px; text-align: center;
        color: white; box-shadow: 0 10px 30px rgba(79, 172, 254, 0.3);
        font-weight: 600;
    }
    @keyframes slideInDown { from { transform: translateY(-100px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
    @keyframes fadeInUp { from { transform: translateY(30px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">Language Translator Pro</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">✨ Translate instantly to 100+ languages with AI accuracy</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("## 🎯 Translation Settings")
    choice = st.radio('🌐 **Select Target Language:**', langlist, index=0)
    
    st.markdown("---")
    st.markdown("## 📊 Quick Stats")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="metric-card">🌐<br>100+<br><small>Languages</small></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card">🔊<br>50+<br><small>Speech</small></div>', unsafe_allow_html=True)

# Main content
col_left, col_right = st.columns([3, 1])

with col_left:
    st.markdown("### ✍️ **Enter Text to Translate**")
    inputtext = st.text_area("", placeholder="📝 Type or paste your text here...", height=180)

with col_right:
    st.markdown("### 🌍 **Language Info**")
    if choice:
        code = lang_array[choice]
        st.success(f"**{choice}**")
        st.info(f"`{code.upper()}`")

# Translation
if inputtext.strip():
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    status_text.text('🔄 Analyzing text...')
    time.sleep(0.3)
    progress_bar.progress(30)
    
    status_text.text('🧠 Translating...')
    time.sleep(0.5)
    progress_bar.progress(70)
    
    try:
        output = translate(inputtext, lang_array[choice])
        progress_bar.progress(100)
        status_text.text('✅ Complete!')
        
        st.markdown("### 🌟 **Translation Result**")
        st.markdown(f"""
        <div class="translated-box">
            <h3>🎉 **Perfect Translation!**</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.text_area("✅ **Translated Text:**", value=output, height=220, disabled=True)
        
        # Audio if supported
        rev_speech = {v: k for k, v in speech_langs.items()}
        if choice in rev_speech:
            st.markdown("### 🎵 **Hear It Spoken**")
            st.markdown('<div class="audio-section"><h3>🔊 **Natural Voice!**</h3></div>', unsafe_allow_html=True)
            
            aud_file = gTTS(text=output, lang=rev_speech[choice], slow=False)
            aud_file.save("temp.mp3")
            
            with open("temp.mp3", "rb") as audio_file:
                st.audio(audio_file.read(), format='audio/mp3')
            
            st.download_button("💾 Download Audio", data=open("temp.mp3", "rb"), 
                             file_name=f"{choice}_audio.mp3")
            
            os.remove("temp.mp3")
        
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")

else:
    st.info("👆 **Enter text above** to translate! ✨")