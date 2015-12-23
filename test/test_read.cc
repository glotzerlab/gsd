#include "gsd.h"

#include <iostream>
#include <string>
#include <stdlib.h>
using namespace std;

int main()
    {
    uint32_t *data = new uint32_t[1];

    struct gsd_handle *handle = gsd_open("test.gsd", GSD_OPEN_READONLY);
    if (handle == NULL)
        {
        cout << "Unable to open file" << endl;
        return 0;
        }

    cout << "Version: " << handle->header.gsd_version << endl;
    cout << "Application: " << handle->header.application << endl;
    cout << "Schema: " << handle->header.schema << endl;
    cout << "Schema version: " << handle->header.schema_version << endl;
    cout << "index_num_entries: " << handle->index_num_entries << endl;
    cout << "index_allocated_entries: " << handle->header.index_allocated_entries << endl;
    cout << "index_location: " << handle->header.index_location << endl;
    cout << "index_written_entries: " << handle->index_written_entries << endl;
    cout << "namelist_num_entries: " << handle->namelist_num_entries << endl;
    cout << "namelist_allocated_entries: " << handle->header.namelist_allocated_entries << endl;
    cout << "namelist_location: " << handle->header.namelist_location << endl;
    cout << "cur_frame: " << handle->cur_frame << endl;

    cout << "Data:" << endl << endl;
    for (unsigned int j= 0; j < handle->index_num_entries; j++)
        {
        uint16_t id = handle->index[j].id;
        string name(handle->namelist[id].name);
        uint8_t type = handle->index[j].type;
        uint64_t N = handle->index[j].N;
        uint8_t M = handle->index[j].M;
        uint64_t frame = handle->index[j].frame;
        int64_t location = handle->index[j].location;

        const struct gsd_index_entry* chunk = gsd_find_chunk(handle, frame, name.c_str());
        if (chunk == NULL)
            {
            cout << "Chunk not found" << endl;
            continue;
            }

        if (chunk != &(handle->index[j]))
            cout << "No match found: " << chunk - handle->index << " " << j << endl;

        int retval = gsd_read_chunk(handle, (void*)data, chunk);
        if (retval != 0)
            cout << "Error reading chunk" << endl;
        cout << name << " " << int(type) << " (" << N << "x" << (int)M << ") " << frame << " " << location << " " << *data << endl;
        }

    int retval = gsd_close(handle);
    cout << retval << endl;
    delete[] data;
    }
