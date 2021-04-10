#pragma once

#if __has_include(<mdspan>)
#include <mdspan>
using std::basic_mdspan;
using std::dynamic_extent;
using std::extents;
using std::layout_left;
using std::layout_right;
using std::layout_stride;
} // namespace caesar
#elif __has_include(<experimental/mdspan>)
#include <experimental/mdspan>
namespace caesar {
using std::experimental::basic_mdspan;
using std::experimental::dynamic_extent;
using std::experimental::extents;
using std::experimental::layout_left;
using std::experimental::layout_right;
using std::experimental::layout_stride;
} // namespace caesar
#else
#error "Could not find mdspan header!"
#endif
