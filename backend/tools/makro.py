BESIN_VERITABANI = {
    "tavuk göğsü": {"kalori": 165, "protein": 31, "karbo": 0, "yag": 3.6},
    "tavuk": {"kalori": 165, "protein": 31, "karbo": 0, "yag": 3.6},
    "yumurta": {"kalori": 155, "protein": 13, "karbo": 1.1, "yag": 11},
    "pirinç": {"kalori": 130, "protein": 2.7, "karbo": 28, "yag": 0.3},
    "makarna": {"kalori": 158, "protein": 5.8, "karbo": 31, "yag": 0.9},
    "ekmek": {"kalori": 265, "protein": 9, "karbo": 49, "yag": 3.2},
    "tam buğday ekmeği": {"kalori": 247, "protein": 13, "karbo": 41, "yag": 4.2},
    "yulaf": {"kalori": 389, "protein": 17, "karbo": 66, "yag": 7},
    "somon": {"kalori": 208, "protein": 20, "karbo": 0, "yag": 13},
    "ton balığı": {"kalori": 116, "protein": 26, "karbo": 0, "yag": 1},
    "dana kıyma": {"kalori": 250, "protein": 26, "karbo": 0, "yag": 15},
    "yoğurt": {"kalori": 59, "protein": 10, "karbo": 3.6, "yag": 0.4},
    "süt": {"kalori": 42, "protein": 3.4, "karbo": 5, "yag": 1},
    "peynir": {"kalori": 402, "protein": 25, "karbo": 1.3, "yag": 33},
    "lor peyniri": {"kalori": 98, "protein": 11, "karbo": 3.4, "yag": 4.3},
    "mercimek": {"kalori": 116, "protein": 9, "karbo": 20, "yag": 0.4},
    "nohut": {"kalori": 164, "protein": 9, "karbo": 27, "yag": 2.6},
    "fasulye": {"kalori": 127, "protein": 8.7, "karbo": 23, "yag": 0.5},
    "patates": {"kalori": 77, "protein": 2, "karbo": 17, "yag": 0.1},
    "tatlı patates": {"kalori": 86, "protein": 1.6, "karbo": 20, "yag": 0.1},
    "brokoli": {"kalori": 34, "protein": 2.8, "karbo": 7, "yag": 0.4},
    "ıspanak": {"kalori": 23, "protein": 2.9, "karbo": 3.6, "yag": 0.4},
    "domates": {"kalori": 18, "protein": 0.9, "karbo": 3.9, "yag": 0.2},
    "muz": {"kalori": 89, "protein": 1.1, "karbo": 23, "yag": 0.3},
    "elma": {"kalori": 52, "protein": 0.3, "karbo": 14, "yag": 0.2},
    "badem": {"kalori": 579, "protein": 21, "karbo": 22, "yag": 50},
    "ceviz": {"kalori": 654, "protein": 15, "karbo": 14, "yag": 65},
    "zeytinyağı": {"kalori": 884, "protein": 0, "karbo": 0, "yag": 100},
    "avokado": {"kalori": 160, "protein": 2, "karbo": 9, "yag": 15},
    "kinoa": {"kalori": 120, "protein": 4.4, "karbo": 22, "yag": 1.9},
}


TOOL_DEFINITION = {
    "type": "function",
    "function": {
        "name": "makro_hesapla",
        "description": (
            "Verilen yemeğin belirtilen miktarı için kalori, protein, karbonhidrat ve yağ "
            "değerlerini hesaplar. Besin değerleri 100g başına veritabanında tutulur ve "
            "istenen miktara orantılanır."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "yemek": {
                    "type": "string",
                    "description": "Yemeğin adı (örn: 'tavuk göğsü', 'yulaf', 'yumurta')",
                },
                "miktar_gram": {
                    "type": "number",
                    "description": "Miktar (gram cinsinden)",
                },
            },
            "required": ["yemek", "miktar_gram"],
        },
    },
}


def makro_hesapla(args: dict) -> str:
    yemek = args["yemek"].lower().strip()
    miktar = float(args["miktar_gram"])

    anahtar = next((k for k in BESIN_VERITABANI if k in yemek or yemek in k), None)
    if not anahtar:
        return (
            f"'{args['yemek']}' veritabanında bulunamadı. "
            f"Mevcut besinler: {', '.join(BESIN_VERITABANI.keys())}"
        )

    oran = miktar / 100
    b = BESIN_VERITABANI[anahtar]
    return (
        f"{miktar:.0f}g {anahtar} için besin değerleri:\n"
        f"  Kalori  : {b['kalori'] * oran:.1f} kcal\n"
        f"  Protein : {b['protein'] * oran:.1f} g\n"
        f"  Karbo   : {b['karbo'] * oran:.1f} g\n"
        f"  Yağ     : {b['yag'] * oran:.1f} g"
    )
