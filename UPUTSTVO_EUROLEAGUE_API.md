# EuroLeague API - Uputstvo za korišćenje

## Šta je EuroLeague API?

EuroLeague API je Python biblioteka koja omogućava pristup statistikama i podacima iz EuroLeague i EuroCup liga. API omogućava dobijanje:

- Rezultata mečeva i izveštaja
- Statistika igrača i timova  
- Tabela (standings)
- Detaljnih podataka o šutevima
- Play-by-play podataka
- Boxscore podataka

## Instalacija

```bash
pip install euroleague-api
```

## Osnovni koncepti

### Takmičenja
- **"E"** - EuroLeague
- **"U"** - EuroCup

### Sezone
Sezone se označavaju početnom godinom. Na primer:
- `2024` = sezona 2024-25
- `2023` = sezona 2023-24

### Tipovi statistika
- **"traditional"** - osnovne statistike (poeni, skokovi, asistencije)
- **"advanced"** - napredne statistike (efikasnost, rating)

### Način agregacije
- **"PerGame"** - prosek po meču
- **"Accumulated"** - ukupno za sezonu

## Dostupni moduli

### 1. GameStats - Statistike mečeva

```python
from euroleague_api.game_stats import GameStats

# Kreiranje instance za EuroLeague
game_stats = GameStats(competition="E")

# Dobijanje svih mečeva iz sezone
mecevi = game_stats.get_game_reports_single_season(2024)

# Dobijanje podataka o jednom meču
mec = game_stats.get_game_report(season=2024, game_code=1)
```

### 2. Standings - Tabele

```python
from euroleague_api.standings import Standings

standings = Standings(competition="E")

# Trenutna tabela
tabela = standings.get_standings(season=2024)

# Tabela nakon određene runde
tabela_runda = standings.get_standings(season=2024, round_number=10)
```

### 3. TeamStats - Statistike timova

```python
from euroleague_api.team_stats import TeamStats

team_stats = TeamStats(competition="E")

# Osnovne statistike timova za sezonu
stats = team_stats.get_team_stats_single_season(
    endpoint="traditional",
    season=2024,
    statistic_mode="PerGame"
)

# Napredne statistike
advanced_stats = team_stats.get_team_stats_single_season(
    endpoint="advanced",
    season=2024,
    statistic_mode="Accumulated"
)
```

### 4. PlayerStats - Statistike igrača

```python
from euroleague_api.player_stats import PlayerStats

player_stats = PlayerStats(competition="E")

# Statistike igrača za sezonu
igraci = player_stats.get_player_stats_single_season(
    endpoint="traditional",
    season=2024,
    statistic_mode="PerGame"
)
```

### 5. BoxScoreData - Boxscore podaci

```python
from euroleague_api.boxscore_data import BoxScoreData

boxscore = BoxScoreData(competition="E")

# Boxscore timova za sezonu
team_boxscore = boxscore.get_game_boxscore_quarter_data_single_season(2024)

# Boxscore igrača za sezonu
player_boxscore = boxscore.get_player_boxscore_stats_single_season(2024)
```

### 6. ShotData - Podaci o šutevima

```python
from euroleague_api.shot_data import ShotData

shot_data = ShotData(competition="E")

# Podaci o šutevima za celu sezonu
sutevi = shot_data.get_game_shot_data_single_season(2024)

# Podaci o šutevima za jedan meč
mec_sutevi = shot_data.get_game_shot_data(season=2024, game_code=1)
```

### 7. PlayByPlay - Detaljni tok meča

```python
from euroleague_api.play_by_play_data import PlayByPlay

pbp = PlayByPlay(competition="E")

# Play-by-play za celu sezonu
tok_meceva = pbp.get_game_play_by_play_data_single_season(2024)
```

## Prosti primer - Poslednjih 5 mečeva

