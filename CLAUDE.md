# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Geliştirme Ortamı

```bash
# Sanal ortamı aktifleştir
source .venv/bin/activate

# Bağımlılıkları yükle
pip install -r requirements.txt

# Uygulamayı çalıştır (http://localhost:5000)
flask --app app run --debug
```

`.env` dosyasında `OPENAI_API_KEY` tanımlı olmalıdır.

## Mimari

Tek sayfalık bir LLM arayüzü: Flask backend, vanilla JS frontend.

**Veri akışı:**
1. `frontend/index.html` → `POST /api/chat` (model, system_instructions, user_prompt)
2. `app.py` → `stream_llm()` çağrısı (model doğrulaması burada yapılır; `ALLOWED_MODELS` sabit listesi)
3. `llm.py` → OpenAI Streaming API → chunk'lar `text/plain` olarak istemciye aktarılır
4. Frontend `ReadableStream` ile chunk'ları okur, `#response` div'ine ekler

**Kritik noktalar:**
- Model doğrulaması `app.py:6`'daki `ALLOWED_MODELS` set'i üzerinden yapılır; yeni model eklendiğinde hem burası hem `index.html` içindeki `<select>` güncellenmeli
- `llm.py` modül yüklendiğinde `client = OpenAI()` oluşturulur; `OPENAI_API_KEY` `.env`'de yoksa uygulama başlamaz
- Backend yanıt `mimetype="text/plain"` olarak stream edilir; JSON değil düz metin
