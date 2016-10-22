%{?scl:%scl_package perl-CPAN-Meta}

Name:           %{?scl_prefix}perl-CPAN-Meta
Summary:        Distribution metadata for a CPAN dist
Version:        2.150005
Release:        366%{?dist}
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/CPAN-Meta/
Source0:        http://search.cpan.org/CPAN/authors/id/D/DA/DAGOLDEN/CPAN-Meta-%{version}.tar.gz
BuildArch:      noarch
# Build
BuildRequires:  %{?scl_prefix}perl
BuildRequires:  %{?scl_prefix}perl-generators
BuildRequires:  %{?scl_prefix}perl(ExtUtils::MakeMaker) >= 6.17
# Module
BuildRequires:  %{?scl_prefix}perl(Carp)
BuildRequires:  %{?scl_prefix}perl(CPAN::Meta::Requirements) >= 2.121
BuildRequires:  %{?scl_prefix}perl(Parse::CPAN::Meta) >= 1.4414
BuildRequires:  %{?scl_prefix}perl(Scalar::Util)
BuildRequires:  %{?scl_prefix}perl(strict)
BuildRequires:  %{?scl_prefix}perl(version) >= 0.88
BuildRequires:  %{?scl_prefix}perl(warnings)
# Main test suite
BuildRequires:  %{?scl_prefix}perl(Data::Dumper)
BuildRequires:  %{?scl_prefix}perl(File::Basename)
BuildRequires:  %{?scl_prefix}perl(File::Spec)
BuildRequires:  %{?scl_prefix}perl(File::Temp) >= 0.20
BuildRequires:  %{?scl_prefix}perl(IO::Dir)
BuildRequires:  %{?scl_prefix}perl(overload)
BuildRequires:  %{?scl_prefix}perl(Test::More) >= 0.88
BuildRequires:  %{?scl_prefix}perl(utf8)
# Runtime
Requires:       %{?scl_prefix}perl(:MODULE_COMPAT_%(%{?scl:scl enable %{scl} '}eval "$(perl -V:version)";echo $version%{?scl:'}))
Requires:       %{?scl_prefix}perl(version) >= 0.88

%{?perl_default_filter}

# Remove under-specified dependencies
%if 0%{?rhel} < 7
# RPM 4.8 style
%{?filter_setup:
%filter_from_requires /^%{?scl_prefix}perl(CPAN::Meta::Converter)$/d
%filter_from_requires /^%{?scl_prefix}perl(CPAN::Meta::Requirements)$/d
%filter_from_requires /^%{?scl_prefix}perl(Parse::CPAN::Meta) >= 1.4400/d
%?perl_default_filter
}
%else
# RPM 4.9 style
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^%{?scl_prefix}perl\\(CPAN::Meta::Converter\\)$
%global __requires_exclude %{__requires_exclude}|^%{?scl_prefix}perl\\(CPAN::Meta::Requirements\\)$
%global __requires_exclude %{__requires_exclude}|^%{?scl_prefix}perl\\(Parse::CPAN::Meta\\) >= 1.4400
%endif

%description
Software distributions released to the CPAN include a META.json or, for older
distributions, META.yml, which describes the distribution, its contents, and
the requirements for building and installing the distribution. The data
structure stored in the META.json file is described in CPAN::Meta::Spec.

%prep
%setup -q -n CPAN-Meta-%{version}

