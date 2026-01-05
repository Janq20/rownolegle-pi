# -*- coding: cp1250 -*-
## @file benchmark.py
#  @brief Skrypt automatyzujący testy wydajnościowe programu C++.
#  @details Skrypt odpowiada za:
#  - Znalezienie pliku wykonywalnego (.exe).
#  - Wielokrotne uruchomienie programu z różnymi parametrami (liczba kroków, liczba wątków).
#  - Parsowanie wyjścia standardowego (stdout) procesu C++.
#  - Wizualizację wyników na wykresie za pomocą biblioteki matplotlib.
#  @author Janq12
#  @date 2025-01-05

import os
import subprocess
import matplotlib.pyplot as plt

# --- KONFIGURACJA ŚCIEŻKI ---

## Lista potencjalnych ścieżek względnych do pliku wykonywalnego.
#  Skrypt sprawdza folder nadrzędny (strukturę VS) oraz bieżący.
paths_to_check = [
    os.path.join("..", "x64", "Release", "rownoleglepi.exe"),
    os.path.join("x64", "Release", "rownoleglepi.exe"),
    "rownoleglepi.exe"
]

## Zmienna przechowująca znalezioną ścieżkę do pliku EXE.
#  Wartość None oznacza, że plik nie został odnaleziony.
EXE_PATH = None

# Logika poszukiwania pliku
for path in paths_to_check:
    if os.path.exists(path):
        EXE_PATH = path
        break

# --- GŁÓWNA FUNKCJA ---

def run_benchmark():
    """!
    @brief Główna funkcja sterująca procesem benchmarku.
    
    @details
    Funkcja wykonuje następujące kroki:
    1. Weryfikuje istnienie pliku `rownoleglepi.exe`.
    2. Definiuje zakresy testów:
       - Kroki całki: 100 mln, 1 mld, 3 mld.
       - Wątki: 1 do 50.
    3. Uruchamia proces potomny (`subprocess`) dla każdej kombinacji parametrów.
    4. Zbiera czasy wykonania parsując wyjście programu C++.
    5. Generuje wykres liniowy wydajności i zapisuje go do pliku PNG.

    @note Wymaga biblioteki `matplotlib`.
    @warning W przypadku braku pliku EXE w trybie Release, funkcja przerywa działanie.
    """
    if EXE_PATH is None:
        print("BŁĄD KRYTYCZNY: Nie znaleziono pliku 'rownoleglepi.exe'!")
        print(f"Szukałem w następujących miejscach:")
        for p in paths_to_check:
            print(f" - {os.path.abspath(p)}")
        print("\nROZWIĄZANIE: Upewnij się, że w Visual Studio zbudowałeś projekt w trybie RELEASE.")
        return

    print(f"Znaleziono plik EXE: {os.path.abspath(EXE_PATH)}")
    
    # Parametry testu
    steps_list = [100_000_000, 1_000_000_000, 3_000_000_000]
    threads_range = range(1, 51)
    
    plt.figure(figsize=(12, 8))

    for steps in steps_list:
        print(f"\n--- Testowanie dla {steps:,} kroków ---")
        times = []
        threads_x = []

        for t in threads_range:
            try:
                # Uruchomienie programu
                res = subprocess.run(
                    [EXE_PATH, str(steps), str(t)],
                    capture_output=True, text=True
                )
                
                parts = res.stdout.strip().split()
                
                if len(parts) >= 1:
                    val = float(parts[0])
                    times.append(val)
                    threads_x.append(t)
                    if t == 1 or t % 5 == 0:
                        print(f"  -> {t} wątków: {val:.4f}s")
            except Exception as e:
                print(f"  Błąd: {e}")

        # Rysowanie wykresu dla danej serii
        plt.plot(threads_x, times, marker='o', markersize=4, label=f'{steps:,} kroków')

    # Stylizacja
    plt.title('Wydajność algorytmu PI (C++ std::thread)')
    plt.xlabel('Liczba wątków')
    plt.ylabel('Czas obliczeń (s)')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    
    filename = "wykres_wydajnosci.png"
    plt.savefig(filename)
    print(f"\nSUKCES! Wykres zapisano jako: {filename}")
    plt.show()

if __name__ == "__main__":
    try:
        run_benchmark()
    except ImportError:
        print("Brakuje biblioteki matplotlib! Zainstaluj: pip install matplotlib")