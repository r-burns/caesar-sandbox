#pragma once

#include <cmath>

namespace caesar {

/**
 * An ellipsoid with two axes of equal length
 *
 * A spheroid is parameterized by its semi-major and semi-minor axis lengths,
 * \f$a\f$ and \f$b\f$ as
 *
 * \f[
 * \frac{x^2 + y^2}{a^2} + \frac{z^2}{b^2} = 1
 * \f]
 *
 * In geodesy, a spheroid is typically used as a geodetic reference ellipsoid
 * that approximates the size and shape of the Earth. In such applications, the
 * semi-major axis length describes the equatorial radius and the semi-minor
 * axis length describes the polar radius.
 *
 * Reference ellipsoids are commonly specified by their semi-major axis and
 * flattening constant, \f$f\f$, defined as
 *
 * \f[
 * f = \frac{a - b}{a}
 * \f]
 *
 * The flattening is a measure of the ellipticity of the spheroid. If the
 * flattening is between 0 and 1, the spheroid is oblate (\f$a > b\f$). If it's
 * equal to 0, the spheroid is a perfect sphere (\f$a == b\f$). If it's less
 * than zero, the spheroid is prolate (\f$a < b\f$).
 *
 * \see wgs84_ellipsoid
 */
class Spheroid {
public:
    /**
     * Construct a new Spheroid object.
     *
     * \param[in] a semi-major axis length
     * \param[in] f flattening constant
     */
    constexpr Spheroid(double a, double f) noexcept : a_(a), f_(f) {}

    /**
     * Return the semi-major axis length.
     *
     * In geodetic applications, this is the equatorial radius.
     *
     * \see Spheroid::a
     */
    [[nodiscard]] constexpr double
    semimajor_axis() const noexcept
    {
        return a();
    }

    /** Same as Spheroid::semimajor_axis() */
    [[nodiscard]] constexpr double
    a() const noexcept
    {
        return a_;
    }

    /**
     * Return the semi-minor axis length.
     *
     * In geodetic applications, this is the polar radius.
     *
     * \see Spheroid::b
     */
    [[nodiscard]] constexpr double
    semiminor_axis() const noexcept
    {
        return b();
    }

    /** Same as Spheroid::semiminor_axis() */
    [[nodiscard]] constexpr double
    b() const noexcept
    {
        return a() * (1. - f());
    }

    /**
     * Return the (first) flattening.
     *
     * \see Spheroid::f
     */
    [[nodiscard]] constexpr double
    flattening() const noexcept
    {
        return f();
    }

    /** Same as Spheroid::flattening() */
    [[nodiscard]] constexpr double
    f() const noexcept
    {
        return f_;
    }

    /**
     * Return the inverse flattening constant, \f$\frac{1}{f}\f$.
     *
     * \see Spheroid::flattening
     */
    [[nodiscard]] constexpr double
    inverse_flattening() const
    {
        return 1. / f();
    }

    /**
     * Return the third flattening.
     *
     * The third flattening, \f$n\f$, is defined as
     *
     * \f[
     * n = \frac{a - b}{a + b}
     * \f]
     */
    [[nodiscard]] constexpr double
    third_flattening() const noexcept
    {
        return f() / (2. - f());
    }

    /**
     * Return the eccentricity of the spheroid.
     *
     * The eccentricity, ]f$e\f$, is defined as
     *
     * \f[
     * e = \sqrt{1 - \frac{b^2}{a^2}}
     * \f]
     */
    [[nodiscard]] double
    eccentricity() const
    {
        return std::sqrt(squared_eccentricity());
    }

    /**
     * Return the squared eccentricity.
     *
     * \see Spheroid::eccentricity
     */
    [[nodiscard]] constexpr double
    squared_eccentricity() const noexcept
    {
        return f() * (2. - f());
    }

    /** Compare two Spheroid objects. */
    [[nodiscard]] friend constexpr bool
    operator==(const Spheroid& lhs, const Spheroid& rhs) noexcept
    {
        return lhs.a() == rhs.a() and lhs.f() == rhs.f();
    }

    /** \copydoc operator==(const Spheroid&, const Spheroid&) */
    [[nodiscard]] friend constexpr bool
    operator!=(const Spheroid& lhs, const Spheroid& rhs) noexcept
    {
        return not(lhs == rhs);
    }

private:
    double a_;
    double f_;
};

/** World Geodetic System 1984 (WGS 84) reference ellipsoid */
inline constexpr Spheroid wgs84_ellipsoid(6378137.0, 1.0 / 298.257223563);

} // namespace caesar
