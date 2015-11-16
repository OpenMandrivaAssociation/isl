%define major	13
%define libname	%mklibname %{name} %{major}
%define devname	%mklibname %{name} -d
%define staticname %mklibname %{name} -s -d

Summary:	Integer Set Library
Name:		isl
Version:	0.13
Release:	0.1
License:	MIT
Group:		System/Libraries
Url:		git://repo.or.cz/isl.git
Source0:	http://isl.gforge.inria.fr/isl-0.13.tar.xz
# See http://gcc.gnu.org/bugzilla/show_bug.cgi?id=58012
Patch0:		isl-no-iostream.patch
BuildRequires:	gmp-devel

%description
isl is a library for manipulating sets and relations of integer points
bounded by linear constraints. Supported operations on sets include
intersection, union, set difference, emptiness check, convex hull,
(integer) affine hull, integer projection, computing the lexicographic
minimum using parametric integer programming, coalescing and parametric
vertex enumeration.

It also includes an ILP solver based on generalized basis reduction,
transitive closures on maps (which may encode infinite graphs),
dependence analysis and bounds on piecewise step-polynomials.

%package -n	%{libname}
Summary:	Integer Set Library
Group:		System/Libraries

%description -n	%{libname}
isl is a library for manipulating sets and relations of integer points
bounded by linear constraints. Supported operations on sets include
intersection, union, set difference, emptiness check, convex hull,
(integer) affine hull, integer projection, computing the lexicographic
minimum using parametric integer programming, coalescing and parametric
vertex enumeration.

It also includes an ILP solver based on generalized basis reduction,
transitive closures on maps (which may encode infinite graphs),
dependence analysis and bounds on piecewise step-polynomials.

%package -n	%{devname}
Summary:	Development files for the isl Integer Set Library
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{devname}
Header files for the isl Integer Set Library.

%package -n	%{staticname}
Summary:	Static library for the isl Integer Set Library
Group:		Development/C
Requires:	%{devname} = %{EVRD}

%description -n	%{staticname}
Static library for the isl Integer Set Library

%prep
%setup -q
%apply_patches
autoreconf -fi

%build
%configure2_5x --enable-static
%make

%check
# All tests must pass
make check

%install
%makeinstall_std

%files -n %{libname}
%{_libdir}/libisl.so.%{major}
%{_libdir}/libisl.so.%{major}.[0-9].[0-9]

%files -n %{devname}
%{_libdir}/libisl.so
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*%{name}*-gdb.py

%files -n %{staticname}
%{_libdir}/*.a
