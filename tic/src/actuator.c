#include "tic.h"
#include <stdio.h>
#include <windows.h>
#include <time.h>
#include <math.h> 


int main() {
    tic_device **devices;
    size_t device_count;
    tic_error *err;
    err = tic_list_connected_devices(&devices, &device_count);
    if (err != NULL){
        printf("ERROR: %s", tic_error_get_message(err));
    }
    printf("%d", device_count);
    tic_handle *open_handle;
    err = tic_handle_open(*devices, &open_handle);
    if (err != NULL){
        printf("ERROR: %s", tic_error_get_message(err));
    }
    tic_energize(open_handle);
    tic_exit_safe_start(open_handle);
    tic_set_target_velocity(open_handle, 5500000 * -5);
    Sleep(3000);
    
    // FILE *fptr;
    // fptr = fopen("time.txt", "w");
    // clock_t t;
    // t = clock();
    for (int i = 0 ; i < 10; i++) {
        tic_set_target_velocity(open_handle, 5500000 * 5);
        Sleep(2000);
        tic_set_target_velocity(open_handle, 5500000 * -5);
        Sleep(2000);
    }
    // fprintf(fptr, "%lf\t", ((double)(clock() - t))/(double)CLOCKS_PER_SEC);
    // fclose(fptr);

    // double pi = acos(-1.0);
    // double period = 16.0/5.0 * pi;
    // printf("%lf\n", pi);
    // double velocity[20];
    // double angle = 0;
    // for (int i = 0; i < 20; i++) {
    //     velocity[i] = 5.0/2.0*sin(5.0/8.0*angle);
    //     printf("%lf\n", velocity[i]);
    //     angle += period/20.0;
    // }
   
    // for (int i = 0; i < 5; i++){
    //     for (int j = 0; j < 20; j++) {
    //         tic_set_target_velocity(open_handle, 5500000 * velocity[j]);
    //         Sleep(period/20 * 1000);
    //     }
    // }

    tic_deenergize(open_handle);
    return 0;
}