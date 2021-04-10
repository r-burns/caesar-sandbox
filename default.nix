with import <nixpkgs> {};
let
  pymdspan-src = fetchTarball {
    url = "https://github.com/r-burns/pybind11-mdspan/archive/1b4a8c6a9af2a2ee97701812c2f9f8455075e1cd.tar.gz";
  };
  mdspan = callPackage "${pymdspan-src}/mdspan.nix" {};
  pybind11-mdspan = python3.pkgs.callPackage "${pymdspan-src}/pymdspan.nix" {
    inherit mdspan;
  };
in
stdenv.mkDerivation rec {
  name = "caesar";
  src = lib.cleanSourceWith {
    filter = name: type: let
      basename = baseNameOf (toString name);
    in !(
      lib.hasSuffix ".nix" basename
    );
    src = lib.cleanSource ./.;
  };
  nativeBuildInputs = [
    cmake
  ];
  buildInputs = [
    mdspan
    pybind11-mdspan
  ] ++ (with python3.pkgs; [
    gdal
    matplotlib
    numba
    numpy
    pybind11
    scipy
    tqdm
  ]);
  cmakeFlags = [
    "-DCAESAR_PKGDIR=${python3.sitePackages}"
  ];
}
