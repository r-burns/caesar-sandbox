#include <caesar/Orbit.hpp>
#include <caesar/bilerp.hpp>
#include <caesar/xyz_to_rdr.hpp>

#include <pybind11/complex.h>
#include <pybind11/eigen.h>
#include <pybind11/mdspan.h>
#include <pybind11/stl.h>

namespace py = pybind11;

PYBIND11_MODULE(caesar, m)
{

    using namespace caesar;

    py::class_<Orbit>(m, "Orbit")
            .def(py::init<double, double, const std::vector<double>>())
            .def("__call__", &Orbit::operator())
            .def("start_time", &Orbit::start_time)
            .def("end_time", &Orbit::end_time);

    m.def("xyz_to_rdr", xyz_to_rdr);

    m.def("bilerp", bilerp<float>);
    m.def("bilerp", bilerp<std::complex<float>>);
}
