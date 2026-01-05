#include <iostream>
#include <vector>
#include <string>
#include <chrono>
#include <thread>

using namespace std;
using namespace std::chrono;

int main(int argc, char* argv[]) {
    long long num_steps = 100000000;
    int num_threads = 4;

    if (argc == 3) {
        num_steps = stoll(argv[1]);
        num_threads = stoi(argv[2]);
    }

    vector<double> partial_sums(num_threads, 0.0);
    vector<thread> threads;
    double step = 1.0 / (double)num_steps;
    double sum = 0.0;

    auto start = high_resolution_clock::now();

    auto worker = [step, num_steps, num_threads, &partial_sums](int id) {
        double local_sum = 0.0;
        for (long long i = id; i < num_steps; i += num_threads) {
            double x = (i + 0.5) * step;
            local_sum += 4.0 / (1.0 + x * x);
        }
        partial_sums[id] = local_sum;
        };

    for (int i = 0; i < num_threads; ++i) {
        threads.emplace_back(worker, i);
    }

    for (auto& th : threads) {
        th.join();
    }

    double pi = sum * step;

    cout << "Wynik PI: " << pi << endl;

    cout << "Konfiguracja: " << num_steps << " krokow, " << num_threads << " watkow." << endl;

    return 0;
}