import os
import subprocess
import sys

EXE_PATH = os.path.join("x64", "Release", "rownoleglepi.exe")

def run_benchmark():
    if not os.path.exists(EXE_PATH):
        print("Brak pliku EXE. Zbuduj projekt w Release!")
        return

    # Pe³na konfiguracja testów
    steps_list = [100_000_000, 1_000_000_000, 3_000_000_000]
    threads_range = range(1, 51) # W¹tki od 1 do 50
    
    # S³ownik na wyniki: {liczba_krokow: [lista_czasow]}
    results = {}

    for steps in steps_list:
        print(f"\n--- Rozpoczynam seriê dla {steps:,} kroków ---")
        times = []
        
        for t in threads_range:
            try:
                # Uruchomienie procesu
                process = subprocess.run(
                    [EXE_PATH, str(steps), str(t)],
                    capture_output=True, text=True
                )
                
                # Parsowanie wyniku
                parts = process.stdout.strip().split()
                if len(parts) >= 1:
                    exec_time = float(parts[0])
                    times.append(exec_time)
                    # Wypisuje postêp w terminalu
                    print(f"  W¹tki: {t:2} | Czas: {exec_time:.4f}s")
                else:
                    print(f"  B³¹d danych dla {t} w¹tków")
                    
            except Exception as e:
                print(f"  B³¹d krytyczny: {e}")
        
        # Zapisuje ca³¹ seriê do s³ownika
        results[steps] = times

    print("\nBenchmark zakoñczony. Dane zebrane.")
    return results, threads_range

if __name__ == "__main__":
    run_benchmark()