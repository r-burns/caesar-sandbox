#pragma once

#include "mdspan.hpp"

namespace caesar {

using Extents2D = extents<dynamic_extent, dynamic_extent>;

template<typename T>
T
bilerp(basic_mdspan<T, Extents2D, layout_right> im, float x, float y) noexcept
{

    float x0 = x;
    float y0 = y;
    float x1 = x0 + 1;
    float y1 = y0 + 1;

    auto clip = [](float val, float lo, float hi) {
        if (val <= lo)
            return lo;
        if (val >= hi)
            return hi;
        return val;
    };

    x0 = clip(x0, 0, im.extent(1) - 1);
    x1 = clip(x1, 0, im.extent(1) - 1);
    y0 = clip(y0, 0, im.extent(0) - 1);
    y1 = clip(y1, 0, im.extent(0) - 1);

    const auto i00 = im(y0, x0);
    const auto i01 = im(y0, x1);
    const auto i10 = im(y1, x0);
    const auto i11 = im(y1, x1);

    const auto w00 = (x1 - x) * (y1 - y);
    const auto w01 = (x1 - x) * (y - y0);
    const auto w10 = (x - x0) * (y1 - y);
    const auto w11 = (x - x0) * (y - y0);

    return i00 * w00 + i01 * w01 + i10 * w10 + i11 * w11;
}

} // namespace caesar
