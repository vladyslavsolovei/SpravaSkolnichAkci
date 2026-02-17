# Správa školních akcí

Jednoduchá desktopová aplikace v Pythonu pro evidenci školních akcí, účastníků a jejich registrací.

## Funkce

- Vytváření a mazání školních akcí
- Přidávání a mazání účastníků
- Filtrování účastníků podle třídy
- Registrace účastníků na akce
- Automatické mazání souvisejících registrací
- Databáze SQLite (vytvoří se automaticky při prvním spuštění)

---

## Požadavky

- Python 3.x
- Není potřeba instalovat žádné externí knihovny (využívá pouze standardní knihovny – `tkinter`, `sqlite3`)

---

## Instalace

### Možnost 1 – Stažení jako ZIP

1. Klikněte na tlačítko **Code**
2. Zvolte **Download ZIP**
3. Rozbalte soubor do vybrané složky

### Možnost 2 – Git clone

```bash
git clone https://github.com/vladyslavsolovei/SpravaSkolnichAkci.git
cd SpravaSkolnichAkci
```
### Spuštění aplikace

Ve složce projektu spusťte:
```
python main_gui.py
```

Po prvním spuštění se automaticky vytvoří soubor:
```
database.db
```

Tento soubor obsahuje databázi aplikace.

### Používání aplikace

Aplikace obsahuje tři záložky:

1️⃣ Akce

Slouží k vytváření a mazání školních akcí.

Vytvoření akce:

Vyplňte název, datum a místo

Klikněte na „Vytvořit akci“

Smazání akce:

Vyberte akci v tabulce

Klikněte na „Smazat vybranou“

2️⃣ Účastníci

Slouží k evidenci studentů.

Přidání účastníka:

Vyplňte jméno a třídu

Klikněte na „Přidat účastníka“

Filtrování podle třídy:

Zadejte název třídy do pole filtru

Klikněte na „Filtrovat“

Smazání účastníka:

Vyberte účastníka

Klikněte na „Smazat vybraného“

3️⃣ Registrace

Slouží k přihlašování účastníků na akce.

Vytvoření registrace:

Zadejte ID akce

Zadejte ID účastníka

Klikněte na „Zaregistrovat“

Smazání registrace:

Vyberte registraci

Klikněte na „Smazat registraci“

### Struktura databáze

Aplikace používá tři tabulky:

akce

id

název

datum

místo

ucastnici

id

jméno

třída

registrace

id

akce_id

ucastnik_id

Při smazání akce nebo účastníka se automaticky smažou související registrace.

### Reset databáze

Pokud chcete vymazat všechna data:

Zavřete aplikaci

Smažte soubor database.db

Spusťte aplikaci znovu

Databáze se vytvoří znovu prázdná.


