#pragma once

template<typename T>
class LinearSpace {
    T start_;
    T spacing_;

public:
    [[nodiscard]] constexpr LinearSpace(T st, T sp) noexcept
        : start_{st}, spacing_{sp}
    {}

    [[nodiscard]] constexpr T
    start() const noexcept
    {
        return start_;
    }
    [[nodiscard]] constexpr T
    spacing() const noexcept
    {
        return spacing_;
    }

    [[nodiscard]] constexpr T
    operator[](double i) const noexcept
    {
        return start() + i * spacing();
    }
    [[nodiscard]] constexpr auto
    index_of(T value) const noexcept
    {
        return (value - start()) / spacing();
    }
};
