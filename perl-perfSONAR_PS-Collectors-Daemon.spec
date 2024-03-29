Name:           perl-perfSONAR_PS-Collectors-Daemon
Version:        0.09
Release:        1%{?dist}
Summary:        perfSONAR_PS::Collectors::Daemon Perl module
License:        CHECK(GPL or Artistic)
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/perfSONAR_PS-Collectors-Daemon/
Source0:        http://www.cpan.org/modules/by-module/perfSONAR_PS/perfSONAR_PS-Collectors-Daemon-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
Requires:       perl(Config::General) >= 2.3
Requires:       perl(Log::Dispatch::FileRotate) >= 1
Requires:       perl(Log::Dispatch::Screen) >= 1
Requires:       perl(Log::Dispatch::Syslog) >= 1
Requires:       perl(Log::Log4perl) >= 1
Requires:       perl(Module::Load) >= 0.1
Requires:       perl(perfSONAR_PS::Common) >= 0.09
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
The perfSONAR_PS::Collectors::Daemon is the main daemon that is used to
start perfSONAR collectors. To use the daemon, install the modules for the
collectors one is interested in and configure the services in
collector.conf.

%prep
%setup -q -n perfSONAR_PS-Collectors-Daemon-%{version}

%build

# we need to edit the files before we install them
awk "{gsub(/^VARDIR=.*/,\"VARDIR=/var\"); gsub(/^BINDIR=.*/,\"BINDIR=/usr/bin\"); gsub(/^CONFDIR=.*/,\"CONFDIR=/etc/perfsonar\"); print}" perfsonar-collector.init > perfsonar-collector.new
mv perfsonar-collector.new perfsonar-collector.init

perl -i -p -e "s/was_installed = 0/was_installed = 1/" psConfigureCollectors
awk "{gsub(/XXX_CONFDIR_XXX/,\"/etc/perfsonar\"); print}" psConfigureCollectors > psConfigureCollectors.new
mv -f psConfigureCollectors.new psConfigureCollectors

perl -i -p -e "s/was_installed = 0/was_installed = 1/" perfsonar-collector
awk "{gsub(/XXX_LIBDIR_XXX/,\"/usr/lib/perl\"); gsub(/XXX_CONFDIR_XXX/,\"/etc/perfsonar\"); print}" perfsonar-collector > perfsonar-collector.new
mv -f perfsonar-collector.new perfsonar-collector


%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null \;

chmod -R u+rwX,go+rX,go-w $RPM_BUILD_ROOT/*

perldoc -t perlgpl > COPYING
perldoc -t perlartistic > Artistic

%check
make test

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc Changes README COPYING Artistic
%{_bindir}/*
%{_mandir}/man1/*
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Thu Mar 27 2008 aaron@internet2.edu 0.09-1
- Specfile autogenerated.
