#pragma once

#include <cmath>

namespace caesar {

using idx_t = ptrdiff_t;

template<typename T, ptrdiff_t N>
class Vector {

    T data_[N];

public:
    [[nodiscard]] constexpr Vector() = default;
    [[nodiscard]] constexpr Vector(const T* data)
    {
        std::copy(data, data + N, data_);
    }

    [[nodiscard]] constexpr idx_t
    size() const noexcept
    {
        return N;
    }
    [[nodiscard]] constexpr const T*
    cbegin() const noexcept
    {
        return data_;
    }
    [[nodiscard]] constexpr const T*
    cend() const noexcept
    {
        return data_ + N;
    }
    [[nodiscard]] constexpr const T*
    begin() const noexcept
    {
        return data_;
    }
    [[nodiscard]] constexpr const T*
    end() const noexcept
    {
        return data_ + N;
    }
    [[nodiscard]] constexpr T*
    begin() noexcept
    {
        return data_;
    }
    [[nodiscard]] constexpr T*
    end() noexcept
    {
        return data_ + N;
    }

    [[nodiscard]] constexpr auto
    operator[](idx_t i) const noexcept
    {
        return data_[i];
    }

    [[nodiscard]] constexpr auto&
    operator[](idx_t i) noexcept
    {
        return data_[i];
    }

    template<idx_t K>
    [[nodiscard]] constexpr auto
    head() const
    {
        static_assert(K >= 0, "Slice must have positive length");
        static_assert(K <= N, "Slice cannot exceed vector length");
        return Vector<T, K>(data_);
    }

    template<idx_t K>
    [[nodiscard]] constexpr auto
    tail() const
    {
        static_assert(K >= 0, "Slice must have positive length");
        static_assert(K <= N, "Slice cannot exceed vector length");
        return Vector<T, K>(data_ + (N - K));
    }

    [[nodiscard]] constexpr T
    dot(const Vector& other) const noexcept
    {
        T result = 0;
        for (idx_t i = 0; i < N; i++) {
            result += data_[i] * other[i];
        }
        return result;
    }

    [[nodiscard]] T
    norm() const noexcept
    {
        return std::sqrt(dot(*this));
    }

    [[nodiscard]] constexpr Vector
    operator-(const Vector& other) const noexcept
    {
        Vector result;
        for (idx_t i = 0; i < N; i++) {
            result[i] = data_[i] - other[i];
        }
        return result;
    }
};

using Vector3d = Vector<double, 3>;
using Vector6d = Vector<double, 6>;

} // namespace caesar
