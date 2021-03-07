%define		apiver		5.3
%define		soname		tolua++%{apiver}
%define		libname		%mklibname %{name} %{apiver}
%define		develname	%mklibname %{name} -d

Summary:	A tool to integrate C/C++ code with Lua
Name:		tolua++
Version:	1.0.93
Release:	10
Group:		Development/Other
License:	MIT
URL:		http://www.codenix.com/~tolua/
Source0:	http://www.codenix.com/~tolua/%{name}-%{version}.tar.bz2
Patch0:         tolua++-1.0.93-no-buildin-bytecode.patch
Patch1:         tolua++-1.0.93-lua52.patch
Patch2:         tolua++-1.0.93-scons-4.1.0.patch
BuildRequires:	scons
BuildRequires:	lua-devel >= %{apiver}

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
Summary:	Development files for tolua++
Group:		Development/Other
Requires:	%{libname} = %{version}-%{release}
Requires:	lua-devel >= %{apiver}
Provides:	tolua++-devel = %{version}-%{release}
Obsoletes:	%{mklibname %{name} %apiver}-devel < 1.0.92-5
Provides:	%{mklibname %{name} %apiver}-devel

%description -n %{develname}
Development files for tolua++.

%prep
%setup -q
%autopatch -p1
sed -i 's/\r//' doc/%{name}.html

%build
%scons CC=%{__cc} -Q CCFLAGS="%{optflags} $(pkg-config --cflags lua)" tolua_lib=%{soname} LINKFLAGS="%{ldflags} -Wl,-soname,lib%{soname}.so" shared=1

%install
%__mkdir_p %{buildroot}%{_bindir}
%__mkdir %{buildroot}%{_libdir}
%__mkdir %{buildroot}%{_includedir}
%__install -m0755 bin/%{name}  %{buildroot}%{_bindir}
%__install -m0755 lib/lib%{soname}.so* %{buildroot}%{_libdir}
%__install -m0644 include/%{name}.h %{buildroot}%{_includedir}
# For use with Patch2 (not working yet)
%__mkdir -p %{buildroot}%{_datadir}/%{name}
%__install -p -m 644 src/bin/lua/*.lua $RPM_BUILD_ROOT%{_datadir}/%{name}
cd %{buildroot}%{_libdir}
%__ln_s lib%{soname}.so libtolua++.so

%files
%{_bindir}/%{name}

%files -n %{libname}
%{_libdir}/lib%{soname}.so

%files -n %{develname}
%doc README doc/*
%{_libdir}/libtolua++.so
%{_includedir}/%{name}.h
%{_datadir}/tolua++/*.lua
