# -*- coding: cp1250 -*-
import os
import subprocess
import matplotlib.pyplot as plt

# --- KONFIGURACJA ŚCIEŻKI ---
# Sprawdzamy dwie możliwe lokalizacje pliku .exe:
# 1. Standardowa dla VS: folder solucji (..) -> x64 -> Release
# 2. Alternatywna: bezpośrednio w folderze x64/Release (jeśli uruchamiasz z innej lokalizacji)
paths_to_check = [
    os.path.join("..", "x64", "Release", "rownoleglepi.exe"),
    os.path.join("x64", "Release", "rownoleglepi.exe"),
    "rownoleglepi.exe"
]

EXE_PATH = None
for path in paths_to_check:
    if os.path.exists(path):
        EXE_PATH = path
        break

# --- GŁÓWNA FUNKCJA ---
def run_benchmark():
    # Jeśli po pętli EXE_PATH nadal jest None, to znaczy, że pliku nie ma nigdzie
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
                    # Wypisujemy postęp co 5 wątków
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