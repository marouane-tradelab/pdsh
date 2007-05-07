Name: pdsh   
Version: See META
Release: See META

Summary: Parallel remote shell program

License: GPL
Url: http://sourceforge.net/projects/pdsh
Group: System Environment/Base
Source: http://dl.sourceforge.net/sourceforge/pdsh/pdsh-%{version}-1.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: pdsh-rcmd

#
# Enabling and disabling pdsh options
#  defaults:
#  enabled:  readline, rsh, ssh, dshgroup, netgroups
#  disabled: rms, mrsh, qshell, mqshell, xcpu, genders, nodeattr, machines,
#            nodeupdown

#  To build the various module subpackages, pass --with <pkg> on
#   the rpmbuild command line (if your rpm is a recent enough version)
#  
#  Similarly, to disable various pdsh options pass --without <pkg> on
#   the rpmbuild command line.
#
#  This specfile also supports passing the --with and --without through
#   the environment variables PDSH_WITH_OPTIONS and PDSH_WITHOUT_OPTIONS.
#   e.g. PDSH_WITH_OPTIONS="qshell genders" rpmbuild ....
#
%define _without_env ${PDSH_WITHOUT_OPTIONS}
%define _with_env ${PDSH_WITH_OPTIONS} 
%define dstr "%%%%"define
%define check() echo %_%{1}_env|grep -qw %%1 && echo %dstr _%{1}_%%1 --%{1}-%%1
%{expand: %%define pdsh_with() %%((%{check with})||(%{check without}))%%{nil}}
%define def() %%{!?_%{2}_%1: %%{!?_%{3}_%1: %%global _%{2}_%1 --%{2}-%1}}

%{expand: %pdsh_with ssh}
%{expand: %def ssh with without}
%{expand: %pdsh_with rsh}
%{expand: %def rsh with without}
%{expand: %pdsh_with readline}
%{expand: %def readline with without}
%{expand: %pdsh_with dshgroups}
%{expand: %def dshgroups with without}
%{expand: %pdsh_with netgroup}
%{expand: %def netgroup with without}

%{expand: %pdsh_with mrsh}
%{expand: %def mrsh without with}
%{expand: %pdsh_with qshell}
%{expand: %def qshell without with}
%{expand: %pdsh_with mqshell}
%{expand: %def mqshell without with}
%{expand: %pdsh_with xcpu}
%{expand: %def xcpu without with}
%{expand: %pdsh_with genders}
%{expand: %def genders without with}
%{expand: %pdsh_with nodeattr}
%{expand: %def nodeattr without with}
%{expand: %pdsh_with nodeupdown}
%{expand: %def nodeupdown without with}
%{expand: %pdsh_with machines}
%{expand: %def machines without with}
%{expand: %pdsh_with slurm}
%{expand: %def slurm without with}
%{expand: %pdsh_with rms}
%{expand: %def rms without with}
%{expand: %pdsh_with debug}
%{expand: %def debug without with}
%{expand: %pdsh_with pam}
%{expand: %def pam without with}

#
# If "--with debug" is set compile with --enable-debug
#   and try not to strip binaries.
#
# (See /usr/share/doc/rpm-*/conditionalbuilds)
#
%if %{?_with_debug:1}%{!?_with_debug:0}
  %define _enable_debug --enable-debug
%endif


%{?_with_qshell:BuildRequires: qsnetlibs}
%{?_with_mqshell:BuildRequires: qsnetlibs}
%{?_with_readline:BuildRequires: readline-devel}
%{?_with_nodeupdown:BuildRequires: whatsup}
%{?_with_genders:BuildRequires: genders > 1.0}
%{?_with_pam:BuildRequires: pam-devel}

##############################################################################
# Pdsh description

%description
Pdsh is a multithreaded remote shell client which executes commands
on multiple remote hosts in parallel.  Pdsh can use several different
remote shell services, including standard "rsh", Kerberos IV, and ssh.
##############################################################################

%package qshd
Summary: Remote shell daemon for pdsh/qshell/Quadrics QsNet
Group:   System Environment/Base
Requires:  xinetd
%description qshd
Remote shell service for running Quadrics QsNet jobs under pdsh.
Sets up Elan capabilities and environment variables needed by Quadrics
MPICH executables.
##############################################################################

