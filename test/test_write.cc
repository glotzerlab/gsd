#include "gsd.h"

#include <iostream>
#include <stdlib.h>
#include <errno.h>
using namespace std;

int main()
    {
    int retval  = gsd_create("test.gsd", "test", "test", gsd_make_version(0,4));
    if (retval != 0)
        {
        cout << "Error creating gsd file" << endl;
        exit(1);
        }

    struct gsd_handle handle;
    retval = gsd_open(&handle, "test.gsd", GSD_OPEN_READWRITE);
    if (retval != 0)
        {
        cout << "Error opening gsd file" << endl;
        exit(1);
        }

    for (unsigned int i = 0; i < 3000; i++)
        {
        int value = i*10;
        int value2 = i*100;

        int err = gsd_write_chunk(&handle, "value", GSD_TYPE_UINT32, 1, 1, 0, (void*)&value);
        if (err != 0)
            {
            cout << "Error writing gsd file: " << strerror(errno) << endl;
            exit(1);
            }
        err = gsd_write_chunk(&handle, "v2", GSD_TYPE_UINT32, 1, 1, 0, (void*)&value2);
        if (err != 0)
            {
            cout << "Error writing gsd file 2" << endl;
            exit(1);
            }
        err = gsd_end_frame(&handle);
        if (err != 0)
            {
            cout << "Error writing gsd file 3" << endl;
            exit(1);
            }
        }

    gsd_close(&handle);
    }
