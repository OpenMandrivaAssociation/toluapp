%define apiver 5.1
%define soname tolua++%{apiver}
%define libname %mklibname %{name} %{apiver}
%define develname %mklibname %{name} -d

Summary:	A tool to integrate C/C++ code with Lua
Name:		tolua++
Version:	1.0.93
Release:	%mkrel 2
Group:		Development/Other
License:	MIT
URL:		http://www.codenix.com/~tolua/
Source0:	http://www.codenix.com/~tolua/%{name}-%{version}.tar.bz2
Source1:	custom.py
BuildRequires:	scons
BuildRequires:	lua-devel >= 5.1
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
tolua++ is an extended version of tolua, a tool to 
integrate C/C++ code with Lua. tolua++ includes new 
features oriented to c++.

%package -n %{libname}
Summary:	Shared library for tolua++
Group:		Development/Other
Requires:	%{name} = %{version}-%{release}

%description -n %{libname}
Shared library for tolua++.

%package -n %{develname}
Summary:        Development files for tolua++
Group:          Development/Other
Requires:       %{libname} = %{version}-%{release}
Requires:       lua-devel >= 5.1
Provides:	tolua++-devel = %{version}-%{release}
Obsoletes:	%{mklibname %{name} 5.1}-devel < 1.0.92-5
Provides:	%{mklibname %{name} 5.1}-devel

%description -n %{develname}
Development files for tolua++.

%prep
%setup -q
cp %{SOURCE1} custom.py

%build
scons -Q CCFLAGS="%{optflags}" LINKFLAGS="%{ldflags} -Wl,-soname,lib%{soname}.so"

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_bindir}
mkdir %{buildroot}%{_libdir}
mkdir %{buildroot}%{_includedir}
install -m0755 bin/%{name}  %{buildroot}%{_bindir}
install -m0755 lib/lib%{soname}.so* %{buildroot}%{_libdir}
install -m0644 include/%{name}.h %{buildroot}%{_includedir}
cd %{buildroot}%{_libdir}
ln -s lib%{soname}.so libtolua++.so

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%files
%defattr(-,root,root)
%{_bindir}/%{name}

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/lib%{soname}.so

%files -n %{develname}
%defattr(-,root,root)
%doc README doc/*
%{_libdir}/libtolua++.so
%{_includedir}/%{name}.h
