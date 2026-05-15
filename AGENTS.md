# AGENTS.md — Repository Guidelines

## ZORUNLU KURAL: Bu Dosyaları Her Zaman Güncelle

**Her kod değişikliğinin ardından, commit yapmadan önce `CLAUDE.md` ve `AGENTS.md` dosyalarını güncellemelisin.**

Aşağıdaki durumlarda ilgili bölümleri güncelle:

| Değişiklik | Güncelle |
|---|---|
| Yeni modül / dosya eklendi | "Proje Yapısı" bölümü her iki dosyada |
| Yeni API endpoint'i | `CLAUDE.md` endpoint tablosu + bu dosyadaki routing bölümü |
| Yeni frontend sayfası | `CLAUDE.md` mimari tablosu + bu dosyadaki yapı bölümü |
| Yeni `pip` bağımlılığı | Bu dosyadaki bağımlılıklar bölümü |
| Yeni ortam değişkeni | Her iki dosyadaki ilgili notlar |

Bu dosyaları güncellemeden commit atmak yasaktır.

---

## Proje Yapısı

```
app.py                      # Flask uygulaması; routing, doğrulama, oturum yönetimi
llm.py                      # OpenAI istemcisi; hafızasız stream_llm() fonksiyonu
asistan.py                  # Asistan sınıfı; conversation history + stream_sohbet()
agent.py                    # Agent sınıfı; tool-calling agentic loop + calistir() generator
backend/
  __init__.py               # Paket tanımı
  tools/
    __init__.py             # TOOL_DEFINITIONS ve TOOL_FUNCTIONS; araç merkezi kayıt
    makro.py                # makro_hesapla aracı: yemek + gram → kalori/makro
frontend/
  index.html                # LLM arayüzü: tek seferlik prompt/yanıt sayfası
  asistan.html              # Asistan arayüzü: çok turlu, baloncuklu sohbet sayfası
  agent.html                # Agent arayüzü: tool call'ları ve adımları görsel gösterim
  menu.html                 # Fit Menü Planlayıcı: profil girişi + menü tercihi + chat
requirements.txt            # Python bağımlılıkları
.env                        # Yerel sırlar (commit edilmez); OPENAI_API_KEY buraya
CLAUDE.md                   # Claude Code'a mimari rehberlik
AGENTS.md                   # Bu dosya; geliştirici ve ajan kuralları
```

Backend routing ve doğrulama `app.py`'de kalır. Provider'a özgü LLM çağrıları `llm.py`, `asistan.py` veya `agent.py`'de kalır. Statik dosyalar `frontend/` altına eklenir.

---

## API Endpoint'leri

| Method | Path | Body | Açıklama |
|---|---|---|---|
| POST | `/api/chat` | `{model, system_instructions, user_prompt}` | Hafızasız, tek seferlik LLM çağrısı (streaming, text/plain) |
| POST | `/api/asistan/yeni` | `{model, system_instructions}` | Yeni asistan oturumu oluşturur, `session_id` döner |
| POST | `/api/asistan/sohbet` | `{session_id, user_prompt}` | Asistana mesaj gönderir (streaming, text/plain) |
| POST | `/api/agent/yeni` | `{model, system_instructions}` | Yeni agent oturumu oluşturur, `session_id` döner |
| POST | `/api/agent/calistir` | `{session_id, user_prompt}` | Agent'ı çalıştırır (NDJSON stream; event tipleri: `step_start`, `thinking`, `tool_call`, `tool_result`, `text`, `done`, `error`) |

`/menu` sayfası mevcut `/api/agent/*` endpoint'lerini kullanır; kendine özel endpoint yoktur.

---

## Geliştirme Komutları

```sh
pip install -r requirements.txt
# macOS'ta port 5000 AirPlay tarafından kullanıldığından 8080 kullan
flask --app app run --debug --port 8080   # http://127.0.0.1:8080
```

---

## Kod Stili

- Python 3, 4 boşluk girinti, yeniden kullanılabilir yardımcılar için type hint.
- `stream_llm(...) -> Iterator[str]` ve `stream_sohbet(...) -> Iterator[str]` imzası örnek alınmalı.
- Hata mesajları API sınırını geçiyorsa kullanıcıya yönelik, provider hatası gizlenmeli.
- Frontend: sade HTML/CSS/JS, `camelCase` JS değişkenleri, amaca uygun `id` isimleri.

---

## Test Kılavuzu

Otomatik test suite mevcut değil. Test eklenecekse:

- `tests/` dizini oluştur, `pytest` kullan.
- Dosyaları `test_*.py` olarak adlandır.
- Öncelikli test alanları: Flask route doğrulama, `ALLOWED_MODELS` kontrolü, streaming hata yönetimi, asistan history doğruluğu.

```sh
pytest
```

Frontend değişikliklerinde tarayıcıda şunları manuel doğrula: boş prompt engelleme, model seçimi, streaming render, asistan history sürekliliği.

---

## Commit ve PR Kuralları

- Commit mesajları kısa ve imperative: `Add streaming assistant`, `Validate chat payload`.
- PR'lara: kısa özet, test notları, gerekli `.env` değişiklikleri, UI değişimi varsa ekran görüntüsü ekle.

---

## Güvenlik

- API anahtarları yalnızca `.env`'de; `python-dotenv` ile yükle. Commit etme.
- Log veya API yanıtında sır basmak yasak.
- `ALLOWED_MODELS` değiştiğinde `app.py` ve tüm frontend `<select>` elementleri birlikte güncellenmeli.
- `_asistanlar` dict'i sunucu hafızasında; production için kalıcı depolama gerekir.
