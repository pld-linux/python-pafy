#
# Conditional build:
%bcond_with	doc	# don't build doc
%bcond_with	tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define		module		pafy
%define		egg_name	pafy
%define		pypi_name	pafy
Summary:	Retrieve YouTube content and metadata
Name:		python-%{pypi_name}
Version:	0.5.4
Release:	3
License:	LGPLv3
Group:		Libraries/Python
Source0:	https://files.pythonhosted.org/packages/source/p/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
# Source0-md5:	092930504c7e4fcea30b7446fa1878c7
URL:		http://np1.github.io/pafy/
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with python2}
BuildRequires:	python-modules
BuildRequires:	python-setuptools
BuildRequires:	python-youtube-dl
%endif
%if %{with python3}
BuildRequires:	python3-modules
BuildRequires:	python3-setuptools
BuildRequires:	python3-youtube-dl
%endif
Requires:	python-modules
Requires:	python-youtube-dl
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Features:

- Retreive metadata such as viewcount, duration, rating, author,
  thumbnail, keywords
- Download video or audio at requested resolution / bitrate / format /
  filesize
- Command line tool (ytdl) for downloading directly from the command
  line
- Retrieve the URL to stream the video in a player such as vlc or
  mplayer
- Works with age-restricted videos and non-embeddable videos
- Small, standalone, single importable module file (pafy.py)
- Select highest quality stream for download or streaming
- Download video only (no audio) in m4v or webm format
- Download audio only (no video) in ogg or m4a format
- Retreive playlists and playlist metadata
- Works with Python 2.6+ and 3.3+
- Optionally depends on youtube-dl (recommended; more stable)

%description -l pl.UTF-8

%package -n python3-%{module}
Summary:	-
Summary(pl.UTF-8):	-
Group:		Libraries/Python
Requires:	python3-modules
Requires:	python3-youtube-dl

%description -n python3-%{module}

%description -n python3-%{module} -l pl.UTF-8

%package apidocs
Summary:	%{module} API documentation
Summary(pl.UTF-8):	Dokumentacja API %{module}
Group:		Documentation

%description apidocs
API documentation for %{module}.

%description apidocs -l pl.UTF-8
Dokumentacja API %{module}.

%prep
%setup -q -n %{pypi_name}-%{version}

rm -r %{egg_name}.egg-info

%build
%if %{with python2}
%py_build %{?with_tests:test}
%endif

%if %{with python3}
%py3_build %{?with_tests:test}
%endif

%if %{with doc}
cd docs
%{__make} -j1 html
rm -rf _build/html/_sources
%endif

%install
rm -rf $RPM_BUILD_ROOT
%if %{with python2}
%py_install
%py_postclean

mv $RPM_BUILD_ROOT%{_bindir}/ytdl{,2}
%endif

%if %{with python3}
%py3_install
mv $RPM_BUILD_ROOT%{_bindir}/ytdl{,3}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc README.rst
%attr(755,root,root) %{_bindir}/ytdl2
%{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/%{egg_name}-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc README.rst
%attr(755,root,root) %{_bindir}/ytdl3
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{egg_name}-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/*
%endif
