#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Primer korišćenja EuroLeague API-ja - ISPRAVLJENA VERZIJA
========================================================

Ovaj primer pokazuje kako da koristite EuroLeague API za:
1. Dobijanje poslednjih 5 mečeva sa statistikama
2. Prikaz top scorera iz poslednjih utakmica
3. Dobijanje standings (tabele)
4. Prikaz osnovnih statistika timova
"""

from euroleague_api.game_stats import GameStats
from euroleague_api.standings import Standings
from euroleague_api.team_stats import TeamStats
from euroleague_api.boxscore_data import BoxScoreData
from euroleague_api.player_stats import PlayerStats
import pandas as pd

def prikazi_poslednje_meceve(season=2024, broj_meceva=5):
    """
    Funkcija koja prikazuje poslednje mečeve iz sezone sa detaljnim statistikama
    """
    print(f"\n{'='*60}")
    print(f"POSLEDNJIH {broj_meceva} MEČEVA SA STATISTIKAMA - SEZONA {season}")
    print(f"{'='*60}")
    
    # Kreiramo instance za različite tipove podataka
    game_stats = GameStats(competition="E")
    boxscore = BoxScoreData(competition="E")
    
    try:
        # Dobijamo sve game reportove za sezonu
        mecevi_df = game_stats.get_game_reports_single_season(season)
        
        # Sortiramo po datumu i uzimamo poslednje mečeve
        if not mecevi_df.empty:
            poslednji_mecevi = mecevi_df.tail(broj_meceva)
            
            for _, mec in poslednji_mecevi.iterrows():
                game_code = mec.get('Gamecode', 'N/A')
                print(f"\n{'='*50}")
                print(f"RUNDA {mec.get('Round', 'N/A')} - GAME CODE: {game_code}")
                print(f"Datum: {mec.get('date', 'N/A')}")
                
                # Osnovne informacije o meču
                if 'teamA' in mec and 'teamB' in mec:
                    team_a = mec['teamA']
                    team_b = mec['teamB']
                    score_a = mec.get('scoreA', 'N/A')
                    score_b = mec.get('scoreB', 'N/A')
                    
                    print(f"\n🏀 {team_a} {score_a} - {score_b} {team_b}")
                    
                    # Pokušavamo da dobijemo detaljne statistike meča
                    try:
                        # Koristimo boxscore podatke umesto game_stats
                        team_boxscore = boxscore.get_game_boxscore_quarter_data(season, game_code)
                        
                        if not team_boxscore.empty:
                            print(f"\n📊 OSNOVNE STATISTIKE:")
                            print(f"  Rezultat: {score_a} - {score_b}")
                            print(f"  Dostupno: {len(team_boxscore)} redova podataka")
                            
                        else:
                            print(f"  📊 Osnovna statistika:")
                            print(f"    Rezultat: {score_a} - {score_b}")
                            
                    except Exception as e_detail:
                        print(f"  ⚠️ Rezultat: {score_a} - {score_b}")
                        print(f"  (Detaljni podaci nisu dostupni)")
                
                print("-" * 50)
        else:
            print("Nije pronađen nijedan meč za zadatu sezonu.")
            
    except Exception as e:
        print(f"Greška pri dobijanju mečeva: {e}")

def prikazi_tabelu(season=2024):
    """
    Funkcija koja prikazuje trenutnu tabelu (bez round_number parametra)
    """
    print(f"\n{'='*60}")
    print(f"TABELA - SEZONA {season}")
    print(f"{'='*60}")
    
    standings = Standings(competition="E")
    
    try:
        # Dobijamo tabelu bez round_number
        tabela_df = standings.get_standings(season=season)
        
        if not tabela_df.empty:
            # Prikazujemo top 10 timova
            print(f"{'Pozicija':<4} {'Tim':<25} {'W':<3} {'L':<3} {'Pts':<4}")
            print("-" * 45)
            
            for _, tim in tabela_df.head(10).iterrows():
                pozicija = tim.get('position', 'N/A')
                ime_tima = tim.get('name', 'N/A')[:24]  # Skraćujemo ime tima
                pobede = tim.get('wins', 'N/A')
                porazi = tim.get('losses', 'N/A')
                poeni = tim.get('points', 'N/A')
                
                print(f"{pozicija:<4} {ime_tima:<25} {pobede:<3} {porazi:<3} {poeni:<4}")
        else:
            print("Tabela nije pronađena.")
            
    except Exception as e:
        print(f"Greška pri dobijanju tabele: {e}")
        print("Pokušavam sa alternativnim pristupom...")
        
        # Alternativni pristup - možemo pokušati da dobijemo standings drugačije
        try:
            # Pokušamo sa team stats da vidimo record
            team_stats = TeamStats(competition="E")
            stats_df = team_stats.get_team_stats_single_season(
                endpoint="traditional", 
                season=season, 
                statistic_mode="Accumulated"
            )
            
            if not stats_df.empty and 'team.name' in stats_df.columns:
                print("\n📊 ALTERNATIVNI PRIKAZ - TIMOVI I STATISTIKE:")
                print(f"{'Tim':<25} {'GP':<3} {'Pts/G':<6}")
                print("-" * 40)
                
                for i, (_, tim) in enumerate(stats_df.head(10).iterrows(), 1):
                    ime = tim.get('team.name', 'N/A')[:24]
                    gp = tim.get('gamesPlayed', 'N/A')
                    avg_pts = tim.get('pointsScored', 0) / max(tim.get('gamesPlayed', 1), 1) if tim.get('pointsScored') else 'N/A'
                    
                    if isinstance(avg_pts, (int, float)):
                        avg_pts = f"{avg_pts:.1f}"
                    
                    print(f"{ime:<25} {gp:<3} {avg_pts:<6}")
                    
        except Exception as e2:
            print(f"Ni alternativni pristup nije uspeo: {e2}")

def prikazi_tim_statistike(season=2024, top_n=5):
    """
    Funkcija koja prikazuje top timove po različitim statistikama
    """
    print(f"\n{'='*60}")
    print(f"TOP {top_n} TIMOVA PO STATISTIKAMA - SEZONA {season}")
    print(f"{'='*60}")
    
    team_stats = TeamStats(competition="E")
    
    try:
        # Dobijamo osnovne statistike timova
        stats_df = team_stats.get_team_stats_single_season(
            endpoint="traditional", 
            season=season, 
            statistic_mode="PerGame"
        )
        
        if not stats_df.empty:
            # Osnovna tabela timova sa ključnim statistikama
            print(f"\nOSNOVNE STATISTIKE TIMOVA (Top {top_n}):")
            print(f"{'Tim':<25} {'GP':<3} {'Pts':<5} {'Reb':<5} {'Ast':<5}")
            print("-" * 50)
            
            for i, (_, tim) in enumerate(stats_df.head(top_n).iterrows(), 1):
                ime = tim.get('team.name', 'N/A')[:24]
                gp = tim.get('gamesPlayed', 'N/A')
                points = tim.get('pointsScored', 'N/A')
                rebounds = tim.get('totalRebounds', 'N/A')
                assists = tim.get('assists', 'N/A')
                
                # Formatiramo brojeve
                if isinstance(points, (int, float)):
                    points = f"{points:.1f}"
                if isinstance(rebounds, (int, float)):
                    rebounds = f"{rebounds:.1f}"
                if isinstance(assists, (int, float)):
                    assists = f"{assists:.1f}"
                
                print(f"{ime:<25} {gp:<3} {points:<5} {rebounds:<5} {assists:<5}")
            
            # Dodajemo top scorere po poenima
            if 'pointsScored' in stats_df.columns:
                top_by_points = stats_df.nlargest(3, 'pointsScored')
                print(f"\n🏆 TOP 3 PO POENIMA:")
                for i, (_, tim) in enumerate(top_by_points.iterrows(), 1):
                    ime = tim.get('team.name', 'N/A')
                    pts = tim.get('pointsScored', 0)
                    print(f"{i}. {ime}: {pts:.1f} poena po meču")
            
        else:
            print("Statistike timova nisu pronađene.")
            
    except Exception as e:
        print(f"Greška pri dobijanju statistika: {e}")

def prikazi_top_scorere_poslednje_utakmice(season=2024, broj_meceva=3, top_n=5):
    """
    Funkcija koja prikazuje top scorere iz poslednjih nekoliko utakmica
    """
    print(f"\n{'='*60}")
    print(f"TOP {top_n} SCORERA IZ POSLEDNJIH {broj_meceva} UTAKMICA - SEZONA {season}")
    print(f"{'='*60}")
    
    boxscore = BoxScoreData(competition="E")
    game_stats = GameStats(competition="E")
    
    try:
        # Dobijamo poslednje mečeve
        mecevi_df = game_stats.get_game_reports_single_season(season)
        
        if not mecevi_df.empty:
            poslednji_mecevi = mecevi_df.tail(broj_meceva)
            game_codes = poslednji_mecevi['Gamecode'].tolist()
            
            print(f"Analiziram mečeve: {game_codes}")
            
            svi_igraci = []
            
            for game_code in game_codes:
                try:
                    # Koristimo ispravnu funkciju
                    player_stats = boxscore.get_player_boxscore_stats_data(season, game_code)
                    
                    if not player_stats.empty:
                        # Dodajemo game_code za reference
                        player_stats['game_code'] = game_code
                        svi_igraci.append(player_stats)
                        print(f"  ✅ Meč {game_code}: {len(player_stats)} igrača")
                    else:
                        print(f"  ❌ Meč {game_code}: Nema podataka")
                        
                except Exception as e:
                    print(f"  ⚠️ Greška za meč {game_code}: {e}")
            
            if svi_igraci:
                # Kombinujemo sve igrače
                combined_df = pd.concat(svi_igraci, ignore_index=True)
                
                print(f"\nUkupno igrača: {len(combined_df)}")
                print(f"Dostupne kolone: {list(combined_df.columns)[:10]}...")
                
                # Pokušavamo da nađemo kolonu za poene
                points_col = None
                for col in ['points', 'Points', 'pts', 'PTS']:
                    if col in combined_df.columns:
                        points_col = col
                        break
                
                if points_col:
                    # Filtriramo samo igrače (ne timove)
                    players_only = combined_df[combined_df['Player'] != 'Total'].copy()
                    players_only = players_only[players_only['Player'] != 'Team'].copy()
                    
                    if not players_only.empty:
                        top_scoreri = players_only.nlargest(top_n, points_col)
                        
                        print(f"\n🏆 TOP {top_n} SCORERA:")
                        print(f"{'Igrač':<25} {'Tim':<8} {'Pts':<4} {'Meč':<8}")
                        print("-" * 50)
                        
                        for i, (_, igrac) in enumerate(top_scoreri.iterrows(), 1):
                            ime = str(igrac.get('Player', 'N/A'))[:24]
                            tim = str(igrac.get('Team', 'N/A'))[:7]
                            poeni = igrac.get(points_col, 'N/A')
                            mec = igrac.get('game_code', 'N/A')
                            
                            print(f"{ime:<25} {tim:<8} {poeni:<4} {mec:<8}")
                    else:
                        print("Nema igrača nakon filtriranja.")
                else:
                    print(f"Kolona za poene nije pronađena.")
                    print(f"Dostupne kolone: {list(combined_df.columns)}")
            else:
                print("Nema dostupnih podataka o igračima.")
                
    except Exception as e:
        print(f"Greška pri dobijanju top scorera: {e}")

def main():
    """
    Glavna funkcija koja pokreće sve primere
    """
    print("EUROLEAGUE API - PRIMER KORIŠĆENJA (ISPRAVLJENA VERZIJA)")
    print("="*65)
    
    # Postavljamo sezonu (2024 znači sezona 2024-25)
    trenutna_sezona = 2024
    
    try:
        # 1. Prikazujemo poslednje mečeve sa statistikama
        prikazi_poslednje_meceve(season=trenutna_sezona, broj_meceva=3)  # Smanjeno na 3
        
        # 2. Prikazujemo top scorere iz poslednjih utakmica
        prikazi_top_scorere_poslednje_utakmice(season=trenutna_sezona, broj_meceva=2, top_n=5)
        
        # 3. Prikazujemo tabelu
        prikazi_tabelu(season=trenutna_sezona)
        
        # 4. Prikazujemo statistike timova
        prikazi_tim_statistike(season=trenutna_sezona, top_n=5)
        
    except Exception as e:
        print(f"Globalna greška: {e}")
        print("Proverite da li je euroleague-api instaliran: pip install euroleague-api")
    
    print(f"\n{'='*65}")
    print("KRAJ PRIMERA")
    print(f"{'='*65}")

if __name__ == "__main__":
    main() 