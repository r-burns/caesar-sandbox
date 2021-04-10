#pragma once

#include "Orbit.hpp"

#include <utility>

namespace caesar {

template<typename Func>
inline auto
bisect(Func f, double a, double b) noexcept
{
    const double tol = 1e-8;
    const int maxiter = 1'000;

    auto fa = f(a);

    for (int i = 0; i < maxiter; i++) {
        const auto c = (a + b) / 2;
        const auto fc = f(c);
        if (fc == 0 or (b - a) / 2 < tol) {
            return c;
        }

        if ((fc > 0) == (fa > 0)) {
            a = c, fa = fc;
        } else {
            b = c;
        }
    }

    // TODO handle errors
    return a;
}

inline auto
xyz_to_rdr(const Vector3d& xyz, const Orbit& orbit)
{

    // not actually, but has the same root for zero-doppler
    auto doppler_eqn = [&](double t) -> double {
        const auto posvel = orbit(t);
        const auto platform_pos = posvel.head<3>();
        const auto platform_vel = posvel.tail<3>();
        return platform_vel.dot(xyz - platform_pos);
    };

    // solve for azimuth time
    const auto t0 = orbit.start_time();
    const auto tf = orbit.end_time();
    const auto t = bisect(doppler_eqn, t0, tf);

    // get corresponding platform position and slant range
    const Vector3d platform_pos = orbit(t).head<3>();
    const double slant_range = (xyz - platform_pos).norm();

    // return results
    return std::make_tuple(t, slant_range);
}

} // namespace caesar
