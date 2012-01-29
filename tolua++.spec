%define		apiver		5.1
%define		soname		tolua++%{apiver}
%define		libname		%mklibname %{name} %{apiver}
%define		develname	%mklibname %{name} -d

Summary:	A tool to integrate C/C++ code with Lua
Name:		tolua++
Version:	1.0.93
Release:	%mkrel 3
Group:		Development/Other
License:	MIT
URL:		http://www.codenix.com/~tolua/
Source0:	http://www.codenix.com/~tolua/%{name}-%{version}.tar.bz2
Source1:	custom.py
BuildRequires:	scons
BuildRequires:	lua-devel >= 5.1

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
Requires:	lua-devel >= 5.1
Provides:	tolua++-devel = %{version}-%{release}
Obsoletes:	%{mklibname %{name} 5.1}-devel < 1.0.92-5
Provides:	%{mklibname %{name} 5.1}-devel

%description -n %{develname}
Development files for tolua++.

%prep
%setup -q
%__cp %{SOURCE1} custom.py

%build
scons -Q CCFLAGS="%{optflags}" LINKFLAGS="%{ldflags} -Wl,-soname,lib%{soname}.so"
# Recompile the binary without the soname. An ugly hack from Fedora.
# We need it to fix tolua++: symbol lookup error: tolua++: undefined symbol: tolua_open
gcc -o bin/%{name} src/bin/tolua.o src/bin/toluabind.o -Llib -l%{soname} -llua -ldl -lm

%install
%__rm -rf %{buildroot}

%__mkdir_p %{buildroot}%{_bindir}
%__mkdir %{buildroot}%{_libdir}
%__mkdir %{buildroot}%{_includedir}
%__install -m0755 bin/%{name}  %{buildroot}%{_bindir}
%__install -m0755 lib/lib%{soname}.so* %{buildroot}%{_libdir}
%__install -m0644 include/%{name}.h %{buildroot}%{_includedir}
cd %{buildroot}%{_libdir}
%__ln_s lib%{soname}.so libtolua++.so

%clean
%__rm -rf %{buildroot}

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

