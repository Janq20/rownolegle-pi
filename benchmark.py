import os
import subprocess
import sys

EXE_PATH = os.path.join("x64", "Release", "rownoleglepi.exe")

def run_single_test(steps, threads):
    """Uruchamia plik exe jeden raz i zwraca wynik"""
    if not os.path.exists(EXE_PATH):
        print(f"B£¥D: Nie znaleziono pliku {EXE_PATH}")
        print("Upewnij siê, ¿e projekt jest zbudowany w trybie Release!")
        return

    print(f"Uruchamiam test: {steps} kroków, {threads} w¹tków...")
    
    try:
        result = subprocess.run(
            [EXE_PATH, str(steps), str(threads)],
            capture_output=True,
            text=True
        )
        
        print("Wyjœcie z programu C++:", result.stdout.strip())
        
    except Exception as e:
        print(f"Wyst¹pi³ b³¹d: {e}")

def main():
    print("--- Test po³¹czenia Python -> C++ ---")
    run_single_test(100000000, 4)

if __name__ == "__main__":
    main()