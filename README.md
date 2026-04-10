# 🌍 Language Translator Pro

## ✨ **Overview**

**🌍 Language Translator Pro** is a beautiful web application built with **Streamlit** that provides instant translations to **100+ languages** with stunning UI/UX. Features include:

- **🔄 Real-time translation**
- **🎵 Text-to-Speech** in 50+ languages with natural voices
- **🌐 100+ supported languages** (including rare dialects)
- **📱 Responsive design** - Works on desktop, tablet, mobile
- **💾 Downloadable audio & text** files
- **🎨 Modern gradient UI** with dark/light theme support
- **⚡ No setup required** - Runs instantly!

## 🚀 **Quick Demo**

```
Enter text → Select language → Get instant translation + audio!
```

## 📋 **Features**

| Feature | Status |
|---------|--------|
| Multi-language translation | ✅ 100+ languages |
| Text-to-Speech | ✅ 50+ languages |
| Audio download | ✅ MP3 format |
| Text copy/download | ✅ TXT format |
| Auto language detection | 🔄 Planned |
| Batch translation | 🔄 Planned |
| Image OCR translation | 🔄 Planned |

## 🛠 **Tech Stack**

```
Frontend: Streamlit (Python)
Translation: mtranslate (Google Translate API)
Speech: gTTS (Google Text-to-Speech)
Data: Pandas
UI: Custom CSS + Animations
Deployment: Streamlit Cloud / Railway / Render
```

## 📦 **Installation**

### Prerequisites
- Python 3.8+
- pip

### 1. Clone & Setup
```bash
git clone <your-repo-url>
cd LanguageTranslator
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```
**Note:** Fix the filename from `requiremwnt.txt` to `requirements.txt`

### 3. Run the App
```bash
streamlit run app.py
```

**✅ App will open at: `http://localhost:8501`**

## 📁 **Project Structure**

```
LanguageTranslator/
├── app.py              # Main Streamlit app
├── language.csv        # Language codes & names (100+)
├── requirements.txt    # Python dependencies
└── README.md           # You're reading it! 📖
```

## 🎯 **Supported Languages**

- **100+ languages** including Afrikaans, Arabic, Chinese, Hindi, Spanish, French, etc.
- Full list embedded in `language.csv`
- **50+ languages** support speech synthesis

**Popular languages:**
```
English ↔ Hindi ↔ Spanish ↔ French ↔ German ↔ Arabic ↔ Chinese
```

## 🔊 **Text-to-Speech Features**

- Natural Google TTS voices
- Download as MP3
- Adjustable speed
- Works offline after generation

## 🎨 **UI Highlights**

- **Gradient animations** & smooth transitions
- **Dark/Light theme** auto-detection
- **Progress bars** during translation
- **Real-time character count**
- **Success animations** (balloons! 🎈)

## ⚡ **Usage**

1. **Enter text** in the input box
2. **Select target language** from dropdown (100+ options)
3. **Click translate** → Instant results!
4. **Listen** to audio (if available)
5. **Download** text/audio files

## 📊 **Performance**

| Operation | Time |
|-----------|------|
| Translation | <2s |
| Audio Generation | <3s |
| UI Load | Instant |

## 🤖 **How Translation Works**

```
Input Text → mtranslate API → Target Language
↓
Optional: gTTS → Audio File → Browser Player
```

**Powered by Google's translation & speech APIs** (free tier)

## 🚀 **Deployment**

### Streamlit Cloud (Recommended)
1. Push to GitHub
2. Connect to [streamlit.io/cloud](https://streamlit.io/cloud)
3. Deploy! ✅

```

## 🔧 **Troubleshooting**

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError` | `pip install -r requirements.txt` |
| Port already in use | `streamlit run app.py --server.port 8502` |
| No audio | Check internet connection |
| CORS errors | Use deployed version |

## 📈 **Future Enhancements**

- [ ] **Batch translation** (multiple texts)
- [ ] **Document translation** (PDF/DOCX)
- [ ] **Image OCR** + translation
- [ ] **Translation history**
- [ ] **Custom voice selection**
- [ ] **API endpoints**

## 🤝 **Contributing**


## ⭐ **Star & Fork**

If you found this useful, please ⭐ **star** the repo and **fork** it!

---

**Built with ❤️ using Streamlit**  
**Made for developers, by developers** 🚀

**Questions?** Open an issue or ping @chinmay! 👨‍💻