# silence rpmlint warnings
sed -i '1s,#!.*perl,%(%{?scl:scl enable %{scl} '}perl -MConfig -e %{?scl:'"}'%{?scl:"'}print $Config{startperl}%{?scl:'"}'%{?scl:"'}%{?scl:'}),' t/*.t

%build
%{?scl:scl enable %{scl} '}perl Makefile.PL INSTALLDIRS=vendor && make %{?_smp_mflags}%{?scl:'}

%install
%{?scl:scl enable %{scl} '}make pure_install DESTDIR=%{buildroot}%{?scl:'}
find %{buildroot} -type f -name .packlist -exec rm -f {} +
%{_fixperms} %{buildroot}

%check
%{?scl:scl enable %{scl} '}make test%{?scl:'}

%files
%doc LICENSE
%doc Changes CONTRIBUTING.mkdn history README Todo t/
%{perl_vendorlib}/CPAN/
%{_mandir}/man3/CPAN::Meta.3*
%{_mandir}/man3/CPAN::Meta::Converter.3*
%{_mandir}/man3/CPAN::Meta::Feature.3*
%{_mandir}/man3/CPAN::Meta::History.3*
%{_mandir}/man3/CPAN::Meta::History::Meta_1_0.3*
%{_mandir}/man3/CPAN::Meta::History::Meta_1_1.3*
%{_mandir}/man3/CPAN::Meta::History::Meta_1_2.3*
%{_mandir}/man3/CPAN::Meta::History::Meta_1_3.3*
%{_mandir}/man3/CPAN::Meta::History::Meta_1_4.3*
%{_mandir}/man3/CPAN::Meta::Merge.3*
%{_mandir}/man3/CPAN::Meta::Prereqs.3*
%{_mandir}/man3/CPAN::Meta::Spec.3*
%{_mandir}/man3/CPAN::Meta::Validator.3*

%changelog
* Mon Jul 11 2016 Petr Pisar <ppisar@redhat.com> - 2.150005-366
- SCL

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.150005-365
- Increase release to favour standalone package

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.150005-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.150005-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 13 2015 Paul Howarth <paul@city-fan.org> - 2.150005-1
- Update to 2.150005
  - Metadata merging now does deep hash merging as long as keys don't conflict
  - Serialized CPAN::Meta objects now include a x_serialization_backend entry
  - Declared extra developer prereq
  - Added test for 'x_deprecated' field in "provides"
  - Noted explicitly that historical META spec files are licensed under the
    same terms as Perl
  - Changed some test data from UTF-8 to ASCII

* Thu Jun 04 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.150001-345
- Increase release to favour standalone package

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.150001-2
- Perl 5.22 rebuild

* Tue Mar 10 2015 Paul Howarth <paul@city-fan.org> - 2.150001-1
- Update to 2.150001
  - Include allowed values for license field in 1.x historic licenses rather
    than linking to Module::Build
  - Documented when fragment merging became available

* Tue Jan 13 2015 Petr Pisar <ppisar@redhat.com> - 2.143240-2
- Correct dependencies

* Thu Nov 20 2014 Paul Howarth <paul@city-fan.org> - 2.143240-1
- Update to 2.143240
  - Give correct path in nested merges such as resources
  - Removed strings test that should have been removed when
    CPAN::Meta::Requirements was removed to a separate dist

* Tue Nov 11 2014 Petr Šabata <contyk@redhat.com> - 2.142690-1
 - Update to 2.142690
  - Fixed use of incorrect method in CPAN::Meta::Merge implementation
  - Clarified documentation that no_index is a list of exclusions, and that
    indexers should generally exclude 'inc', 'xt' and 't' as well
  - CPAN::Meta::History::Meta_1_0 through 1_4 are added as a permanent
    record of 1.x versions of the metaspec

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.142060-2
- Perl 5.20 rebuild

* Mon Jul 28 2014 Paul Howarth <paul@city-fan.org> - 2.142060-1
- Update to 2.142060
  - Added ability for CPAN::Meta::Converter to convert metadata fragments
    (incomplete portions of a metadata structure)
  - Optimized internal use of JSON for datastructure cloning
  - Removed dependency on List::Util 1.33
  - Clarified language around 'dynamic_config' in the Spec
  - Clarified use of 'file' for the 'provides' field in the Spec
  - CPAN::Meta::Merge is a new class for merging two possibly overlapping
    instances of metadata, which will accept both CPAN::Meta objects and
    (possibly incomplete) hashrefs of metadata
- Use %%license

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.140640-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Mar 26 2014 Paul Howarth <paul@city-fan.org> - 2.140640-1
- Update to 2.140640
  - Improved bad version handling during META conversion
  - When downgrading multiple licenses to version 1.x META formats, if all the
    licenses are open source, the downgraded license will be "open_source", not
    "unknown"
  - Added a 'load_string' method that guesses whether the string is YAML or
    JSON
- Drop obsoletes/provides for old tests sub-package
- Classify buildreqs by usage
- Package upstream's CONTRIBUTING file
- Make %%files list more explicit

* Fri Oct 11 2013 Paul Howarth <paul@city-fan.org> - 2.132830-1
- Update to 2.132830
  - Fixed incorrectly encoded META.yml
  - META validation used to allow a scalar value when a list (i.e. array
    reference) was required for a field; this has been tightened and
    validation will now fail if a scalar value is given
  - Installation on Perls < 5.12 will uninstall older versions installed
    due to being bundled with ExtUtils::MakeMaker
  - Updated Makefile.PL logic to support PERL_NO_HIGHLANDER
  - Dropped ExtUtils::MakeMaker configure_requires dependency to 6.17
  - CPAN::Meta::Prereqs now has a 'merged_requirements' method for combining
    requirements across multiple phases and types
  - Invalid 'meta-spec' is no longer a fatal error: instead, it will usually
    be treated as spec version "1.0" (prior to formalization of the meta-spec
    field); conversion has some heuristics for guessing a version depending on
    other fields if 'meta-spec' is missing or invalid
- Don't need to remove empty directories from the buildroot

* Thu Sep  5 2013 Paul Howarth <paul@city-fan.org> - 2.132140-1
- update to latest upstream version

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.120921-291
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 15 2013 Petr Pisar <ppisar@redhat.com> - 2.120921-290
- Increase release to favour standalone package

* Fri Jul 12 2013 Petr Pisar <ppisar@redhat.com> - 2.120921-6
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.120921-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.120921-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 06 2012 Petr Pisar <ppisar@redhat.com> - 2.120921-3
- Perl 5.16 rebuild

* Fri Jun 01 2012 Petr Pisar <ppisar@redhat.com> - 2.120921-2
- Build-require Data::Dumper for tests

* Mon Apr 02 2012 Iain Arnell <iarnell@gmail.com> 2.120921-1
- update to latest upstream version

* Fri Mar 30 2012 Iain Arnell <iarnell@gmail.com> 2.120900-1
- update to latest upstream version

* Sun Mar 04 2012 Iain Arnell <iarnell@gmail.com> 2.120630-1
- update to latest upstream version

* Wed Feb 22 2012 Iain Arnell <iarnell@gmail.com> 2.120530-1
- update to latest upstream version

* Sat Feb 04 2012 Iain Arnell <iarnell@gmail.com> 2.120351-1
- update to latest upstream version

* Sun Jan 22 2012 Iain Arnell <iarnell@gmail.com> 2.113640-3
- drop tests subpackage; move tests to main package documentation

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.113640-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jan  3 2012 Marcela Mašláňová <mmaslano@redhat.com> 2.113640-1
- update to latest version, which deprecated Version::Requirements

* Fri Sep 23 2011 Iain Arnell <iarnell@gmail.com> 2.112621-1
- update to latest upstream version
- clean up spec for modern rpmbuild

* Sat Aug 27 2011 Iain Arnell <iarnell@gmail.com> 2.112150-1
- update to latest upstream version

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.110930-2
- Perl mass rebuild

* Sun Apr 03 2011 Iain Arnell <iarnell@gmail.com> 2.110930-1
- update to latest upstream version

* Sat Apr 02 2011 Iain Arnell <iarnell@gmail.com> 2.110910-1
- update to latest upstream version

* Sun Mar 06 2011 Iain Arnell <iarnell@gmail.com> 2.110580-1
- update to latest upstream version
- drop BR perl(Storable)

* Sat Feb 26 2011 Iain Arnell <iarnell@gmail.com> 2.110550-1
- update to latest upstream version

* Thu Feb 17 2011 Iain Arnell <iarnell@gmail.com> 2.110440-1
- update to latest upstream
- drop BR perl(autodie)
- drop BR perl(Data::Dumper)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.110350-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Feb 04 2011 Iain Arnell <iarnell@gmail.com> 2.110350-1
- update to latest upstream version

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.102400-2
- 661697 rebuild for fixing problems with vendorach/lib

* Sun Aug 29 2010 Iain Arnell <iarnell@gmail.com> 2.102400-1
- update by Fedora::App::MaintainerTools 0.006
- updating to latest GA CPAN version (2.102400)
- added a new br on perl(Carp) (version 0)
- added a new br on perl(Data::Dumper) (version 0)
- altered br on perl(ExtUtils::MakeMaker) (0 => 6.31)
- added a new br on perl(File::Spec) (version 0)
- added a new br on perl(File::Temp) (version 0.20)
- added a new br on perl(IO::Dir) (version 0)
- added a new br on perl(Scalar::Util) (version 0)
- added a new br on perl(Storable) (version 0)
- added a new br on perl(autodie) (version 0)
- added a new br on perl(version) (version 0.82)

* Thu Aug 05 2010 Iain Arnell <iarnell@gmail.com> 2.102160-1
- update to latest upstream

* Wed Jun 16 2010 Iain Arnell <iarnell@gmail.com> 2.101670-1
- update to latest upstream

* Mon Jun 14 2010 Iain Arnell <iarnell@gmail.com> 2.101610-1
- update to latest upstream

* Tue Jun 01 2010 Iain Arnell <iarnell@gmail.com> 2.101461-2
- rebuild for perl-5.12

* Fri May 28 2010 Iain Arnell <iarnell@gmail.com> 2.101461-1
- Specfile autogenerated by cpanspec 1.78.
- drop explicit requirements
