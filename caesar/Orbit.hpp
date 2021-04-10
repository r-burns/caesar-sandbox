#pragma once

#include "LinearSpace.hpp"
#include "mdspan.hpp"
#include "vector.hpp"

#include <stdexcept>
#include <vector>

namespace caesar {

double
cubic_interpolate(const double a,
                  const double b,
                  const double c,
                  const double d,
                  const double x)
{
    const auto y = 1 - x;
    return (x * (c - a * y * y + (c * (y * 3 + 1) - d * y) * x) +
            b * (x * x * (x * 3 - 5) + 2)) /
           2;
}

class Orbit {
    LinearSpace<double> time;
    std::vector<Vector6d> statevecs;

public:
    Orbit(double t0, double tstep, const std::vector<double>& svflat)
        : time(t0, tstep)
    {
        if (svflat.size() % 6 != 0) {
            throw std::runtime_error(
                    "Pos/vel vector size must be a multiple of 6");
        }
        if (svflat.size() == 0) {
            throw std::runtime_error("No state vectors provided");
        }

        statevecs.resize(svflat.size() / 6);
        for (std::size_t i = 0; i < statevecs.size(); i++) {
            Vector6d posvel;
            for (int j = 0; j < 6; j++) {
                posvel[j] = svflat[6 * i + j];
            }
            statevecs[i] = posvel;
        }
    }

    [[nodiscard]] constexpr auto
    start_time() const noexcept
    {
        return time.start();
    }
    [[nodiscard]] auto
    end_time() const noexcept
    {
        return time[statevecs.size() - 1];
    }

    // N-by-2-by-3 extents (nsamples, pos/vel, x/y/z)
    // using ExtentsN23 = extents<dynamic_extent, 2, 3>;
    // basic_mdspan<double, ExtentsN23, layout_right> statevecs;

    [[nodiscard]] auto
    operator()(double t) const
    {
        const auto i = time.index_of(t);

        const auto bi = int(i);
        const auto ai = bi - 1;
        const auto ci = bi + 1;
        const auto di = bi + 2;

        const auto a = statevecs[ai];
        const auto b = statevecs[bi];
        const auto c = statevecs[ci];
        const auto d = statevecs[di];

        Vector6d ret;
        for (int j = 0; j < 6; j++) {
            ret[j] = cubic_interpolate(a[j], b[j], c[j], d[j], i - int(i));
        }
        return ret;
    }
};

} // namespace caesar
