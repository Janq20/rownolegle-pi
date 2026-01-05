import os
import subprocess
import matplotlib.pyplot as plt

EXE_PATH = os.path.join("x64", "Release", "rownoleglepi.exe")

def run_benchmark():
    if not os.path.exists(EXE_PATH):
        print("Brak pliku EXE!")
        return

    # Konfiguracja
    steps_list = [100_000_000, 1_000_000_000, 3_000_000_000]
    threads_range = range(1, 51)
    
    # Inicjalizacja wykresu
    plt.figure(figsize=(12, 8))

    for steps in steps_list:
        print(f"Testowanie dla {steps:,} kroków...")
        times = []
        threads_x = [] # Oœ X 

        for t in threads_range:
            try:
                res = subprocess.run(
                    [EXE_PATH, str(steps), str(t)],
                    capture_output=True, text=True
                )
                parts = res.stdout.strip().split()
                
                if len(parts) >= 1:
                    val = float(parts[0])
                    times.append(val)
                    threads_x.append(t)
                    print(f"  -> {t} w¹tków: {val:.4f}s")
            except:
                pass

        # Rysowanie linii dla danej serii
        plt.plot(threads_x, times, marker='o', markersize=4, label=f'{steps:,} kroków')

    # Stylizacja i zapis
    plt.title('Wydajnoœæ algorytmu obliczania PI (std::thread)')
    plt.xlabel('Liczba w¹tków')
    plt.ylabel('Czas obliczeñ (s)')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    
    filename = "wykres_wydajnosci.png"
    plt.savefig(filename)
    print(f"\nGotowe! Wykres zapisano w pliku: {filename}")
    
if __name__ == "__main__":
    try:
        run_benchmark()
    except ImportError:
        print("Brakuje biblioteki matplotlib. Zainstaluj: pip install matplotlib")