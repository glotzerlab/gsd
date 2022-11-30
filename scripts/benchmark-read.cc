#include <chrono>
#include <cstdlib>
#include <iostream>
#include <sstream>
#include <vector>

#include "gsd.h"

int main(int argc, char** argv) // NOLINT
    {
    const size_t n_keys = 40000;
    const size_t max_frames = 100;
    std::vector<char> data;

    std::vector<std::string> names;
    for (size_t i = 0; i < n_keys; i++)
        {
        std::ostringstream s;
        s << "log/hpmc/integrate/Sphere/quantity/" << i;
        names.push_back(s.str());
        }

    gsd_handle handle;
    gsd_open(&handle, "test.gsd", GSD_OPEN_READONLY);
    size_t n_frames = gsd_get_nframes(&handle);
    size_t n_read = n_frames;
    if (n_read > max_frames)
        {
        n_read = max_frames;
        }

    std::cout << "Reading test.gsd with: " << n_keys << " keys and " << n_frames << " frames."
              << std::endl;

    auto t1 = std::chrono::high_resolution_clock::now();

    for (size_t frame = 0; frame < n_read; frame++)
        {
        for (auto const& name : names)
            {
            const gsd_index_entry* e;
            e = gsd_find_chunk(&handle, frame, name.c_str());
            if (data.empty())
                {
                data.resize(e->N * e->M * gsd_sizeof_type((gsd_type)e->type));
                }
            gsd_read_chunk(&handle, data.data(), e);
            }
        }

    auto t2 = std::chrono::high_resolution_clock::now();

    std::chrono::duration<double> time_span
        = std::chrono::duration_cast<std::chrono::duration<double>>(t2 - t1);
    double time_per_key = time_span.count() / double(n_keys) / double(n_read);

    const double us = 1e-6;
    std::cout << "Sequential read time: " << time_per_key / us << " microseconds/key." << std::endl;

    gsd_close(&handle);
    }
