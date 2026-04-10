import streamlit as st
# from mtranslate import translate
from googletrans import Translator


import pandas as pd
import io
import os
from gtts import gTTS
import base64
import time
import requests
from io import BytesIO

translator = Translator()


# ✅ FIXED: Removed theme="auto" parameter
st.set_page_config(
    page_title="🌍 Global Language Translator Pro",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful styling (unchanged)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    .main { font-family: 'Poppins', sans-serif; }
    
    .main-header {
        font-size: 3.2rem; font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        background-clip: text; text-align: center; margin-bottom: 1rem;
        animation: slideInDown 0.8s ease-out;
    }
    
    .subtitle {
        font-size: 1.3rem; color: #64748b; text-align: center;
        margin-bottom: 3rem; font-weight: 400;
    }
    
    .stTextArea > label {
        font-size: 1.2rem; font-weight: 600; color: #1e40af; margin-bottom: 0.5rem;
    }
    
    .translated-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px; padding: 2rem; color: white;
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.3);
        margin-bottom: 1rem; animation: fadeInUp 0.8s ease-out;
    }
    
    .audio-section {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        border-radius: 20px; padding: 2rem; color: white;
        box-shadow: 0 20px 40px rgba(245, 87, 108, 0.3);
        animation: fadeInUp 1s ease-out;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 1.5rem; border-radius: 20px; text-align: center;
        color: white; box-shadow: 0 10px 30px rgba(79, 172, 254, 0.3);
        font-weight: 600;
    }
    
    .stRadio > div > label {
        font-size: 1.2rem; font-weight: 500; color: #1e40af;
        padding: 0.5rem; border-radius: 10px;
    }
    
    .stDownloadButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white; border: none; padding: 0.8rem 2rem;
        border-radius: 25px; font-weight: 600; font-size: 1rem;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
    }
    
    @keyframes slideInDown {
        from { transform: translateY(-100px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    
    @keyframes fadeInUp {
        from { transform: translateY(30px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    
    .footer {
        text-align: center; padding: 2rem; color: #64748b;
        font-size: 0.95rem; border-top: 1px solid #e2e8f0; margin-top: 3rem;
    }
</style>
""", unsafe_allow_html=True)

# Auto system theme support (simplified - works perfectly)
st.markdown("""
<style>
/* Dark mode support via Streamlit's built-in theme */
[data-testid="stAppViewContainer"] {
    background-color: var(--background-color);
    color: var(--text-color);
}

/* Custom dark mode overrides */
@media (prefers-color-scheme: dark) {
    .translated-box {
        background: linear-gradient(135deg, #5b21b6 0%, #7c3aed 100%) !important;
    }
    .audio-section {
        background: linear-gradient(135deg, #be185d 0%, #dc2626 100%) !important;
    }
    .subtitle, .footer {
        color: #94a3b8 !important;
    }
}
</style>
""", unsafe_allow_html=True)

# EMBEDDED LANGUAGE DATA (unchanged)
LANGUAGE_DATA = """
name,iso
Afrikaans,af
Albanian,sq
Amharic,am
Arabic,ar
Armenian,hy
Azerbaijani,az
Basque,eu
Belarusian,be
Bengali,bn
Bosnian,bs
Bulgarian,bg
Catalan,ca
Cebuano,ceb
Chinese (Simplified),zh-CN
Chinese (Traditional),zh-TW
Corsican,co
Croatian,hr
Czech,cs
Danish,da
Dutch,nl
English,en
Esperanto,eo
Estonian,et
Finnish,fi
French,fr
Frisian,fy
Galician,gl
Georgian,ka
German,de
Greek,el
Gujarati,gu
Haitian Creole,ht
Hausa,ha
Hawaiian,haw
Hebrew,iw
Hindi,hi
Hmong,hmn
Hungarian,hu
Icelandic,is
Igbo,ig
Indonesian,id
Irish,ga
Italian,it
Japanese,ja
Javanese,jw
Kannada,kn
Kazakh,kk
Khmer,km
Korean,ko
Kurdish (Kurmanji),ku
Kyrgyz,ky
Lao,lo
Latin,la
Latvian,lv
Lithuanian,lt
Luxembourgish,lb
Macedonian,mk
Malagasy,mg
Malay,ms
Malayalam,ml
Maltese,mt
Maori,mi
Marathi,mr
Mongolian,mn
Myanmar (Burmese),my
Nepali,np
Norwegian,no
Odia (Oriya),or
Pashto,ps
Persian,fa
Polish,pl
Portuguese,pt
Punjabi,pa
Romanian,ro
Russian,ru
Samoan,sm
Sanskrit,sans
Scots Gaelic,gd
Serbian,sr
Sesotho,st
Shona,sn
Sindhi,sd
Sinhala,si
Slovak,sk
Slovenian,sl
Somali,so
Spanish,es
Sundanese,su
Swahili,sw
Swedish,sv
Tagalog (Filipino),tl
Tajik,tg
Tamil,ta
Telugu,te
Thai,th
Turkish,tr
Turkmen,tk
Ukrainian,uk
Urdu,ur
Uyghur,ug
Uzbek,uz
Vietnamese,vi
Welsh,cy
Xhosa,xh
Yiddish,yi
Yoruba,yo
Zulu,zu
"""

# Load languages from embedded data
@st.cache_data
def load_languages():
    df = pd.read_csv(io.StringIO(LANGUAGE_DATA))
    df.dropna(inplace=True)
    lang = df['name'].to_list()
    langcode = df['iso'].to_list()
    return {lang[i]: langcode[i] for i in range(len(langcode))}, tuple(lang)

lang_array, langlist = load_languages()

# Speech languages (gTTS supported)
speech_langs = {
    "Afrikaans": "af", "Arabic": "ar", "Bulgarian": "bg", "Bengali": "bn",
    "Bosnian": "bs", "Catalan": "ca", "Czech": "cs", "Welsh": "cy",
    "Danish": "da", "German": "de", "Greek": "el", "English": "en",
    "Esperanto": "eo", "Spanish": "es", "Estonian": "et", "Finnish": "fi",
    "French": "fr", "Gujarati": "gu", "Hindi": "hi", "Croatian": "hr",
    "Hungarian": "hu", "Armenian": "hy", "Indonesian": "id", "Icelandic": "is",
    "Italian": "it", "Japanese": "ja", "Javanese": "jw", "Khmer": "km",
    "Kannada": "kn", "Korean": "ko", "Latin": "la", "Latvian": "lv",
    "Macedonian": "mk", "Malayalam": "ml", "Marathi": "mr", "Myanmar (Burmese)": "my",
    "Nepali": "ne", "Dutch": "nl", "Norwegian": "no", "Polish": "pl",
    "Portuguese": "pt", "Romanian": "ro", "Russian": "ru", "Sinhala": "si",
    "Slovak": "sk", "Albanian": "sq", "Serbian": "sr", "Sundanese": "su",
    "Swedish": "sv", "Swahili": "sw", "Tamil": "ta", "Telugu": "te",
    "Thai": "th", "Tagalog (Filipino)": "tl", "Turkish": "tr", "Ukrainian": "uk",
    "Urdu": "ur", "Vietnamese": "vi", "Chinese (Simplified)": "zh-CN", "Odia (Oriya)": "or"
}

# Header
st.markdown('<h1 class="main-header">🌍 Language Translator Pro</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">✨ Translate instantly to 100+ languages with AI accuracy</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 🎯 Translation Settings")
    choice = st.radio(
        '🌐 **Select Target Language:**', 
        langlist, 
        index=langlist.index('English') if 'English' in langlist else 0
    )
    
    st.markdown("---")
    st.markdown("## 📊 Quick Stats")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="metric-card">🌐<br>100+<br><small>Languages</small></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card">🔊<br>50+<br><small>Speech</small></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card">🤖<br>AI<br><small>Powered</small></div>', unsafe_allow_html=True)

# Main content
col_left, col_right = st.columns([3, 1])

with col_left:
    st.markdown("### ✍️ **Enter Text to Translate**")
    inputtext = st.text_area(
        label="Enter text to translate",
        height=200,
        placeholder="Type or paste text here...",
        key="input_text"
    )

with col_right:
    st.markdown("### 🌍 **Language Info**")
    if choice:
        code = lang_array[choice]
        st.success(f"**{choice}**")
        st.info(f"`{code.upper()}`")
        speech_support = "✅ **Available**" if choice in speech_langs else "❌ **Not Available**"
        st.metric("Speech Support", speech_support)

# Translation Processing
if inputtext.strip():
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    status_text.text('🔄 Analyzing text...')
    time.sleep(0.3)
    progress_bar.progress(30)
    
    status_text.text('🧠 Translating with AI...')
    time.sleep(0.5)
    progress_bar.progress(70)
    
    try:
        output = translator.translate(inputtext, dest=lang_array[choice]).text
        progress_bar.progress(100)
        status_text.text('✅ Translation complete!')
        time.sleep(0.5)
        st.balloons()
        
        # Results
        st.markdown("### 🌟 **Translation Result**")
        st.markdown(f"""
        <div class="translated-box">
            <h3>🎉 **Perfect Translation!**</h3>
            <p><strong>From:</strong> {len(inputtext)} chars → <strong>To:</strong> {len(output)} chars</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.text_area(
            "✅ **Translated Text:**", 
            value=output, 
            height=220, 
            disabled=True,
            label_visibility="collapsed"
        )
        
        # Audio generation
        if choice in speech_langs:
            st.markdown("### 🎵 **Hear It Spoken**")
            st.markdown(f"""
            <div class="audio-section">
                <h3>🔊 **Natural Voice!**</h3>
            </div>
            """, unsafe_allow_html=True)
            
            status_text.text('🎤 Generating audio...')
            
            # Generate audio in memory
            tts = gTTS(text=output, lang=speech_langs[choice], slow=False)
            audio_buffer = BytesIO()
            tts.write_to_fp(audio_buffer)
            audio_bytes = audio_buffer.getvalue()
            
            # Audio player
            st.audio(audio_bytes, format='audio/mp3')
            
            # Download buttons
            col1, col2 = st.columns(2)
            with col1:
                st.download_button(
                    label="💾 **Download Audio**",
                    data=audio_bytes,
                    file_name=f"{choice.replace(' ', '_')}_pronunciation.mp3",
                    mime="audio/mpeg"
                )
            with col2:
                st.download_button(
                    label="📋 **Copy Text**",
                    data=output,
                    file_name=f"{choice}_translation.txt",
                    mime="text/plain"
                )
        else:
            st.warning("🎵 **Audio pronunciation not available** for this language")
            st.success("✅ **Text translation completed successfully!**")
            
    except Exception as e:
        st.error(f"❌ **Translation Error:** {str(e)}")
        st.info("💡 **Tips:** Try shorter text or a different language")

else:
    st.info("👆 **Enter some text above** to see the magic happen! ✨")

# Footer
st.markdown("""
<div class="footer">
    <p>🚀 Built with Streamlit By Chinmay ❤️  100+ Languages  </p>
    <p>**Quick** translations | **No Setup Required**</p>
</div>
""", unsafe_allow_html=True)