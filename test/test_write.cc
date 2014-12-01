#include "gsd.h"

#include <iostream>
#include <stdlib.h>
using namespace std;

int main()
    {
    int retval  = gsd_create("test.gsd", "test", "test", 0x000001);
    if (retval != 0)
        {
        cout << "Error creating gsd file" << endl;
        exit(1);
        }

    gsd_handle_t *handle = gsd_open("test.gsd", GSD_OPEN_READWRITE);
    if (handle == NULL)
        {
        cout << "Error writing gsd file" << endl;
        exit(1);
        }

    for (unsigned int i = 0; i < 40; i++)
        {
        int value = i*10;
        int value2 = i*100;

        int err = gsd_write_chunk(handle, "value", GSD_UINT32_TYPE, 1, 1, i, (void*)&value);
        if (err != 0)
            {
            cout << "Error writing gsd file" << endl;
            exit(1);
            }
        err = gsd_write_chunk(handle, "v2", GSD_UINT32_TYPE, 1, 1, i, (void*)&value2);
        if (err != 0)
            {
            cout << "Error writing gsd file" << endl;
            exit(1);
            }
        err = gsd_end_frame(handle);
        if (err != 0)
            {
            cout << "Error writing gsd file" << endl;
            exit(1);
            }
        }

    gsd_close(handle);
    }