```python
from euroleague_api.game_stats import GameStats
import pandas as pd

def poslednjih_5_meceva():
    # Kreiraj instancu za EuroLeague
    game_stats = GameStats(competition="E")
    
    # Dobij sve mečeve iz trenutne sezone (2024)
    mecevi_df = game_stats.get_game_reports_single_season(2024)
    
    # Uzmi poslednjih 5 mečeva
    poslednjih_5 = mecevi_df.tail(5)
    
    # Prikaži rezultate
    for _, mec in poslednjih_5.iterrows():
        print(f"Runda {mec['Round']} - Game Code: {mec['Gamecode']}")
        print(f"Datum: {mec.get('date', 'N/A')}")
        print(f"Timovi: {mec.get('teamA', 'N/A')} vs {mec.get('teamB', 'N/A')}")
        print(f"Rezultat: {mec.get('scoreA', 'N/A')} - {mec.get('scoreB', 'N/A')}")
        print("-" * 40)

# Pokreni funkciju
poslednjih_5_meceva()
```

## Prosti primer - Top 5 timova po poenima

```python
from euroleague_api.team_stats import TeamStats

def top_5_timova_poeni():
    team_stats = TeamStats(competition="E")
    
    # Dobij statistike timova
    stats_df = team_stats.get_team_stats_single_season(
        endpoint="traditional",
        season=2024,
        statistic_mode="PerGame"
    )
    
    # Sortiraj po poenima (kolona se može zvati 'points' ili slično)
    if 'points' in stats_df.columns:
        top_5 = stats_df.nlargest(5, 'points')
        
        print("TOP 5 TIMOVA PO POENIMA PO MEČU:")
        for i, (_, tim) in enumerate(top_5.iterrows(), 1):
            print(f"{i}. {tim['team.name']}: {tim['points']:.1f} poena")
    else:
        print("Dostupne kolone:", list(stats_df.columns))

# Pokreni funkciju
top_5_timova_poeni()
```

## Primer - Tabela lige

```python
from euroleague_api.standings import Standings

def prikazi_tabelu():
    standings = Standings(competition="E")
    
    # Dobij trenutnu tabelu
    tabela_df = standings.get_standings(season=2024)
    
    print("EUROLEAGUE TABELA 2024-25:")
    print(f"{'Poz':<3} {'Tim':<25} {'W':<3} {'L':<3} {'Pts':<4}")
    print("-" * 40)
    
    for _, tim in tabela_df.head(10).iterrows():
        print(f"{tim.get('position', 'N/A'):<3} "
              f"{tim.get('name', 'N/A')[:24]:<25} "
              f"{tim.get('wins', 'N/A'):<3} "
              f"{tim.get('losses', 'N/A'):<3} "
              f"{tim.get('points', 'N/A'):<4}")

# Pokreni funkciju
prikazi_tabelu()
```

## Pokretanje primera

Da pokrenete pripremljeni primer:

```bash
python primer_euroleague_api.py
```

Ovaj fajl sadrži funkcije za:
1. Prikaz poslednjih 5 mečeva
2. Prikaz tabele lige
3. Prikaz statistika timova

## Napomene

- API zahteva internetsku konekciju
- Neke funkcije mogu biti spore jer dobijaju velike količine podataka
- Pazite na rate limiting od strane API-ja
- Za najnovije podatke koristite aktuelnu sezonu (2024 za sezonu 2024-25)

## Korisni linkovi

- [Originalna dokumentacija](https://github.com/giasemidis/euroleague_api)
- [Swagger API dokumentacija](https://api-live.euroleague.net/swagger/index.html)
- [EuroLeague zvanični sajt](https://www.euroleague.net/)

## Česte greške

1. **Neispravna sezona** - Proverite da li je sezona dostupna
2. **Neispravni game_code** - Game code možete naći na EuroLeague sajtu
3. **Mrežne greške** - Proverite internet konekciju
4. **Nedostaju podaci** - Neki stariji mečevi možda nemaju sve podatke 