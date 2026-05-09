# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## ZORUNLU KURAL: Bu Dosyaları Her Zaman Güncelle

**Her kod değişikliğinin ardından, commit yapmadan önce `CLAUDE.md` ve `AGENTS.md` dosyalarını güncellemelisin.**

Güncelleme gerektiren durumlar:
- Yeni dosya veya modül eklenmesi
- Yeni API endpoint'i eklenmesi veya kaldırılması
- Yeni frontend sayfası eklenmesi
- Mevcut bir modülün sorumluluğunun değişmesi
- Yeni bağımlılık veya ortam değişkeni eklenmesi

Güncelleme yapmazsan mimari bilgisi eskir ve gelecekteki Claude oturumları yanlış varsayımlarla çalışır.

---

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

---

## Mimari

Flask backend + vanilla JS frontend. İki ayrı sayfa sunar:

| Sayfa | URL | Açıklama |
|---|---|---|
| LLM Arayüzü | `/` | Tek seferlik, hafızasız LLM çağrısı |
| Asistan | `/asistan` | Conversation history tutan sohbet arayüzü |

### Dosya Sorumlulukları

- **`app.py`** — Flask uygulaması. Routing, model doğrulaması, asistan oturumu yönetimi.
- **`llm.py`** — OpenAI istemcisi kurulumu ve `stream_llm()` fonksiyonu. Tek seferlik, history'siz.
- **`asistan.py`** — `Asistan` sınıfı. Conversation history tutan, `sohbet()` ve `stream_sohbet()` metodları olan wrapper.
- **`frontend/index.html`** — LLM arayüzü. Tek prompt → tek yanıt.
- **`frontend/asistan.html`** — Sohbet arayüzü. Baloncuklu, çok turlu, session tabanlı.

### LLM Arayüzü Veri Akışı

1. `frontend/index.html` → `POST /api/chat` (model, system_instructions, user_prompt)
2. `app.py` → `stream_llm()` çağrısı
3. `llm.py` → OpenAI Streaming API → chunk'lar `text/plain` olarak istemciye aktarılır
4. Frontend `ReadableStream` ile chunk'ları okur, `#response` div'ine ekler

### Asistan Veri Akışı

1. `frontend/asistan.html` → `POST /api/asistan/yeni` (model, system_instructions) → `session_id` döner
2. `frontend/asistan.html` → `POST /api/asistan/sohbet` (session_id, user_prompt)
3. `app.py` → `_asistanlar[session_id].stream_sohbet()` çağrısı
4. `asistan.py` → OpenAI Streaming API → chunk yield eder, bitince history'ye ekler
5. Frontend chunk'ları asistan balonuna akıtır

### API Endpoint'leri

| Method | Path | Açıklama |
|---|---|---|
| POST | `/api/chat` | Tek seferlik LLM çağrısı (streaming) |
| POST | `/api/asistan/yeni` | Yeni asistan oturumu oluştur |
| POST | `/api/asistan/sohbet` | Asistana mesaj gönder (streaming) |

### Kritik Noktalar

- Model doğrulaması `app.py`'deki `ALLOWED_MODELS` set'i üzerinden yapılır; yeni model eklendiğinde hem burası hem `index.html` ve `asistan.html` içindeki `<select>` güncellenmeli.
- `llm.py` modül yüklendiğinde `client = OpenAI()` oluşturulur; `OPENAI_API_KEY` `.env`'de yoksa uygulama başlamaz.
- `_asistanlar` dict'i sunucu hafızasındadır; sunucu yeniden başlatılınca tüm oturumlar sıfırlanır.
- Backend yanıtlar `mimetype="text/plain"` olarak stream edilir; JSON değil düz metin.
