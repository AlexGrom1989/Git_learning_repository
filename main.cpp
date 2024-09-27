/*
#include <iostream>
#include <vector>
using std::cin, std::cout, std::vector, std::max, std::min;

int evkl(int, int);

int main(){
    int n;
    cin >> n;
    vector<int> kop(n);
    int amount = 0;
    for (int i = 0; i < n; i++) cin >> kop[i];
    while (kop.size() != 0){
        int ones = 0;
        for (int i = 0; i < n-1; i++){
            int tmp = evkl(kop[i], kop[i+1]);
            amount += tmp;
            ones += tmp == 1;
        }
        amount += ones * (kop.size() - 1) / (ones*(ones-1) / 2)
    }
    cout << amount;
    return 0;
}

int evkl(int a, int b){
    while (a && b){
        if (a > b) a %= b;
        else b %= a;
    }
    return a + b;
}*/
#include <iostream>

int main(){
    
    return 0;
}