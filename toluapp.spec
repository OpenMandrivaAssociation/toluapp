%define		apiver		5.3
%define		soname		tolua++%{apiver}
%define		libname		%mklibname %{name} %{apiver}
%define		develname	%mklibname %{name} -d

Summary:	A tool to integrate C/C++ code with Lua
Name:		tolua++
Version:	1.0.93
Release:	8
Group:		Development/Other
License:	MIT
URL:		http://www.codenix.com/~tolua/
Source0:	http://www.codenix.com/~tolua/%{name}-%{version}.tar.bz2
Patch0:         tolua++-1.0.93-no-buildin-bytecode.patch
Patch1:         tolua++-1.0.93-lua52.patch
BuildRequires:	scons
BuildRequires:	lua-devel >= 5.3

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
Requires:	lua-devel >= 5.3
Provides:	tolua++-devel = %{version}-%{release}
Obsoletes:	%{mklibname %{name} %apiver}-devel < 1.0.92-5
Provides:	%{mklibname %{name} %apiver}-devel

%description -n %{develname}
Development files for tolua++.

%prep
%setup -q
%apply_patches
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



%changelog
* Sun Jan 29 2012 Andrey Bondrov <abondrov@mandriva.org> 1.0.93-3mdv2012.0
+ Revision: 769594
- Fix tolua++ symbol lookup error: tolua_open

* Wed Dec 08 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.93-2mdv2011.0
+ Revision: 615234
- the mass rebuild of 2010.1 packages

* Sat Nov 21 2009 Funda Wang <fwang@mandriva.org> 1.0.93-1mdv2010.1
+ Revision: 468332
- New version 1.0.93

* Wed Sep 09 2009 Thierry Vignaud <tv@mandriva.org> 1.0.92-6mdv2010.0
+ Revision: 434404
- rebuild

* Mon Aug 25 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 1.0.92-5mdv2009.0
+ Revision: 275908
- new devel library policy

* Sun Aug 03 2008 Thierry Vignaud <tv@mandriva.org> 1.0.92-4mdv2009.0
+ Revision: 261613
- rebuild

* Wed Jul 30 2008 Thierry Vignaud <tv@mandriva.org> 1.0.92-3mdv2009.0
+ Revision: 254681
- rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Fri Dec 21 2007 Olivier Blin <blino@mandriva.org> 1.0.92-1mdv2008.1
+ Revision: 136549
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Fri Jun 15 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 1.0.92-1mdv2008.0
+ Revision: 40011
- Import tolua++

