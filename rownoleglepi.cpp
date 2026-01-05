/**
 * @file rownoleglepi.cpp
 * @brief Program obliczający przybliżenie liczby PI metodą całki oznaczonej (Suma Riemanna).
 * @author Jan Wójcik
 * @date 2025-01-05
 * * Program wykorzystuje wielowątkowość (std::thread) do zrównoleglenia obliczeń.
 * Algorytm dzieli przedział całkowania na N części i sumuje pola prostokątów
 * pod wykresem funkcji f(x) = 4 / (1 + x^2).
 */

#include <iostream>
#include <vector>
#include <string>
#include <chrono>
#include <thread>
#include <iomanip> 

using namespace std;
using namespace std::chrono;

/**
 * @brief Główna funkcja programu.
 * * Przyjmuje argumenty wiersza poleceń sterujące liczbą kroków i wątków.
 * Uruchamia wątki, zbiera wyniki cząstkowe i wypisuje czas oraz wynik końcowy.
 * * @param argc Liczba argumentów wywołania.
 * @param argv Tablica argumentów:
 * - argv[1]: Liczba kroków (long long)
 * - argv[2]: Liczba wątków (int)
 * @return int Kod wyjścia (0 oznacza sukces).
 */
int main(int argc, char* argv[]) {
    /// Domyślna liczba kroków całkowania (100 milionów)
    long long num_steps = 100000000;
    /// Domyślna liczba wątków
    int num_threads = 4;

    // Parsowanie argumentów wejściowych
    if (argc == 3) {
        num_steps = stoll(argv[1]);
        num_threads = stoi(argv[2]);
    }

    /// Wektor przechowujący sumy cząstkowe obliczone przez każdy wątek
    vector<double> partial_sums(num_threads, 0.0);
    vector<thread> threads;

    /// Szerokość pojedynczego prostokąta (dx)
    double step = 1.0 / (double)num_steps;

    auto start = high_resolution_clock::now();

    /**
     * @brief Wyrażenie lambda wykonujące pracę dla pojedynczego wątku.
     * * Używa schematu "cyclic distribution" (przeplotu), gdzie wątek o indeksie 'id'
     * przetwarza elementy: id, id + num_threads, id + 2*num_threads, itd.
     * Eliminuje to potrzebę dynamicznego przydzielania zakresów.
     * * @param id Indeks wątku (0 do num_threads-1).
     */
    auto worker = [step, num_steps, num_threads, &partial_sums](int id) {
        double local_sum = 0.0;
        for (long long i = id; i < num_steps; i += num_threads) {
            double x = (i + 0.5) * step; // Punkt środkowy
            local_sum += 4.0 / (1.0 + x * x); // Wartość funkcji
        }
        partial_sums[id] = local_sum;
        };

    // Uruchamianie wątków
    for (int i = 0; i < num_threads; ++i) {
        threads.emplace_back(worker, i);
    }

    // Oczekiwanie na zakończenie pracy wątków
    for (auto& th : threads) {
        th.join();
    }

    // Agregacja wyników (Suma Riemanna)
    double total_sum = 0.0;
    for (double p : partial_sums) {
        total_sum += p;
    }
    double pi = total_sum * step;

    auto end = high_resolution_clock::now();
    duration<double> diff = end - start;

    // Wyjście sformatowane dla skryptu benchmark.py: CZAS WYNIK
    cout << fixed << setprecision(6) << diff.count() << " "
        << setprecision(15) << pi << endl;

    return 0;
}