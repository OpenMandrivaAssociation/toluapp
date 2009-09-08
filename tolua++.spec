%define apiver 5.1
%define soname tolua++-%{apiver}
%define libname %mklibname %{name} %{apiver}
%define develname %mklibname %{name} -d

Summary:	A tool to integrate C/C++ code with Lua
Name:		tolua++
Version:	1.0.92
Release:	%mkrel 6
Group:		Development/Other
License:	GPL
URL:		http://www.codenix.com/~tolua/
Source0:	http://www.codenix.com/~tolua/%{name}-%{version}.tar.bz2
Patch0:		tolua++-1.0.92-shared-library.patch
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
%patch0 -p1
sed -i 's/\r//' doc/%{name}.html

%build
scons -Q CCFLAGS="%{optflags} -I%{_includedir}" tolua_lib=%{soname} LINKFLAGS="-Wl,-soname,lib%{soname}.so"

#Recompile the exe without the soname. An ugly hack.
gcc -o bin/%{name} src/bin/tolua.o src/bin/toluabind.o -Llib -l%{soname} -llua -ldl -lm

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_bindir}
mkdir %{buildroot}%{_libdir}
mkdir %{buildroot}%{_includedir}
install -m0755 bin/%{name}  %{buildroot}%{_bindir}
install -m0755 lib/lib%{soname}.so* %{buildroot}%{_libdir}
install -m0644 include/%{name}.h %{buildroot}%{_includedir}
cd %{buildroot}%{_libdir}
ln -s lib%{soname}.so.%{sover} libtolua++.so

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
