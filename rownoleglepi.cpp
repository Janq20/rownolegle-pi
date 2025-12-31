#include <iostream>
#include <vector>
#include <string>
#include <chrono>

using namespace std;

int main(int argc, char* argv[]) {
    long long num_steps = 100000000;
    int num_threads = 4;

    if (argc == 3) {
        num_steps = stoll(argv[1]);
        num_threads = stoi(argv[2]);
    }

    cout << "Konfiguracja: " << num_steps << " krokow, " << num_threads << " watkow." << endl;
    return 0;
}