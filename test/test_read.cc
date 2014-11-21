#include "gsd.h"

#include <iostream>
#include <string>
#include <stdlib.h>
using namespace std;

int main()
    {
    uint32_t *data = new uint32_t[1];

    gsd_handle_t *handle = gsd_open("test.gsd");
    if (handle == NULL)
        {
        cout << "Unable to open file" << endl;
        return 0;
        }

    cout << "Application: " << handle->header.application << endl;
    cout << "Version: " << handle->header.version << endl;
    cout << "index_num_entries: " << handle->header.index_num_entries << endl;
    cout << "index_allocated_entries: " << handle->header.index_allocated_entries << endl;
    cout << "index_location: " << handle->header.index_location << endl;
    cout << "index_written_entries: " << handle->index_written_entries << endl;

    cout << "Data:" << endl << endl;
    for (unsigned int j= 0; j < handle->header.index_num_entries; j++)
        {
        string name(handle->index[j].name);
        uint8_t type = handle->index[j].type;
        uint64_t N = handle->index[j].N;
        uint64_t M = handle->index[j].M;
        uint64_t frame = handle->index[j].frame;
        uint64_t step = handle->index[j].step;
        int64_t location = handle->index[j].location;

        gsd_index_entry_t* chunk = gsd_find_chunk(handle, frame, name.c_str());
        if (chunk != &(handle->index[j]))
            cout << "No match found" << endl;

        int retval = gsd_read_chunk(handle, (void*)data, chunk);
        if (retval != 0)
            cout << "Error reading chunk" << endl;
        cout << name << " " << int(type) << " (" << N << "x" << M << ") " << frame << " " << step << " " << location << " " << *data << endl;
        }

    int retval = gsd_close(handle);
    cout << retval << endl;
    }
