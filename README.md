## 🌍 Quiz o jeziorach świata – Django App

Opis:
Aplikacja webowa w Django, która umożliwia użytkownikom rozwiązywanie quizu o jeziorach świata. Dane zostałe pobrane ze strony internetowej (scraping) 'International Lake Environment Comittee Foundation' i przechowywane są w bazie SQLite3. Quiz generuje 5 pytań z 4 możliwymi odpowiedziami, a dodatkowo można przeglądać wszystkie jeziora i ich lokalizację z wyszukiwarką.

### 🛠 Technologie

Backend: Python 3.11+, Django  
Baza danych: SQLite3  
Kontrola wersji: Git  


### ⚡ Funkcjonalności

Generowanie quizu z 5 pytań i 4 odpowiedziami.  
Możliwość przeglądania wszystkich jezior i ich lokalizacji.  
Wyszukiwarka konkretnych jezior.  
Prosta i czytelna strona webowa do interakcji z quizem.  


### 🚀 Uruchomienie lokalne

Sklonuj repozytorium
```
git clone https://github.com/marc32132/worldLakeQuizApp.git
cd worldLakeQuizApp
```
Utwórz i aktywuj wirtualne środowisko

```
python -m venv venv 
source venv/bin/activate  # Linux / macOS 
venv\Scripts\activate     # Windows
```
Zainstaluj zależności
```
pip install -r requirements.txt
```
Uruchom serwer Django
```
python manage.py runserver
```
Otwórz przeglądarkę: `http://127.0.0.1:8000/`




 
GitHub: https://github.com/marc32132