%package mqshd
Summary: Remote shell daemon for pdsh/mqshell/Quadrics QsNet
Group:   System Environment/Base
Requires:  xinetd
%description mqshd
Remote shell service for running Quadrics QsNet jobs under pdsh with
mrsh authentication.  Sets up Elan capabilities and environment variables 
needed by Quadrics MPICH executables.
##############################################################################

#
# Module packages:
#
%package   rcmd-rsh
Summary:   Provides bsd rcmd capability to pdsh
Group:     System Environment/Base
Provides:  pdsh-rcmd
%description rcmd-rsh
Pdsh module for bsd rcmd functionality. Note: This module
requires that the pdsh binary be installed setuid root.

%package   rcmd-ssh
Summary:   Provides ssh rcmd capability to pdsh
Group:     System Environment/Base
Provides:  pdsh-rcmd
%description rcmd-ssh
Pdsh module for ssh rcmd functionality.

%package   rcmd-qshell
Summary:   Provides qshell rcmd capability to pdsh
Group:     System Environment/Base
Provides:  pdsh-rcmd
Conflicts: pdsh-rcmd-mqshell
%description rcmd-qshell
Pdsh module for running QsNet MPI jobs. Note: This module
requires that the pdsh binary be installed setuid root.

%package   rcmd-mrsh
Summary:   Provides mrsh rcmd capability to pdsh
Group:     System Environment/Base
Provides:  pdsh-rcmd
%description rcmd-mrsh
Pdsh module for mrsh rcmd functionality.

%package   rcmd-mqshell
Summary:   Provides mqshell rcmd capability to pdsh
Group:     System Environment/Base
Provides:  pdsh-rcmd
Conflicts: pdsh-rcmd-qshell
%description rcmd-mqshell
Pdsh module for mqshell rcmd functionality.

%package   rcmd-xcpu
Summary:   Provides xcpu rcmd capability to pdsh
Group:     System Environment/Base
Provides:  pdsh-xcpu
%description rcmd-xcpu
Pdsh module for xcpu rcmd functionality.

%package   mod-genders
Summary:   Provides libgenders support for pdsh
Group:     System Environment/Base
Requires:  genders >= 1.1
Conflicts: pdsh-mod-nodeattr
Conflicts: pdsh-mod-machines
%description mod-genders
Pdsh module for libgenders functionality.

%package   mod-nodeattr
Summary:   Provides genders support for pdsh using the nodeattr program
Group:     System Environment/Base
Requires:  genders 
Conflicts: pdsh-mod-genders
Conflicts: pdsh-mod-machines
%description mod-nodeattr
Pdsh module for genders functionality using the nodeattr program.

%package   mod-nodeupdown
Summary:   Provides libnodeupdown support for pdsh
Group:     System Environment/Base
Requires:  whatsup
%description mod-nodeupdown
Pdsh module providing -v functionality using libnodeupdown.

%package   mod-rms
Summary:   Provides RMS support for pdsh
Group:     System Environment/Base
Requires:  qsrmslibs
%description mod-rms
Pdsh module providing support for gathering the list of target nodes
from an allocated RMS resource.

%package   mod-machines
Summary:   Pdsh module for gathering list of target nodes from a machines file
Group:     System Environment/Base
%description mod-machines
Pdsh module for gathering list of all target nodes from a machines file.

