#include <chrono>
#include <cstdlib>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

#ifdef _WIN32
#include <io.h>
#define fsync _commit
#else // linux / mac
#include <unistd.h>
#endif

#include "gsd.h"

double benchmark(size_t buffer)
    {
    const size_t n_keys = 2;
    const size_t key_size = 2048;
    const size_t target_file_size = 256 * 1024 * 1024;

    const size_t n_frames = target_file_size / key_size / n_keys / sizeof(double);

    std::vector<double> data(key_size);

    for (size_t i = 0; i < key_size; i++)
        {
        data[i] = (double)i;
        }

    std::vector<std::string> names;
    for (size_t i = 0; i < n_keys; i++)
        {
        std::ostringstream s;
        s << "log/hpmc/integrate/Sphere/quantity/" << i;
        names.push_back(s.str());
        }

    // std::cout << "Writing test.gsd with: " << n_keys << " keys, " << n_frames << " frames, "
    //           << "and " << key_size << " double(s) per key" << '\n';


    gsd_handle handle;
    gsd_create_and_open(&handle, "test.gsd", "app", "schema", 0, GSD_OPEN_APPEND, 0);
    gsd_set_maximum_write_buffer_size(&handle, buffer);

    auto t1 = std::chrono::high_resolution_clock::now();
    for (size_t frame = 0; frame < n_frames; frame++)
        {
        for (auto const& name : names)
            {
            gsd_write_chunk(&handle, name.c_str(), GSD_TYPE_DOUBLE, key_size, 1, 0, data.data());
            }
        gsd_end_frame(&handle);
        }
    gsd_flush(&handle);

    auto t2 = std::chrono::high_resolution_clock::now();

    std::chrono::duration<double> const time_span
        = std::chrono::duration_cast<std::chrono::duration<double>>(t2 - t1);
    double const time_per_key = time_span.count() / double(n_keys) / double(n_frames);

    // const double us = 1e-6;
    // std::cout << "Write time: " << time_per_key / us << " microseconds/key." << '\n';
    // std::cout << "Write time: " << time_per_key / us * n_keys << " microseconds/frame." << '\n';

    const double mb_per_second
        = double(key_size * 8 + static_cast<const size_t>(32) * static_cast<const size_t>(2))
          / 1048576.0 / time_per_key;
    // std::cout << "MB/s: " << mb_per_second << " MB/s." << '\n';

    gsd_close(&handle);

    // gsd_open(&handle, "test.gsd", GSD_OPEN_READONLY);
    // std::cout << "Frames: " << gsd_get_nframes(&handle) << '\n';
    // gsd_close(&handle);

    return mb_per_second;
    }

int main(int argc, char** argv) // NOLINT
    {
    size_t buffer = 65536;

    std::cout << "[";
    while (buffer <= 64 * 1024 * 1024)
        {
        std::cout << "[";
        std::cout << buffer << ", " << benchmark(buffer) << "]," <<std::endl;
        buffer *= 2;
        }
    std::cout << "]" << std::endl;
    }
