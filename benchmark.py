import os
import subprocess
import sys

EXE_PATH = os.path.join("x64", "Release", "rownoleglepi.exe")

def run_single_test(steps, threads):
    """Uruchamia plik exe i zwraca czas wykonania jako float"""
    if not os.path.exists(EXE_PATH):
        print(f"B£¥D: Nie znaleziono pliku {EXE_PATH}")
        return None

    try:
        result = subprocess.run(
            [EXE_PATH, str(steps), str(threads)],
            capture_output=True,
            text=True
        )
        
        # Parsowanie: dzielimy wyjœcie "CZAS WYNIK" na czêœci
        output_parts = result.stdout.strip().split()
        
        # Sprawdzam czy dostaliœmy poprawne dane
        if len(output_parts) >= 1:
            time_taken = float(output_parts[0])
            return time_taken
        else:
            print("B³¹d: Program C++ nie zwróci³ czasu.")
            return None
            
    except Exception as e:
        print(f"Wyst¹pi³ b³¹d: {e}")
        return None

def main():
    print("--- Test parsowania danych ---")
    # Sprawdzam czy funkcja poprawnie zwraca liczbê
    czas = run_single_test(100000000, 4)
    if czas is not None:
        print(f"Sukces! Otrzymany czas to: {czas} sekundy")
    else:
        print("Test nieudany.")

if __name__ == "__main__":
    main()