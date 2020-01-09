#include <sstream>
#include <iostream>
#include <chrono>
#include <cstdlib>
#include <vector>
#include <unistd.h>

#include "gsd.h"

using namespace std;

int main(int argc, char **argv) // NOLINT
    {
    const size_t n_keys = 65534;
    const size_t n_frames = 1000;
    const size_t key_size = 1;

    vector<double> data(key_size);
    vector<string> names;
    for (size_t i = 0; i < n_keys; i++)
        {
        ostringstream s;
        s << "log/hpmc/integrate/Sphere/quantity/" << i;
        names.push_back(s.str());
        }

    cout << "Writing test.gsd with: " << n_keys << " keys, " << n_frames << " frames, "
         << "and " << key_size << " double(s) per key" << endl;
    gsd_handle handle;
    gsd_create_and_open(&handle, "test.gsd", "app", "schema", 0, GSD_OPEN_APPEND, 0);
    for (size_t frame = 0; frame < n_frames/2; frame++)
        {
        for (auto const &name : names)
            {
            gsd_write_chunk(&handle, name.c_str(), GSD_TYPE_DOUBLE, key_size, 1, 0, &data[0]);
            }
        gsd_end_frame(&handle);
        }
    fsync(handle.fd);

    auto t1 = chrono::high_resolution_clock::now();

    for (size_t frame = 0; frame < n_frames/2; frame++)
        {
        for (auto const &name : names)
            {
            gsd_write_chunk(&handle, name.c_str(), GSD_TYPE_DOUBLE, key_size, 1, 0, &data[0]);
            }
        gsd_end_frame(&handle);
        }
    fsync(handle.fd);

    auto t2 = chrono::high_resolution_clock::now();

    chrono::duration<double> time_span = chrono::duration_cast<chrono::duration<double>>(t2 - t1);
    double time_per_key = time_span.count() / double(n_keys) / double(n_frames)/2;

    const double us = 1e-6;
    std::cout << "Write time: " << time_per_key/us << " microseconds/key." << endl;

    gsd_close(&handle);

    gsd_open(&handle, "test.gsd", GSD_OPEN_READONLY);
    std::cout << "Frames: " << gsd_get_nframes(&handle) << std::endl;
    gsd_close(&handle);
    }
