def ensure_alpha3(code):
    a2_to_a3 = {
            "en": "eng",
            "fi": "fin",
            "ru": "rus",
            "se": "sme",
            "uk": "ukr",
            }

    if len(code) < 3:
        return a2_to_a3[code]
    else:
        return code
