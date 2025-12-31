#include <iostream>
#include <vector>
#include <string>
#include <chrono>

using namespace std;
using namespace std::chrono; // Dodano, aby high_resolution_clock był widoczny

int main(int argc, char* argv[]) {
    long long num_steps = 100000000;
    int num_threads = 4;
    double step = 1.0 / (double)num_steps;
    double sum = 0.0;
    auto start = high_resolution_clock::now();
    for (long long i = 0; i < num_steps; i++) {
        double x = (i + 0.5) * step;
        sum += 4.0 / (1.0 + x * x);
    }

    double pi = sum * step;
    cout << "Wynik PI: " << pi << endl;
    if (argc == 3) {
        num_steps = stoll(argv[1]);
        num_threads = stoi(argv[2]);
    }

    cout << "Konfiguracja: " << num_steps << " krokow, " << num_threads << " watkow." << endl;
    return 0;
}