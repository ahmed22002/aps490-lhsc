#include "tic.h"
#include <stdio.h>
#include <windows.h>

typedef tic_error * (*list_connected_devices)(tic_device *** device_list, size_t * device_count);
typedef tic_error * (*set_target_velocity)(tic_handle *, int32_t velocity);
typedef tic_error * (*handle_open)(const tic_device *, tic_handle **);
typedef void        (*handle_close)(tic_handle *);
typedef tic_error * (*deenergize)(tic_handle *);
typedef tic_error * (*energize)(tic_handle *);
typedef tic_error * (*exit_safe_start)(tic_handle *);

int main() {
    HMODULE hDll = LoadLibrary("./libpololu-tic-1.dll");
    if (hDll == NULL) {
        int err = GetLastError();
        printf("Error loading DLL. Error code: %d\n", err);
        return 1;
    }

    // Get the function pointer from the DLL
    list_connected_devices tic_list_connected_devices = (list_connected_devices)GetProcAddress(hDll, "tic_list_connected_devices");
    // if (tic_list_connected_devices == NULL) {
    //         printf("Error finding function\n");
    //         FreeLibrary(hDll);
    //         return 1;
    // }

    set_target_velocity tic_set_target_velocity = (set_target_velocity)GetProcAddress(hDll, "tic_set_target_velocity");
    // if (tic_set_target_velocity == NULL) {
    //         printf("Error finding function: tic_set_target_velocity\n");
    //         FreeLibrary(hDll);
    //         return 1;
    // }

    // handle_open tic_handle_open = (handle_open)GetProcAddress(hDll, "tic_handle_open");
    // if (tic_handle_open == NULL) {
    //         printf("Error finding function: tic_handle_open\n");
    //         FreeLibrary(hDll);
    //         return 1;
    // }

    // handle_close tic_handle_close = (handle_close)GetProcAddress(hDll, "tic_handle_close");
    // if (tic_handle_close == NULL) {
    //         printf("Error finding function: tic_handle_close\n");
    //         FreeLibrary(hDll);
    //         return 1;
    // }

    // deenergize tic_deenergize = (deenergize)GetProcAddress(hDll, "tic_deenergize");
    // if (tic_deenergize == NULL) {
    //         printf("Error finding function: tic_deenergize\n");
    //         FreeLibrary(hDll);
    //         return 1;
    // }
    
    // energize tic_energize = (energize)GetProcAddress(hDll, "tic_energize");
    // if (tic_energize == NULL) {
    //         printf("Error finding function: tic_energize\n");
    //         FreeLibrary(hDll);
    //         return 1;
    // }

    // exit_safe_start tic_exit_safe_start = (exit_safe_start)GetProcAddress(hDll, "tic_exit_safe_start");
    // if (tic_exit_safe_start == NULL) {
    //         printf("Error finding function: tic_exit_safe_start\n");
    //         FreeLibrary(hDll);
    //         return 1;
    // }

    tic_device ***devices;
    size_t device_count;
    tic_list_connected_devices(devices, &device_count);
    printf("%d", device_count);
    // tic_handle **open_handle;
    // tic_handle_open(**devices, open_handle);
    FreeLibrary(hDll);
    return 0;
}