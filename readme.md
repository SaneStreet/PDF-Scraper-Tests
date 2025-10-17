# 🧪 PDF Scraper – Unit & Integration Testing

Dette projekt indeholder en samling **unit tests** og **integration tests** til et eksisterende Python-projekt kaldet ```pdf_scraper```.  
Formålet er at demonstrere, hvordan man kan teste netværkskald, filoperationer og globale variabler effektivt med ```unittest``` og ```unittest.mock```.

---

## 🧰 Teknologier
- Python 3.x  
- unittest (standardbibliotek)  
- unittest.mock  
- pandas (mockes i integrationstests)  
- requests (mockes i integrationstests)

---

## 📂 Projektstruktur
```
📁 project/tests/
│
├── test_file.py                    # Unit tests til File() klassen
├── test_urlaccess.py               # Unit tests til UrlAccess() klassen
├── test_intercae.py                # Unit tests til Interface() klassen
├── test_integration_urlaccess.py   # Integration test til UrlAccess.access() funktionen
└── requirements.txt                # Imports som er vigtige for at teste
```

---

## 🧠 Testindhold

### ✅ Unit tests
Testene fokuserer på enkelte funktioner og metoder, fx:
- `File.get_from_file()`
- `UrlAccess.save_file()`
- Fejlhåndtering og returværdier

Disse tests bruger `MagicMock` og `patch` til at simulere API-kald og filadgang uden rigtige downloads.

---

### 🔗 Integration tests
Integrationstesten (`test_integration_urlaccess.py`) kører hele `UrlAccess.access()`-flowet:
- Mock’er `requests.head` og `requests.get`
- Simulerer globale variabler (`filenames`, `initial_urls`, osv.)
- Tester, at downloads, filskrivning og Excel-output sker korrekt

---

### ▶️ Sådan kører du testene
Kør alle tests med:
```
bash
python -m unittest discover -s .\tests\ -p "test_*.py" -v
```
Eller kun én specifik test:
```
python -m unittest .\tests\testens_navn.py -v
```
---

### ⚙️ Krav
For at installere ```requirements.txt``` køres:
```
pip install -r requirements.txt
```
Fra mappen ```tests```

### 🧩 Formål
Dette repo er udelukkende til demonstration og læring om:
* Mocking i Python
* TEstdækning på systemniveau
* Arbejdsstruktur mellem Unit og Integration tests
