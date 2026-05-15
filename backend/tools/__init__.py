import os
import subprocess

from backend.tools.makro import TOOL_DEFINITION as _makro_tanim, makro_hesapla

AGENT_WORKSPACE = "/tmp/agent_workspace"


def _terminal(args: dict) -> str:
    command = args["command"]
    os.makedirs(AGENT_WORKSPACE, exist_ok=True)
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30,
            cwd=AGENT_WORKSPACE,
        )
        output = (result.stdout + result.stderr).strip()
        return output or "(komut çıktı üretmedi)"
    except subprocess.TimeoutExpired:
        return "Hata: Komut 30 saniyede tamamlanamadı."
    except Exception as e:
        return f"Hata: {e}"


def _dosya_oku(args: dict) -> str:
    try:
        with open(args["yol"], encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Hata: {e}"


def _dosya_yaz(args: dict) -> str:
    yol, icerik = args["yol"], args["icerik"]
    try:
        dizin = os.path.dirname(yol)
        if dizin:
            os.makedirs(dizin, exist_ok=True)
        with open(yol, "w", encoding="utf-8") as f:
            f.write(icerik)
        return f"Başarıyla yazıldı: {yol}"
    except Exception as e:
        return f"Hata: {e}"


TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "terminal",
            "description": (
                "Terminalde bir shell komutu çalıştırır ve çıktısını döner. "
                f"Çalışma dizini: {AGENT_WORKSPACE}"
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": "Çalıştırılacak shell komutu"},
                },
                "required": ["command"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "dosya_oku",
            "description": "Bir dosyanın içeriğini okur.",
            "parameters": {
                "type": "object",
                "properties": {
                    "yol": {"type": "string", "description": "Dosya yolu"},
                },
                "required": ["yol"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "dosya_yaz",
            "description": "Bir dosyaya içerik yazar; dosya yoksa oluşturur, varsa üzerine yazar.",
            "parameters": {
                "type": "object",
                "properties": {
                    "yol": {"type": "string", "description": "Dosya yolu"},
                    "icerik": {"type": "string", "description": "Dosyaya yazılacak içerik"},
                },
                "required": ["yol", "icerik"],
            },
        },
    },
    _makro_tanim,
]

TOOL_FUNCTIONS = {
    "terminal": _terminal,
    "dosya_oku": _dosya_oku,
    "dosya_yaz": _dosya_yaz,
    "makro_hesapla": makro_hesapla,
}
