#include <iostream>
#include <sys/time.h>
#include "sum.h"

int main() {
    int a = 5;
    int b = 10;

    int result = sum(a, b);

    std::cout << "The sum of " << a << " and " << b << " is: " << result << std::endl;

    return 0;
}
