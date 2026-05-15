# Fit Menü Planlayıcı — vbl1

Bu proje, Flask backend ve vanilla JavaScript frontend kullanarak geliştirilmiş bir AI agent uygulamasıdır. Kullanıcılar LLM arayüzü, sohbet asistanı, kodlama agenti ve fit menü planlayıcısı sayfalarını kullanabilir.

## Eklenen Araç: `makro_hesapla`

`backend/tools/makro.py` dosyasında tanımlanan `makro_hesapla` aracı, agent'a besin değerlerini hesaplama yeteneği kazandırır. Yemek adı ve gram miktarı parametre olarak alır; 30'dan fazla besini kapsayan yerleşik bir veritabanından kalori, protein, karbonhidrat ve yağ değerlerini hesaplayarak döndürür. Bu sayede Fit Menü Planlayıcı sayfasındaki agent, kullanıcının kişisel profiline (yaş, kilo, boy, cinsiyet) göre makro-doğruluklu beslenme planları ve tarif önerileri sunabilir.

## Kurulum

`.env` dosyasında `OPENAI_API_KEY` tanımlı olmalıdır.

```bash
pip install -r requirements.txt
flask --app app run --debug --port 8080
```

Uygulama `http://localhost:8080` adresinde çalışır.

## Sayfalar

| Sayfa | URL |
|---|---|
| LLM Arayüzü | `/` |
| Asistan | `/asistan` |
| Kodlama Agenti | `/agent` |
| Fit Menü Planlayıcı | `/menu` |

## Araçlar

| Araç | Dosya | Ne Yapar |
|---|---|---|
| `makro_hesapla` | `backend/tools/makro.py` | Yemek adı + gram → kalori/protein/karbo/yağ hesaplar |
| `terminal` | `backend/tools/__init__.py` | Shell komutu çalıştırır |
| `dosya_oku` | `backend/tools/__init__.py` | Dosya okur |
| `dosya_yaz` | `backend/tools/__init__.py` | Dosya yazar |
