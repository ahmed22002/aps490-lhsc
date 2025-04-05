#include <windows.h>
#include <stdio.h>
#include <time.h>

int main() {
    STARTUPINFO si1, si2;
    PROCESS_INFORMATION pi1, pi2;

    ZeroMemory(&si1, sizeof(si1));
    si1.cb = sizeof(si1);
    ZeroMemory(&pi1, sizeof(pi1));

    ZeroMemory(&si2, sizeof(si2));
    si2.cb = sizeof(si2);
    ZeroMemory(&pi2, sizeof(pi2));

    // if (!CreateProcess("D:\\University\\Capstone\\tic\\actuator.exe", NULL, NULL, NULL, FALSE, 0, NULL, NULL, &si1, &pi1)) {
    //     printf("CreateProcess failed for actuator 1\n");
    //     return 1;
    // }

    // if (!CreateProcess("D:\\University\\Capstone\\tic\\actuator2.exe", NULL, NULL, NULL, FALSE, 0, NULL, NULL, &si2, &pi2)) {
    //     printf("CreateProcess failed for actuator 2\n");
    //     return 1;
    // }
    
    // printf("%lf\n", ((double)clock()/(double)CLOCKS_PER_SEC));
    CreateProcess("D:\\University\\Capstone\\tic\\actuator.exe", NULL, NULL, NULL, FALSE, 0, NULL, NULL, &si1, &pi1);
    CreateProcess("D:\\University\\Capstone\\tic\\actuator2.exe", NULL, NULL, NULL, FALSE, 0, NULL, NULL, &si2, &pi2);

    WaitForSingleObject(pi1.hProcess, INFINITE);
    WaitForSingleObject(pi2.hProcess, INFINITE);

    return 0;
}