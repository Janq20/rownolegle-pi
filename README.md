# 🧮 Równoległe Pi (Parallel Pi) — C++ & Python

Repozytorium "Równoległe Pi" zawiera prosty i wydajny program do przybliżania liczby Pi metodą całki oznaczonej (Suma Riemanna) z implementacją wielowątkową w C++ oraz skryptem w Pythonie do automatycznego benchmarku i wizualizacji wyników.

Autor: Jan Wójcik  
Data: 2026-01-05

---

## 🧾 Krótkie streszczenie

Program oblicza przybliżenie liczby π z całki f(x) = 4 / (1 + x^2) na przedziale [0,1] używając sum Riemanna. Obliczenia wykonane są w C++ z użyciem `std::thread`, a dystrybucja pracy pomiędzy wątki jest dokonywana schematem "cyclic distribution" (przeplot). Skrypt `benchmark.py` uruchamia program z różnymi parametrami i tworzy wykresy wydajności (matplotlib).

---

## 📁 Zawartość repozytorium

- `rownoleglepi.cpp` — kernel obliczeniowy (C++, wielowątkowość)
- `benchmark.py` — skrypt automatycznego benchmarku i wizualizacji
- `Równoległe_Pi.pdf` — dokumentacja / praca inżynierska (opcjonalnie)
- `wykres_wydajnosci.png` — przykładowy wynik benchmarku (po uruchomieniu skryptu)

---

## 🔧 Kompilacja (C++)

Zalecane: kompilator wspierający C++20 (g++, clang++ lub MSVC).

Przykład kompilacji (Linux / MinGW) z optymalizacjami:
```
g++ -O3 -march=native -std=c++20 -pthread rownoleglepi.cpp -o rownoleglepi
```

Na Windows (Visual Studio) — zbuduj projekt w trybie Release. Plik wykonywalny zwykle znajdzie się w `x64/Release/rownoleglepi.exe`.

---

## ▶️ Uruchamianie programu

Składnia:
```
./rownoleglepi [liczba_kroków] [liczba_wątków]
```

- `liczba_kroków` (long long) — liczba podprzedziałów (domyślnie 100000000)
- `liczba_wątków` (int) — liczba wątków (domyślnie 4)

Przykład:
```
./rownoleglepi 100000000 8
```

Wyjście programu:
- drukuje dwa pola oddzielone spacją:
  - czas wykonania (s)
  - przybliżenie pi (z dużą precyzją)

Format: `CZAS WYNIK` (skrypt `benchmark.py` oczekuje takiego formatu).

---

## 🐍 Benchmark i wizualizacja (Python)

Skrypt `benchmark.py` automatyzuje uruchomienia i tworzy wykresy przy użyciu matplotlib.

Jak użyć:
1. Upewnij się, że plik wykonawczy (`rownoleglepi` lub `rownoleglepi.exe`) jest w jednym z oczekiwanych miejsc:
   - `../x64/Release/rownoleglepi.exe`
   - `x64/Release/rownoleglepi.exe`
   - `rownoleglepi.exe` (bieżący katalog)
2. Uruchom:
```
python benchmark.py
```

Skrypt domyślnie testuje kombinacje:
- kroki: 100_000_000, 1_000_000_000, 3_000_000_000
- wątki: 1..50

Uwaga: duże liczby kroków (np. 3e9) mogą trwać bardzo długo — planuj testy ostrożnie.

Wymagania:
- Python 3.x
- matplotlib (zainstaluj: `pip install matplotlib`)

---

## ⚙️ Sposób działania programu (krótkie wyjaśnienie)

- Algorytm: przybliżenie π poprzez sumę prostokątów funkcji f(x) = 4/(1+x^2) na [0,1].
- Dystrybucja pracy: cyclic distribution — wątek o id przetwarza indeksy id, id + n_threads, id + 2*n_threads, ...
  - działa to dobrze dla równomiernego rozkładu pracy i zmniejsza ryzyko nierównomiernego obciążenia z powodu planisty.
- Synchronizacja: brak blokad w pętli obliczeniowej; każdy wątek akumuluje wynik lokalnie, a na końcu wartości są sumowane.

---

## 🔍 Wskazówki do benchmarkowania i optymalizacji

- Ustaw `-O3` i (jeśli to możliwe) `-march=native` aby skorzystać z rozszerzeń procesora.
- Dla porównań używaj liczby wątków równej liczbie logicznych lub fizycznych rdzeni — sprawdź `std::thread::hardware_concurrency()` lub `nproc`.
- Pamiętaj, że hyper-threading może dawać mniejsze zyski niż dodatkowe fizyczne rdzenie.
- Duże wartości `num_steps` dają dokładniejsze przybliżenie ale wydłużają czas; możesz testować skalę (1e7, 1e8, 1e9).
- Jeśli chcesz profilować pamięć/CPU, użyj narzędzi systemowych (perf, vtune, Visual Studio Profiler).

---

## ✅ Testy i walidacja

- Program wypisuje wartość przybliżoną π — porównaj z M_PI (lub znaną wartością) by sprawdzić poprawność.
- Benchmark: uruchamiać kilka razy (szczególnie dłuższe testy) i brać średnie lub medianę pomiarów, by ograniczyć szum wyników.

---

## 📝 Dodatkowe uwagi

- Kod C++ używa typu `long long` do iteracji (bezpieczne dla dużych liczby kroków).
- Skrypt `benchmark.py` w kodowaniu CP1250 (nagłówek pliku) — jeżeli masz problemy z kodowaniem, zmień nagłówek lub użyj UTF-8.

---

## 📜 Licencja

Zawartość repozytorium domyślnie dostępna do użytku edukacyjnego. Jeżeli chcesz, mogę dodać plik LICENSE (np. MIT) — daj znać, jaką licencję preferujesz.

---

## 🤝 Współpraca / Contributing

Chcesz rozszerzyć projekt? Kilka pomysłów:
- dodać warianty dystrybucji pracy (blokowa, dynamiczna),
- implementacja SIMD (wektoryzacja),
- wersja z OpenMP / TBB,
- automatyczne CI do budowania i uruchamiania szybkich testów.

Jeśli chcesz, mogę przygotować PR z dodanym plikiem LICENSE i/lub skryptami CI (GitHub Actions).

---