%package   mod-dshgroup
Summary:   Provides dsh-style group file support for pdsh
Group:     System Environment/Base
%description mod-dshgroup
Pdsh module providing dsh (Dancer's shell) style "group" file support.
Provides -g groupname and -X groupname options to pdsh.

%package   mod-netgroup
Summary:   Provides netgroup support for pdsh
Group:     System Environment/Base
%description mod-netgroup
Pdsh module providing support for targeting hosts based on netgroup.
Provides -g groupname and -X groupname options to pdsh.

%package   mod-slurm
Summary:   Provides support for running pdsh under SLURM allocations
Group:     System Environment/Base
Requires:  slurm
%description mod-slurm
Pdsh module providing support for gathering the list of target nodes
from an allocated SLURM job.



##############################################################################

%prep
%setup
##############################################################################

%build
%configure --program-prefix=%{?_program_prefix:%{_program_prefix}} \
    %{?_enable_debug}       \
    %{?_with_pam}           \
    %{?_without_pam}        \
    %{?_with_rsh}           \
    %{?_without_rsh}        \
    %{?_with_ssh}           \
    %{?_without_ssh}        \
    %{?_with_qshell}        \
    %{?_without_qshell}     \
    %{?_with_readline}      \
    %{?_without_readline}   \
    %{?_with_machines}      \
    %{?_without_machines}   \
    %{?_with_genders}       \
    %{?_without_genders}    \
    %{?_with_rms}           \
    %{?_without_rms}        \
    %{?_with_nodeupdown}    \
    %{?_without_nodeupdown} \
    %{?_with_nodeattr}      \
    %{?_without_nodeattr}   \
    %{?_with_mrsh}          \
    %{?_without_mrsh}       \
    %{?_with_mqshell}       \
    %{?_without_mqshell}    \
    %{?_with_xcpu}       \
    %{?_without_xcpu}    \
    %{?_with_slurm}         \
    %{?_without_slurm}      \
    %{?_with_dshgroups}     \
    %{?_without_dshgroups}  \
    %{?_with_netgroup}      \
    %{?_without_netgroup} 
    
           
# FIXME: build fails when trying to build with _smp_mflags if qsnet is enabled
# make %{_smp_mflags} CFLAGS="$RPM_OPT_FLAGS"
make CFLAGS="$RPM_OPT_FLAGS"
##############################################################################

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT
DESTDIR="$RPM_BUILD_ROOT" make install
if [ -x $RPM_BUILD_ROOT/%{_sbindir}/in.qshd ]; then
   install -D -m644 etc/qshell.xinetd $RPM_BUILD_ROOT/%{_sysconfdir}/xinetd.d/qshell
fi
if [ -x $RPM_BUILD_ROOT/%{_sbindir}/in.mqshd ]; then
   install -D -m644 etc/mqshell.xinetd $RPM_BUILD_ROOT/%{_sysconfdir}/xinetd.d/mqshell
fi

# 
# Remove all module .a's as they are not needed on any known RPM platform.
rm $RPM_BUILD_ROOT/%{_libdir}/pdsh/*.a 
rm $RPM_BUILD_ROOT/%{_libdir}/pdsh/*.la

##############################################################################

%clean
rm -rf "$RPM_BUILD_ROOT"
##############################################################################

%files
%defattr(-,root,root)
%doc COPYING README ChangeLog NEWS DISCLAIMER 
%doc README.KRB4 README.modules README.QsNet
%{_bindir}/pdsh
%{_bindir}/pdcp
%{_bindir}/rpdcp
%{_bindir}/dshbak
%{_mandir}/man1/*
##############################################################################

%if %{?_with_rsh:1}%{!?_with_rsh:0}
%files rcmd-rsh
%defattr(-,root,root)
%{_libdir}/pdsh/xrcmd.*
%endif
##############################################################################

%if %{?_with_ssh:1}%{!?_with_ssh:0}
%files rcmd-ssh
%defattr(-,root,root)
%{_libdir}/pdsh/sshcmd.*
%endif
##############################################################################

%if %{?_with_qshell:1}%{!?_with_qshell:0}
%files rcmd-qshell
%defattr(-,root,root)
%{_libdir}/pdsh/qcmd.*
%endif
##############################################################################

%if %{?_with_mrsh:1}%{!?_with_mrsh:0}
%files rcmd-mrsh
%defattr(-,root,root)
%{_libdir}/pdsh/mcmd.*
%endif
##############################################################################

%if %{?_with_mqshell:1}%{!?_with_mqshell:0}
%files rcmd-mqshell
%defattr(-,root,root)
%{_libdir}/pdsh/mqcmd.*
%endif
##############################################################################

%if %{?_with_xcpu:1}%{!?_with_xcpu:0}
%files rcmd-xcpu
%defattr(-,root,root)
%{_libdir}/pdsh/xcpucmd.*
%endif
##############################################################################

%if %{?_with_genders:1}%{!?_with_genders:0}
%files mod-genders
%defattr(-,root,root)
%{_libdir}/pdsh/genders.*
%endif
##############################################################################

%if %{?_with_nodeattr:1}%{!?_with_nodeattr:0}
%files mod-nodeattr
%defattr(-,root,root)
%{_libdir}/pdsh/nodeattr.*
%endif
##############################################################################

%if %{?_with_nodeupdown:1}%{!?_with_nodeupdown:0}
%files mod-nodeupdown
%defattr(-,root,root)
%{_libdir}/pdsh/nodeupdown.*
%endif
##############################################################################

%if %{?_with_rms:1}%{!?_with_rms:0}
%files mod-rms
%defattr(-,root,root)
%{_libdir}/pdsh/rms.*
%endif
##############################################################################

%if %{?_with_machines:1}%{!?_with_machines:0}
%files mod-machines
%defattr(-,root,root)
%{_libdir}/pdsh/machines.*
%endif
##############################################################################

%if %{?_with_dshgroups:1}%{!?_with_dshgroups:0}
%files mod-dshgroup
%defattr(-,root,root)
%{_libdir}/pdsh/dshgroup.*
%endif
##############################################################################

%if %{?_with_netgroup:1}%{!?_with_netgroup:0}
%files mod-netgroup
%defattr(-,root,root)
%{_libdir}/pdsh/netgroup.*
%endif
##############################################################################

%if %{?_with_slurm:1}%{!?_with_slurm:0}
%files mod-slurm
%defattr(-,root,root)
%{_libdir}/pdsh/slurm.*
%endif
##############################################################################

%if %{?_with_qshell:1}%{!?_with_qshell:0}
%files qshd
%defattr(-,root,root)
%{_sbindir}/in.qshd
%{_sysconfdir}/xinetd.d/qshell

%post qshd
if ! grep "^qshell" /etc/services >/dev/null; then
  echo "qshell            523/tcp                  # pdsh/qshell/Quadrics QsNet" >>/etc/services
fi
%{_initrddir}/xinetd reload

%endif
##############################################################################

%if %{?_with_mqshell:1}%{!?_with_mqshell:0}
%files mqshd
%defattr(-,root,root)
%{_sbindir}/in.mqshd
%{_sysconfdir}/xinetd.d/mqshell

%post mqshd
if ! grep "^mqshell" /etc/services >/dev/null; then
  echo "mqshell         21234/tcp                  # pdsh/mqshell/Quadrics QsNet" >>/etc/services
fi
%{_initrddir}/xinetd reload

%endif
##############################################################################

%changelog
* Thu Feb 22 2007 Daniel J Blueman <daniel@quadrics.com>
- added 'rpmbuild ... --without pam' option passthrough
- generalised 'elan3' to 'Quadrics QsNet'

* Thu Dec  7 2006 Mark Grondona <mgrondona@llnl.gov>
- Package new rpdcp command.

* Fri Feb 23 2006 Ben Woodard <woodard@redhat.com> 
- changed source location to point to main site not mirror.

* Thu Feb 22 2006 Ben Woodard <woodard@redhat.com>
- removed change of attributes of pdsh and pcp in files section
- removed .a files from packages.

* Wed Feb 22 2006 Ben Woodard <woodard@redhat.com> 
- add parameters to make
- replace etc with _sysconfdir in most places
- remove post section with unexplained removing of cached man pages.
- removed dots at end of all summaries.

* Wed Feb 16 2006 Ben Woodard <woodard@redhat.com
- removed dot at end of summary
- removed unused/broken smp build
- changed to using initrddir macro
- changed depricated Prereq to Requires

* Thu Feb 9 2006 Ben Woodard <woodard@redhat.com> 
- add in rpmlint fixes
- change buildroot

* Wed Feb 1 2006 Ben Woodard <woodard@redhat.com> 
- Modified spec file to fix some problems uncovered by rpmlint
