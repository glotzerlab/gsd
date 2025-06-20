#include <chrono>
#include <cstdlib>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

#include "gsd.h"

int main(int argc, char** argv) // NOLINT
    {
    const size_t n_keys = 2048;
    const size_t max_frames = 100;
    std::vector<char> data;

    std::vector<std::string> names;
    for (size_t i = 0; i < n_keys; i++)
        {
        std::ostringstream s;
        s << "key " << i;
        names.push_back(s.str());
        }

    gsd_handle handle;
    auto t1 = std::chrono::high_resolution_clock::now();
    gsd_open(&handle, "test.gsd", GSD_OPEN_READONLY);
    auto t2 = std::chrono::high_resolution_clock::now();
    auto const open_time = std::chrono::duration_cast<std::chrono::duration<double>>(t2 - t1);
    std::cout << "Time to open: " << open_time.count() / 1e-6 << " microseconds\n";

    size_t const n_frames = gsd_get_nframes(&handle);
    size_t n_read = n_frames;
    if (n_read > max_frames)
        {
        n_read = max_frames;
        }

    std::cout << "Reading test.gsd with: " << n_keys << " keys and " << n_frames << " frames."
              << '\n';

    t1 = std::chrono::high_resolution_clock::now();

    size_t total_bytes = 0;
    for (size_t frame = 0; frame < n_read; frame++)
        {
        for (auto const& name : names)
            {
            const gsd_index_entry* e;
            e = gsd_find_chunk(&handle, frame, name.c_str());
            if (e == nullptr)
                {
                std::cout << "ERROR: Chunk `" << name << "` not found\n";
                exit(1);
                }
            if (data.empty())
                {
                data.resize(e->N * e->M * gsd_sizeof_type((gsd_type)e->type));
                }
            total_bytes += e->N * e->M * gsd_sizeof_type((gsd_type)e->type);
            gsd_read_chunk(&handle, data.data(), e);
            }
        }

    t2 = std::chrono::high_resolution_clock::now();

    auto const time_span = std::chrono::duration_cast<std::chrono::duration<double>>(t2 - t1);
    double const time_per_key = time_span.count() / double(n_keys) / double(n_read);
    double const us_per_key = time_per_key / 1e-6;

    std::cout << "Sequential latency   : " << us_per_key << " microseconds/key.\n";

    std::cout << "Sequential throughput: "
              << double(total_bytes) / 1024.0 / 1024.0 / time_span.count() << " MB/s\n";

    gsd_close(&handle);
    }
