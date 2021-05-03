%define debug_package %{nil} 

# isl is used by PollyISL, PollyISL is used by mesa
%ifarch %{x86_64}
%bcond_without compat32
%else
%bcond_with compat32
%endif

%define major 23
%define libname %mklibname %{name} %{major}
%define devname %mklibname %{name} -d
%define staticname %mklibname %{name} -s -d
%define lib32name lib%{name}%{major}
%define dev32name lib%{name}-devel
%define static32name lib%{name}-static-devel

# (tpg) optimize it a bit
%global optflags %optflags -O3

Summary:	Integer Set Library
Name:		isl
# BIG FAT WARNING: gcc requires isl. That includes the parts of gcc used by
# clang. When updating to a version that changes the soname, you MUST build
# a compat package for the old version FIRST (see isl13, isl15 packages).
Version:	0.24
Release:	1
License:	MIT
Group:		System/Libraries
Url:		git://repo.or.cz/isl.git
Source0:	http://isl.gforge.inria.fr/isl-%{version}.tar.xz
BuildRequires:	gmp-devel
%if %{with compat32}
BuildRequires:	devel(libgmp)
%endif

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

%package -n %{libname}
Summary:	Integer Set Library
Group:		System/Libraries

%description -n %{libname}
isl is a library for manipulating sets and relations of integer points
bounded by linear constraints. Supported operations on sets include
intersection, union, set difference, emptiness check, convex hull,
(integer) affine hull, integer projection, computing the lexicographic
minimum using parametric integer programming, coalescing and parametric
vertex enumeration.

It also includes an ILP solver based on generalized basis reduction,
transitive closures on maps (which may encode infinite graphs),
dependence analysis and bounds on piecewise step-polynomials.

%package -n %{devname}
Summary:	Development files for the isl Integer Set Library
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
Header files for the isl Integer Set Library.

%package -n %{staticname}
Summary:	Static library for the isl Integer Set Library
Group:		Development/C
Requires:	%{devname} = %{EVRD}

%description -n %{staticname}
Static library for the isl Integer Set Library

%if %{with compat32}
%package -n %{lib32name}
Summary:	Integer Set Library (32-bit)
Group:		System/Libraries

%description -n %{lib32name}
isl is a library for manipulating sets and relations of integer points
bounded by linear constraints. Supported operations on sets include
intersection, union, set difference, emptiness check, convex hull,
(integer) affine hull, integer projection, computing the lexicographic
minimum using parametric integer programming, coalescing and parametric
vertex enumeration.

It also includes an ILP solver based on generalized basis reduction,
transitive closures on maps (which may encode infinite graphs),
dependence analysis and bounds on piecewise step-polynomials.

%package -n %{dev32name}
Summary:	Development files for the isl Integer Set Library
Group:		Development/C
Requires:	%{devname} = %{version}-%{release}
Requires:	%{lib32name} = %{version}-%{release}

%description -n %{dev32name}
Header files for the isl Integer Set Library.

%package -n %{static32name}
Summary:	Static library for the isl Integer Set Library
Group:		Development/C
Requires:	%{dev32name} = %{EVRD}

%description -n %{static32name}
Static library for the isl Integer Set Library
%endif

%prep
%autosetup -p1
autoreconf -fi

export CONFIGURE_TOP="$(pwd)"
%if %{with compat32}
mkdir build32
cd build32
%configure32 --enable-static --enable-portable-binary CFLAGS="%{optflags} -m32"
cd ..
%endif

mkdir build
cd build
%configure --enable-static --enable-portable-binary CFLAGS="%{optflags}"

%build
%if %{with compat32}
%make_build -C build32 CFLAGS="%{optflags} -m32"
%endif
%make_build -C build

%check
# All tests must pass
%if %{with compat32}
%make_build -C build32 check
%endif
%make_build -C build check

%install
%if %{with compat32}
%make_install -C build32
%endif
%make_install -C build

mkdir -p %{buildroot}/%{_datadir}/gdb/auto-load/%{_libdir}
mv %{buildroot}/%{_libdir}/*.py %{buildroot}/%{_datadir}/gdb/auto-load/%{_libdir}

%files -n %{libname}
%{_libdir}/libisl.so.%{major}
%{_libdir}/libisl.so.%{major}.[0-9].[0-9]

%files -n %{devname}
%{_libdir}/libisl.so
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc
%{_datadir}/gdb/auto-load/%{_libdir}/*%{name}*-gdb.py

%files -n %{staticname}
%{_libdir}/*.a

%if %{with compat32}
%files -n %{lib32name}
%{_prefix}/lib/libisl.so.%{major}
%{_prefix}/lib/libisl.so.%{major}.[0-9].[0-9]

%files -n %{dev32name}
%{_prefix}/lib/libisl.so
%{_prefix}/lib/pkgconfig/*.pc
%{_prefix}/lib/libisl.so.*-gdb.py

%files -n %{static32name}
%{_prefix}/lib/*.a
%endif
