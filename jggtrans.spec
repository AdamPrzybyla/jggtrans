# $Revision: 1.69 $, $Date: 2007-12-12 08:22:08 $
#
# Conditional build:
%bcond_with	internal_libgadu	# Build with transport's internal libgadu
#
Summary:	GaduGadu transport module for Jabber
Summary(pl.UTF-8):	Moduł transportowy GaduGadu dla systemu Jabber
Name:		jggtrans
Version:	2.2.4
Release:	2
License:	GPL
Group:		Applications/Communications
Source0:	http://jggtrans.jajcus.net/downloads/jggtrans-%{version}.tar.gz
# Source0-md5:	70bbec4e9c438cda6b7379ccfc63492f
Source1:	jggtrans.init
Source2:	jggtrans.sysconfig
Patch0:		%{name}-pidfile.patch
Patch1:		%{name}-spooldir.patch
#Patch2:		%{name}-external.patch
URL:		http://jggtrans.jajcus.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bind-libbind-devel
BuildRequires:	expat-devel >= 1.95.1
BuildRequires:	gettext-devel >= 0.14.1
BuildRequires:	glib2-devel >= 2.0.0
%{!?with_internal_libgadu:BuildRequires:	libgadu-devel}
BuildRequires:	libidn-devel >= 0.3.0
BuildRequires:	libtool
BuildRequires:	pkgconfig
Requires(post):	sed >= 4.0
Requires(post,preun):	/sbin/chkconfig
#Requires(pre):	jabber-common
#Requires:	jabber-common
Obsoletes:	jabber-gg-transport
#BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
BuildRoot:	%{_tmppath}/%{name}-%{version}-root-%(id -u -n)

%description
This module allows Jabber to communicate with GaduGadu server with GG8 support.

%description -l pl.UTF-8
Moduł ten umożliwia użytkownikom Jabbera komunikowanie się z
użytkownikami GaduGadu. Zgodny z GG8.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
#%{!?with_internal_libgadu:%patch2 -p1}

%build
#%{__gettextize}
#%{__aclocal}
#%{__autoconf}
#%{__automake}
./autogen.sh
%configure \
	%{?debug:--with-efence} \
	--without-bind \
	--sysconfdir=%{_sysconfdir}/jabber
%{__make} cl-stamp
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/jabber,/etc/rc.d/init.d,/etc/sysconfig,/var/lib/jggtrans}

%{__make} install \
	DESTDIR="$RPM_BUILD_ROOT"

install jggtrans.xml $RPM_BUILD_ROOT%{_sysconfdir}/jabber
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/jggtrans
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/jggtrans

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f %{_sysconfdir}/jabber/secret ] ; then
	SECRET=`cat %{_sysconfdir}/jabber/secret`
	if [ -n "$SECRET" ] ; then
		echo "Updating component authentication secret in jggtrans.xml..."
		%{__sed} -i -e "s/>secret</>$SECRET</" /etc/jabber/jggtrans.xml
	fi
fi
/sbin/chkconfig --add jggtrans
if [ -r /var/lock/subsys/jggtrans ]; then
	/etc/rc.d/init.d/jggtrans restart >&2
#else
#	echo "Run \"/etc/rc.d/init.d/jggtrans start\" to start Jabber GaduGadu transport."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -r /var/lock/subsys/jggtrans ]; then
		/etc/rc.d/init.d/jggtrans stop >&2
	fi
	/sbin/chkconfig --del jggtrans
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README README.Pl jggtrans.xml.Pl
%attr(755,root,root) %{_sbindir}/*
%attr(640,root,ejabberd) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/jabber/jggtrans.xml
%attr(754,root,root) /etc/rc.d/init.d/jggtrans
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/jggtrans
%attr(770,root,ejabberd) /var/lib/jggtrans

%define date	%(echo `LC_ALL="C" date +"%a %b %d %Y"`)
#git-log |grep -v ^commit|sed 's/ *-/-/g'|sed 's/^  */- /g'| awk '/Author/ {a=$0;gsub("Author:","",a);next} /Date/ {d=$2" "$3" "$4" "$6; gsub("-.*","",d);print "\n* "d,a;next} /^-/ {print} '|sed 1d |grep -v '^- $' >>../SPECS/jggtrans.spec
%changelog
* Fri Aug 12 2011  Jacek Konieczny <jajcus@jajcus.net>
- Merge pull request #25 from rozwell/missing
- Add missing "do not disturb" param

* Thu Aug 11 2011  rozwell <rozwell@lapik.(none)>
- Added missing "do not disturb" param

* Fri May 6 2011  Jacek Konieczny <jajcus@jajcus.net>
- Auto-updates to the *.po files

* Fri May 6 2011  Jacek Konieczny <jajcus@jajcus.net>
- svn magic replaced with git magic
- Use 'git log' to generate changelog, user '+git' instead of '+svn'
- for unofficial builds.

* Fri May 6 2011  Jacek Konieczny <jajcus@jajcus.net>
- .gitignore files added

* Fri Mar 18 2011  Jacek Konieczny <jajcus@jajcus.net>
- status code handling fix by  Mateusz Jakub Kwapich

* Wed Feb 9 2011  Jacek Konieczny <jajcus@jajcus.net>
- send all messages as chat (some GG clients send non-chat messages in a chat context)

* Tue Aug 17 2010  Jacek Konieczny <jajcus@jajcus.net>
- patch for 'unavailable with description' status on x86_64, by Manio

* Wed Apr 14 2010  Jacek Konieczny <jajcus@jajcus.net>
- Do not send <presence type='unsubscibed'/> as a reply to a probe from a
- known, but not yet logged-in user. fixes #22

* Sat Apr 10 2010  Jacek Konieczny <jajcus@jajcus.net>
- *** Version: 2.2.4 ***

* Wed Apr 7 2010  Jacek Konieczny <jajcus@jajcus.net>
- option to ignore system messages

* Mon Apr 5 2010  Jacek Konieczny <jajcus@jajcus.net>
- translations update

* Mon Apr 5 2010  Jacek Konieczny <jajcus@jajcus.net>
- merged change from xiaoka: r73 'Fixed presence time stamping. Fixes #1'

* Mon Apr 5 2010  Jacek Konieczny <jajcus@jajcus.net>
- merged change from xiaoka: r68 'Fixed presence-probe handling according to RFC 3921bis 4.3.2. Server Processing '

* Mon Apr 5 2010  Jacek Konieczny <jajcus@jajcus.net>
- merged change from xiaoka: r59 'fixed g_error() abort on stream reading error'

* Mon Apr 5 2010  Jacek Konieczny <jajcus@jajcus.net>
- merged change from xiaoka: r51 'fixed setting text status during connection'

* Mon Apr 5 2010  Jacek Konieczny <jajcus@jajcus.net>
- changeset 705 reverted

* Mon Apr 5 2010  Jacek Konieczny <jajcus@jajcus.net>
- merged change from xiaoka: r29 'canged description to more verbose'

* Mon Apr 5 2010  Jacek Konieczny <jajcus@jajcus.net>
- merged change from xiaoka: r21 'gg subscription computation fix'

* Mon Apr 5 2010  Jacek Konieczny <jajcus@jajcus.net>
- merged change from xiaoka: r20 'friends_only support on disconnection'

* Mon Apr 5 2010  Jacek Konieczny <jajcus@jajcus.net>
- use UTF8 for GG strings

* Mon Apr 5 2010  Jacek Konieczny <jajcus@jajcus.net>
- Polish descriptions for the new statuses

* Mon Apr 5 2010  Jacek Konieczny <jajcus@jajcus.net>
- 'dnd' (GG_STATUS_DND) and 'chat' (GG_STATUS_FFC) support

* Mon Apr 5 2010  Jacek Konieczny <jajcus@jajcus.net>
- require external libgadu-1.9.0 instead of bundled old version (pthread problem should be fixed by now adn libgadu-1.9 brings GG10 compatibility)

* Sun Oct 26 2008  Jacek Konieczny <jajcus@jajcus.net>
- remove old timers on re-login (thx smoku)

* Tue Oct 21 2008  Jacek Konieczny <jajcus@jajcus.net>
- autoupdated

* Tue Oct 21 2008  Jacek Konieczny <jajcus@jajcus.net>
- properly load u->subscribe

* Mon Sep 1 2008  Jacek Konieczny <jajcus@jajcus.net>
- always send contact list to GG server, even if empty (thanks to Łukasz Siudut)

* Fri Nov 16 2007  Jacek Konieczny <jajcus@jajcus.net>
- more GG versions recognized (thanks to arghil)

* Fri Jun 29 2007  Jacek Konieczny <jajcus@jajcus.net>
- buffer overflow bug fixed, thanks Michal

* Sun Oct 22 2006  Jacek Konieczny <jajcus@jajcus.net>
- forbidden (not defined in vcard-temp) jabber:iq:register fields 'gender' and 'born' removed

* Sun Oct 22 2006  Jacek Konieczny <jajcus@jajcus.net>
- when user is already registered return the information in the reply to a registration form

* Sun Oct 22 2006  Jacek Konieczny <jajcus@jajcus.net>
- long message splitting hopefully fixed (previous version of the function just could not work)

* Wed Jul 19 2006  Jacek Konieczny <jajcus@jajcus.net>
- Another patch by Zbyszek Żółkiewski (kolargol):
- new default server IP address
- log more GG numbers

* Wed Jul 19 2006  Jacek Konieczny <jajcus@jajcus.net>
- not needed any more

* Tue Jul 18 2006  Jacek Konieczny <jajcus@jajcus.net>
- new GG server IP addresses

* Wed Jun 21 2006  Jacek Konieczny <jajcus@jajcus.net>
- hopefully fixed problem with the second login to GG

* Thu Jun 8 2006  Jacek Konieczny <jajcus@jajcus.net>
- include timestamps in the debuging messages, log level cleanup (fixes #3) [jaak]

* Fri Jun 2 2006  Jacek Konieczny <jajcus@jajcus.net>
- project name is: jggtrans

* Fri Jun 2 2006  Jacek Konieczny <jajcus@jajcus.net>
- updated

* Fri Jun 2 2006  Jacek Konieczny <jajcus@jajcus.net>
- autoupdated

* Fri Jun 2 2006  Jacek Konieczny <jajcus@jajcus.net>
- *** Version: 2.2.2 ***

* Fri Jun 2 2006  Jacek Konieczny <jajcus@jajcus.net>
- dates in the copyright header updated

* Fri Jun 2 2006  Jacek Konieczny <jajcus@jajcus.net>
- changed in version 2.2.2

* Fri Jun 2 2006  Jacek Konieczny <jajcus@jajcus.net>
- tested versions of required libraries updated

* Fri Jun 2 2006  Jacek Konieczny <jajcus@jajcus.net>
- svn:ignore libgadu/configure

* Fri Jun 2 2006  Jacek Konieczny <jajcus@jajcus.net>
- addresses updated after moving to the new site

* Tue May 30 2006  Jacek Konieczny <jajcus@jajcus.net>
- not needed here (in the new repository)

* Mon May 29 2006  Jacek Konieczny <jajcus@jajcus.net>
- an important notice about repository being moved

* Sun Apr 9 2006  Jacek Konieczny <jajcus@jajcus.net>
- log UIN together with JID on login success/failure. Patch by Zbyszek Żółkiewski (kolargol)

* Sat Apr 8 2006  Jacek Konieczny <jajcus@jajcus.net>
- better <servers/> example

* Sat Apr 8 2006  Jacek Konieczny <jajcus@jajcus.net>
- do not use '/registered' resource by default, but still do it in old configurations

* Sat Apr 8 2006  Jacek Konieczny <jajcus@jajcus.net>
- auto-update

* Sat Apr 8 2006  Jacek Konieczny <jajcus@jajcus.net>
- auto-generated configure removed from repo

* Thu Dec 29 2005  Jacek Konieczny <jajcus@jajcus.net>
- reverted last change

* Thu Dec 29 2005  Jacek Konieczny <jajcus@jajcus.net>
- comment about using presence information instead of subscription state when setting user visibility for GG contacts

* Thu Dec 29 2005  Jacek Konieczny <jajcus@jajcus.net>
- trigger presence_send_subscribe() on every successfully processed registration/configuration request. It is safe and may be easier to use than unsubcribed/subscribe on some clients.

* Thu Dec 29 2005  Jacek Konieczny <jajcus@jajcus.net>
- fix of use of uninitialized variables

* Thu Dec 29 2005  Jacek Konieczny <jajcus@jajcus.net>
- keep track of user subscription to transport, so <presence type='subscribe'/> may be issued without a risk of any loop
- more XMPP-like of contact subscription (do not send <presence type='subscribe'/> if contact has already subscribed user
- fixed parsing of <version file_format='xxxx'/> in config file
- file_format: 02020101

* Thu Dec 15 2005  Tomasz Sterna <tomek@xiaoka.com>
- sending fixed status in info using utf-8 bugfix

* Tue Dec 13 2005  Tomasz Sterna <tomek@xiaoka.com>
- big statuses update
- removed invisible status description
- femoved status_offline description
- descriptions are copied from jabber status
- or can be fixed permanently
- invisible and offline status with description implemented

* Mon Dec 12 2005  Tomasz Sterna <tomek@xiaoka.com>
- saving status message in user.xml file

* Mon Dec 12 2005  Tomasz Sterna <tomek@xiaoka.com>
- connect as invisible, change status after connection

* Mon Dec 12 2005  Tomasz Sterna <tomek@xiaoka.com>
- 'status not changed' detection fix

* Mon Dec 12 2005  Tomasz Sterna <tomek@xiaoka.com>
- update gg status even when disconnected

* Mon Dec 12 2005  Tomasz Sterna <tomek@xiaoka.com>
- send disconnection jabber status before gg logoff

* Mon Dec 12 2005  Tomasz Sterna <tomek@xiaoka.com>
- datatype cosmetics

* Mon Dec 12 2005  Tomasz Sterna <tomek@xiaoka.com>
- replaced fixed 70 status characters length with GG_STATUS_DESCR_MAXSIZE

* Mon Dec 12 2005  Tomasz Sterna <tomek@xiaoka.com>
- normalize resource concat fix

* Mon Dec 12 2005  Tomasz Sterna <tomek@xiaoka.com>
- new GG client version mappings

* Wed Oct 12 2005  Jacek Konieczny <jajcus@jajcus.net>
- ACL fix (rules with no 'what' attribute were ignored)

* Sun Jul 31 2005  Jacek Konieczny <jajcus@jajcus.net>
- *** Version: 2.2.1 ***

* Sun Jul 31 2005  Jacek Konieczny <jajcus@jajcus.net>
- autoupdated

* Tue Jul 26 2005  Jacek Konieczny <jajcus@jajcus.net>
- '+svn' version marker

* Tue Jul 26 2005  Jacek Konieczny <jajcus@jajcus.net>
- disabled--show-reachable=yes option for valgrind

* Tue Jul 26 2005  Jacek Konieczny <jajcus@jajcus.net>
- user file format version marker
- workaround for buggy user files (wrong subscription) created by jggtrans 2.2.0
- fixed handling od pretty-formated XML files

* Tue Jul 26 2005  Jacek Konieczny <jajcus@jajcus.net>
- don't break contact subscription on <presence type='probe'/>! (why the hell this crap was here?)

* Mon Jul 25 2005  Jacek Konieczny <jajcus@jajcus.net>
- registration/unregistration fixes

* Mon Jul 25 2005  Jacek Konieczny <jajcus@jajcus.net>
- send <presence type='subscribe'/> on sucessull registration

* Mon Jul 25 2005  Jacek Konieczny <jajcus@jajcus.net>
- call the 'garbage collector' on each user_delete() (makes unregistration work) and every minute (will probably save some memory)

* Mon Jul 25 2005  Jacek Konieczny <jajcus@jajcus.net>
- define g_debug() macro if it is not defined by glib

* Sun Jul 24 2005  Jacek Konieczny <jajcus@jajcus.net>
- removed references to removed files

* Sun Jul 24 2005  Jacek Konieczny <jajcus@jajcus.net>
- *** Version: 2.2.0 ***

* Sun Jul 24 2005  Jacek Konieczny <jajcus@jajcus.net>
- copyright years and my email updated

* Sun Jul 24 2005  Jacek Konieczny <jajcus@jajcus.net>
- missing comma in a debug message

* Sun Jul 24 2005  Jacek Konieczny <jajcus@jajcus.net>
- updated

* Sun Jul 24 2005  Jacek Konieczny <jajcus@jajcus.net>
- translations updated (nl translation auto-updated only)

* Sun Jul 24 2005  Jacek Konieczny <jajcus@jajcus.net>
- emails updated and mangled

* Sun Jul 24 2005  Jacek Konieczny <jajcus@jajcus.net>
- copyright info updated in header (year and e-mail)

* Sun Jul 24 2005  Jacek Konieczny <jajcus@jajcus.net>
- copyright info updated in header (year and e-mail)

* Sun Jul 24 2005  Jacek Konieczny <jajcus@jajcus.net>
- more ignores

* Sun Jul 24 2005  Jacek Konieczny <jajcus@jajcus.net>
- fixed memory leaks in the conversation with transport code

* Sun Jul 24 2005  Jacek Konieczny <jajcus@jajcus.net>
- fixed sending unavailable presence on exit

* Sun Jul 24 2005  Jacek Konieczny <jajcus@jajcus.net>
- 'Saving user ...' is now a debug message-- it was displayed too often

* Sun Jul 24 2005  Jacek Konieczny <jajcus@jajcus.net>
- do not subtract 1 from server number shown in timeout message

* Sat Jul 23 2005  Jacek Konieczny <jajcus@jajcus.net>
- autogenerated

* Sat Jul 23 2005  Jacek Konieczny <jajcus@jajcus.net>
- autogenerated

* Sat Jul 23 2005  Jacek Konieczny <jajcus@jajcus.net>
- autogenerated

* Sat Jul 23 2005  Jacek Konieczny <jajcus@jajcus.net>
- continued search results removed as not compatible with XMPP

* Sat Jul 23 2005  Jacek Konieczny <jajcus@jajcus.net>
- all the password-change related stuff commented-out

* Sat Jul 23 2005  Jacek Konieczny <jajcus@jajcus.net>
- free version query node after use

* Sat Jul 23 2005  Jacek Konieczny <jajcus@jajcus.net>
- do not access contact possibly removed by user_check_contact()

* Sat Jul 23 2005  Jacek Konieczny <jajcus@jajcus.net>
- User reference counting
- send available presence on successfull connect

* Sat Jul 23 2005  Jacek Konieczny <jajcus@jajcus.net>
- user reference counting (simple garbage collection, currently on exit only)

* Sat Jul 23 2005  Jacek Konieczny <jajcus@jajcus.net>
- use the right timestamp

* Sat Jul 23 2005  Jacek Konieczny <jajcus@jajcus.net>
- memory leak fix

* Sat Jul 23 2005  Jacek Konieczny <jajcus@jajcus.net>
- another use of uninitialized variable fixed

* Sat Jul 23 2005  Jacek Konieczny <jajcus@jajcus.net>
- memory leak fix

* Sat Jul 23 2005  Jacek Konieczny <jajcus@jajcus.net>
- use of uninitialized variable (invisible_status) fixed

* Sat Jul 23 2005  Jacek Konieczny <jajcus@jajcus.net>
- support for HTTP requests removed-- the only request implemented was password change and it is not supported anymore (as GG uses graphical tokens now)

* Sat Jul 23 2005  Jacek Konieczny <jajcus@jajcus.net>
- support for HTTP requests removed-- the only request implemented was password change and it is not supported anymore (as GG uses graphical tokens now)

* Sat Jul 23 2005  Jacek Konieczny <jajcus@jajcus.net>
- password change is not available any more

* Sat Jul 23 2005  Jacek Konieczny <jajcus@jajcus.net>
- Use GSource and GPollFD instad of higher level GIOChannel as the socket is handled (eg. closed or replaced) by libgadu

* Sat Jul 23 2005  Jacek Konieczny <jajcus@jajcus.net>
- use g_io_channel_shutdown instead of obsolete g_io_channel_close

* Fri Jul 22 2005  Jacek Konieczny <jajcus@jajcus.net>
- do not try to close session iochannel twice

* Fri Jul 22 2005  Jacek Konieczny <jajcus@jajcus.net>
- do not pass NULL argument to debug() (use empty string instead)

* Fri Jul 22 2005  Jacek Konieczny <jajcus@jajcus.net>
- s/AM_CONFIG_HEADERS/AM_CONFIG_HEADER/

* Fri Jul 22 2005  Jacek Konieczny <jajcus@jajcus.net>
- s/AC_CONFIG_HEADERS/AM_CONFIG_HEADERS/

* Fri Jul 22 2005  Jacek Konieczny <jajcus@jajcus.net>
- expat.m4 added, as it is missing in many systems

* Fri Jul 22 2005  Jacek Konieczny <jajcus@jajcus.net>
- do not use libgadu/make.inc (that was ugly hack that didn't work as it should)

* Fri Jul 22 2005  Jacek Konieczny <jajcus@jajcus.net>
- translation files autoupdate

* Fri Jul 22 2005  Jacek Konieczny <jajcus@jajcus.net>
- build files cleanup

* Fri Jul 22 2005  Jacek Konieczny <jajcus@jajcus.net>
- updated to libgadu-1.6rc3

* Fri Jul 22 2005  Jacek Konieczny <jajcus@jajcus.net>
- libgadu is now included in the transport sources, so not required any more

* Wed Feb 23 2005  Jacek Konieczny <jajcus@jajcus.net>
- per-user presence control: working one-way subscriptions, directed presence and privacy-lists
- ignore list
- customizable status messages for available, unavailable and invisible modes

* Wed Feb 23 2005  Jacek Konieczny <jajcus@jajcus.net>
- unnecessary XMPP stream output buffering dropped-- that caused too much problems and probably no benefit

* Wed Feb 23 2005  Jacek Konieczny <jajcus@jajcus.net>
- updated to use the included libgadu

* Wed Feb 23 2005  Jacek Konieczny <jajcus@jajcus.net>
- now libgadu is included in the jggtrans source tree, so we don't depend on strange and not-working-well-with-jggtrans libgadu builds in distributions.

* Thu Nov 11 2004  Jacek Konieczny <jajcus@jajcus.net>
- fail if Expat is not available

* Thu Nov 11 2004  Jacek Konieczny <jajcus@jajcus.net>
- not needed any more

* Thu Nov 11 2004  Jacek Konieczny <jajcus@jajcus.net>
- updated

* Thu Nov 11 2004  Jacek Konieczny <jajcus@jajcus.net>
- s/stdint.h/inttypes.h/ (portability fixes)

* Fri Nov 5 2004  Tomasz Sterna <tomek@xiaoka.com>
- new password change method fix

* Sun Oct 31 2004  Jacek Konieczny <jajcus@jajcus.net>
- '+svn' version flag is back after the release

* Sun Oct 31 2004  Jacek Konieczny <jajcus@jajcus.net>
- forgotten information about external expat usage

* Sun Oct 31 2004  Jacek Konieczny <jajcus@jajcus.net>
- *** Version: 2.1.0 ***

* Sun Oct 31 2004  Jacek Konieczny <jajcus@jajcus.net>
- updates for 2.1.0 release

* Sun Oct 31 2004  Jacek Konieczny <jajcus@jajcus.net>
- note about jabberd2 configuration

* Sun Oct 31 2004  Jacek Konieczny <jajcus@jajcus.net>
- better format of ChangeLog entries

* Sun Oct 31 2004  Jacek Konieczny <jajcus@jajcus.net>
- convert unknown characters to '?' or the Unicode replacement character (fixes bug #4378)

* Sun Oct 31 2004  Jacek Konieczny <jajcus@jajcus.net>
- apply 'invisible' and 'friends only' settings when registration form submission is processes

* Sun Oct 31 2004  Jacek Konieczny <jajcus@jajcus.net>
- error message when trying 'make dist' when '+svn' version flag is set

* Sun Oct 31 2004  Jacek Konieczny <jajcus@jajcus.net>
- SVN version flag

* Sun Oct 31 2004  Jacek Konieczny <jajcus@jajcus.net>
- use the 'new' version of AM_INIT_AUTOMAKE and specify package version only once (in AC_INIT)

* Sun Oct 31 2004  Jacek Konieczny <jajcus@jajcus.net>
- updated

* Sat Oct 30 2004  Jacek Konieczny <jajcus@jajcus.net>
- another attempt to make good 'ChangeLog' make target

* Sat Oct 30 2004  Jacek Konieczny <jajcus@jajcus.net>
- m4/*m4 files added to EXTRA_DIST
- ChangeLog depending on .svn/entries was a bad idea

* Sat Oct 30 2004  Jacek Konieczny <jajcus@jajcus.net>
- cosmetics

* Sat Oct 30 2004  Jacek Konieczny <jajcus@jajcus.net>
- EXTRA_DIST for old expat files removed

* Sat Oct 30 2004  Jacek Konieczny <jajcus@jajcus.net>
- disable TLS by default (doesn't work well)

* Sat Oct 30 2004  Jacek Konieczny <jajcus@jajcus.net>
- updated for JEP-30 and Jabber Registar disco categories/types registry compliance

* Sat Oct 30 2004  Jacek Konieczny <jajcus@jajcus.net>
- translation updated

* Sat Oct 30 2004  Jacek Konieczny <jajcus@jajcus.net>
- svn2log.py included in sources and ChangeLog made dependent on .svn/entries

* Sat Oct 30 2004  Jacek Konieczny <jajcus@jajcus.net>
- executable flag set

* Sat Oct 30 2004  Jacek Konieczny <jajcus@jajcus.net>
- use external expat (the one previously included in the sources was buggy)

* Fri Oct 29 2004  Jacek Konieczny <jajcus@jajcus.net>
- m4/Makefile.am seems not being created by autogen.sh and not needed. References removed.

* Fri Oct 29 2004  Jacek Konieczny <jajcus@jajcus.net>
- proper use of autopoint
- abort autogen.sh on any error

* Fri Oct 29 2004  Jacek Konieczny <jajcus@jajcus.net>
- do not call 'gettextize' here. autopoint does what we need

* Thu Oct 28 2004  Jacek Konieczny <jajcus@jajcus.net>
- use--no-changelog for gettextize

* Thu Oct 28 2004  Jacek Konieczny <jajcus@jajcus.net>
- 'ChangeLog' and 'cosmetics' make targets
- auto* tools update

* Thu Oct 28 2004  Jacek Konieczny <jajcus@jajcus.net>
- 'executable' flag set

* Thu Oct 28 2004  Jacek Konieczny <jajcus@jajcus.net>
- 'executable' flag set

* Thu Oct 28 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog removed from the repo. It will be automatically regenerated in the working directory when needed.

* Thu Oct 28 2004  Jacek Konieczny <jajcus@jajcus.net>
- .cvsingore files are not needed in SVN

* Thu Oct 28 2004  Jacek Konieczny <jajcus@jajcus.net>
- auxiliary scripts moved to 'aux' dir

* Wed Oct 27 2004  Jacek Konieczny <jajcus@jajcus.net>
- send GG roster in 'normal' message, not 'chat' (fixes the roster retrieval problem with Psi)

* Sat Sep 18 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Sat Sep 18 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Wed Jun 16 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Wed Jun 16 2004  Jacek Konieczny <jajcus@jajcus.net>
- reports for the CIA ( http://cia.navi.cx )

* Fri Jun 11 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Fri Jun 11 2004  Tomasz Sterna <tomek@xiaoka.com>
- protocol 0x22 added

* Fri Jun 11 2004  Tomasz Sterna <tomek@xiaoka.com>
- conference disabling cleanup

* Fri Jun 11 2004  Tomasz Sterna <tomek@xiaoka.com>
- disabled GG conference messages- it's not supported yet

* Wed May 5 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Wed May 5 2004  Jacek Konieczny <jajcus@jajcus.net>
- s/tabwidth/tabstop/

* Sat May 1 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Fri Apr 30 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Fri Apr 30 2004  Jacek Konieczny <jajcus@jajcus.net>
- don't set type='chat' on jabber:x:roster messages

* Fri Apr 30 2004  Jacek Konieczny <jajcus@jajcus.net>
- requirements updated- glib2 and libidn

* Thu Apr 22 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Thu Apr 22 2004  Tomasz Sterna <tomek@xiaoka.com>
- checking return code of stream_eat()

* Wed Apr 14 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Wed Apr 14 2004  Jacek Konieczny <jajcus@jajcus.net>
- ported to glib2

* Tue Apr 13 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Tue Apr 13 2004  Tomasz Sterna <tomek@xiaoka.com>
- restored VERSION #define

* Tue Apr 13 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Tue Apr 13 2004  Tomasz Sterna <tomek@xiaoka.com>
- fixes to the build system

* Tue Apr 13 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Tue Apr 13 2004  Jacek Konieczny <jajcus@jajcus.net>
- glib2 minimum version string fixed

* Tue Apr 13 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Tue Apr 13 2004  Jacek Konieczny <jajcus@jajcus.net>
- ported to GLib 2
- use libidn for proper JID normalization (stringprep,IDNA)

* Tue Apr 6 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Tue Apr 6 2004  Jacek Konieczny <jajcus@jajcus.net>
- translation revised by Ben Branders

* Sun Mar 28 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Sun Mar 28 2004  Jacek Konieczny <jajcus@jajcus.net>
- s/Dutch/Nederlands/

* Sun Mar 28 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Sun Mar 28 2004  Jacek Konieczny <jajcus@jajcus.net>
- Dutch in locale mapping (to be updated)

* Sun Mar 28 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Sun Mar 28 2004  Jacek Konieczny <jajcus@jajcus.net>
- cleanup

* Sun Mar 28 2004  Jacek Konieczny <jajcus@jajcus.net>
- Dutch translation

* Thu Mar 18 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Thu Mar 18 2004  Jacek Konieczny <jajcus@jajcus.net>
- *** Version: 2.0.9 ***

* Thu Mar 18 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Thu Mar 18 2004  Jacek Konieczny <jajcus@jajcus.net>
- updated

* Thu Mar 18 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Thu Mar 18 2004  Jacek Konieczny <jajcus@jajcus.net>
- got rid of the @pld.org.pl e-mail address

* Thu Mar 18 2004  Jacek Konieczny <jajcus@jajcus.net>
- ChangeLog update by makelog.sh

* Thu Mar 18 2004  Jacek Konieczny <jajcus@jajcus.net>
- updated

* Thu Mar 18 2004  Jacek Konieczny <jajcus@jajcus.net>
- update: libgadu-1.4 required, pthread support not recommended

* Thu Mar 18 2004  Jacek Konieczny <jajcus@jajcus.net>
- more ignores

* Thu Mar 18 2004  Jacek Konieczny <jajcus@jajcus.net>
- interactive 'valgrind-int' target with--gen-suppressions=yes option passed to valgrind

* Wed Mar 17 2004  Jacek Konieczny <jajcus@jajcus.net>
- LINGUAS file instead of obsolete ALL_LINGUAS configure.ac variable

* Wed Mar 17 2004  Jacek Konieczny <jajcus@jajcus.net>
- cosmetics

* Wed Mar 17 2004  Jacek Konieczny <jajcus@jajcus.net>
- updated

* Wed Mar 17 2004  Jacek Konieczny <jajcus@jajcus.net>
- don't break on write buffer overflow- just block to send the data

* Wed Mar 17 2004  Jacek Konieczny <jajcus@jajcus.net>
- make jggtrans interruptable when not connected to jabber server- workaround for a bug I couldn't find: do only 100 iterations instead of infinite loop

* Wed Mar 17 2004  Jacek Konieczny <jajcus@jajcus.net>
- do not send presence errors in response to presence errors

* Tue Mar 16 2004  Mariusz Mazur <mmazur@kernel.pl>
- get roster works again

* Mon Mar 15 2004  Mariusz Mazur <mmazur@kernel.pl>
- require new ekg. Old versions stoped working yesterday

* Fri Mar 5 2004  Jacek Konieczny <jajcus@jajcus.net>
- configure--disable-nls should work now

* Mon Mar 1 2004  Mariusz Mazur <mmazur@kernel.pl>
- Jajcus says ping is important

* Mon Mar 1 2004  Mariusz Mazur <mmazur@kernel.pl>
- removed ping support. Not used and only makes a lot of noise when debugging

* Thu Feb 26 2004  Jacek Konieczny <jajcus@jajcus.net>
- solaris library test improved (?)

* Thu Feb 26 2004  Jacek Konieczny <jajcus@jajcus.net>
- search for gethostbyname and socket in specific libraries (should partialy fix solaris build)

* Thu Feb 26 2004  Jacek Konieczny <jajcus@jajcus.net>
- LOG_FTP and LOG_AUTHPRIV are not available on Solaris- use them only when defined

* Fri Feb 20 2004  Jacek Konieczny <jajcus@jajcus.net>
- *** Version 2.0.8 ***

* Fri Feb 20 2004  Jacek Konieczny <jajcus@jajcus.net>
- fixed last change

* Fri Feb 20 2004  Jacek Konieczny <jajcus@jajcus.net>
- updated

* Fri Feb 20 2004  Jacek Konieczny <jajcus@jajcus.net>
- cosmetics

* Fri Feb 20 2004  Jacek Konieczny <jajcus@jajcus.net>
- updates by gettextize

* Fri Feb 20 2004  Jacek Konieczny <jajcus@jajcus.net>
- updated

* Thu Feb 5 2004  Tomasz Sterna <tomek@xiaoka.com>
- initial checkin

* Thu Feb 5 2004  Tomasz Sterna <tomek@xiaoka.com>
- reverted misfix

* Thu Feb 5 2004  Tomasz Sterna <tomek@xiaoka.com>
- fix for autogen.sh's `gettextize--force'

* Thu Feb 5 2004  Tomasz Sterna <tomek@xiaoka.com>
- we now log in with GG_DEFAULT_PROTOCOL_VERSION  [teardrop]

* Thu Feb 5 2004  Tomasz Sterna <tomek@xiaoka.com>
- disabled roster import even more ;-)

* Thu Feb 5 2004  Tomasz Sterna <tomek@xiaoka.com>
- support for protocol 6.0 notifies and statuses

* Wed Feb 4 2004  Jacek Konieczny <jajcus@jajcus.net>
- updates for latest auto*-tools and gettext: autoconf-2.59-2, automake-1.8.2-1, libtool-1.5-14, gettext-0.13.1-1

* Wed Feb 4 2004  Jacek Konieczny <jajcus@jajcus.net>
- 64-bit fixes (without them this won't work on AMD64 or Alpha)

* Wed Feb 4 2004  Jacek Konieczny <jajcus@jajcus.net>
- s/Fatalny blad/Blad krytyczny/; format string fixed

* Mon Feb 2 2004  Jacek Konieczny <jajcus@jajcus.net>
- typos fixed: no ',' before 'a' (bug #3287)

* Fri Jan 30 2004  Jacek Konieczny <jajcus@jajcus.net>
- always send presence_subscribe from /registered jid

* Fri Jan 30 2004  Jacek Konieczny <jajcus@jajcus.net>
- don't sent <presence type='subscribed'/> when not asked to

* Mon Jan 26 2004  Jacek Konieczny <jajcus@jajcus.net>
- obsolete disco features removed

* Sat Jan 24 2004  Jacek Konieczny <jajcus@jajcus.net>
- get/import roster disabled. It is not ported to new protocol/API and causes SIGSEGV

* Sat Jan 24 2004  Jacek Konieczny <jajcus@jajcus.net>
- don't fail on empty <priority/> [teardrop]

* Thu Oct 16 2003  Tomasz Sterna <tomek@xiaoka.com>
- fixed infinite wait, when already registered user tries to reregister
- after deleting transport-contact from roster

* Fri Oct 3 2003  Jacek Konieczny <jajcus@jajcus.net>
- man page by Robert Olejnik

* Sun Sep 14 2003  Jacek Konieczny <jajcus@jajcus.net>
- jabberd 2.0 configuration comments updates

* Sun Sep 14 2003  Jacek Konieczny <jajcus@jajcus.net>
- jabberd 2.0 compatibility fix

* Wed Sep 10 2003  Jacek Konieczny <jajcus@jajcus.net>
- *** Version: 2.0.7 ***

* Wed Sep 10 2003  Jacek Konieczny <jajcus@jajcus.net>
- updated for 2.0.7

* Wed Sep 10 2003  Jacek Konieczny <jajcus@jajcus.net>
- reverted last change (protocol version)

* Tue Sep 9 2003  Jacek Konieczny <jajcus@jajcus.net>
- introduce yourself as GG 6.0 when using TLS

* Mon Sep 8 2003  Jacek Konieczny <jajcus@jajcus.net>
- info about mailing list added

* Mon Sep 8 2003  Jacek Konieczny <jajcus@jajcus.net>
- polish translation updated

* Mon Sep 8 2003  Jacek Konieczny <jajcus@jajcus.net>
- when invisible send own presence as 'away' with '(invisible)' in status

* Mon Sep 8 2003  Jacek Konieczny <jajcus@jajcus.net>
- do nothing in session_set_status() when session is not connected

* Mon Sep 8 2003  Jacek Konieczny <jajcus@jajcus.net>
- do not call session_set status when session is not available

* Mon Sep 8 2003  Jacek Konieczny <jajcus@jajcus.net>
- set presence of all contacts to unavailable when disconnected from server

* Sun Sep 7 2003  Jacek Konieczny <jajcus@jajcus.net>
- don't panic when unknown user ask for GG client version

* Sun Sep 7 2003  Tomasz Sterna <tomek@xiaoka.com>
- cutting GG-side status to allowed 70 characters

* Sun Sep 7 2003  Tomasz Sterna <tomek@xiaoka.com>
- loging in with protocol 0x18 (GG 5.0)

* Sun Sep 7 2003  Tomasz Sterna <tomek@xiaoka.com>
- Gadu-Gadu protocol to version mapping updated

* Sun Sep 7 2003  Tomasz Sterna <tomek@xiaoka.com>
- segv while empty client resource fixed

* Fri Aug 8 2003  Jacek Konieczny <jajcus@jajcus.net>
- newline conversion

* Sat Jun 28 2003  Jacek Konieczny <jajcus@jajcus.net>
- *** Version: 2.0.6 ***

* Sat Jun 28 2003  Jacek Konieczny <jajcus@jajcus.net>
- cosmetics

* Sat Jun 28 2003  Jacek Konieczny <jajcus@jajcus.net>
- updated for 2.0.6

* Fri Jun 27 2003  Jacek Konieczny <jajcus@jajcus.net>
- include debug.h last- it contains macros that may break other headers

* Fri Jun 27 2003  Jacek Konieczny <jajcus@jajcus.net>
- updated

* Fri Jun 27 2003  Jacek Konieczny <jajcus@jajcus.net>
- "not available with descrition" is also not available

* Fri Jun 27 2003  Jacek Konieczny <jajcus@jajcus.net>
- return unavailable contact presence from bare jid unless this contact was active during current session
- support both "get roster" and "import roster" requested in registration form
- react to presence changes of the resource with the highest priority only
- disconnect only when the last resource becomes unavailable

* Fri Jun 27 2003  Jacek Konieczny <jajcus@jajcus.net>
- "import roster" is not recommended
- unsubscribe user from all contacts presence when unregistering

* Fri Jun 27 2003  Jacek Konieczny <jajcus@jajcus.net>
- unsubscribe != unregister
- do not reply to probes if contact status is not yet known
- send "unavailable" presence probe responses from bare jid

* Fri Jun 27 2003  Jacek Konieczny <jajcus@jajcus.net>
- 'unknown' user status support (before GG server returns notifications)

* Fri Jun 27 2003  Jacek Konieczny <jajcus@jajcus.net>
- "import roster" is not recommended
- "menu" reformated

* Fri Jun 27 2003  Jacek Konieczny <jajcus@jajcus.net>
- segmentation fault, when message from unknown user is received, fixed

* Tue May 27 2003  Jacek Konieczny <jajcus@jajcus.net>
- *** Version 2.0.5 ***

* Tue May 27 2003  Jacek Konieczny <jajcus@jajcus.net>
- updated

* Tue May 27 2003  Jacek Konieczny <jajcus@jajcus.net>
- updated for 2.0.5

* Tue May 27 2003  Jacek Konieczny <jajcus@jajcus.net>
- updated

* Tue May 27 2003  Jacek Konieczny <jajcus@jajcus.net>
- show connection information to user

* Tue May 27 2003  Jacek Konieczny <jajcus@jajcus.net>
- some servers don't accept TLS

* Tue May 27 2003  Jacek Konieczny <jajcus@jajcus.net>
- info about TLS

* Tue May 27 2003  Jacek Konieczny <jajcus@jajcus.net>
- updated

* Tue May 27 2003  Jacek Konieczny <jajcus@jajcus.net>
- clean shutdown- let all <presence type="unavailable"/> be written to Jabber stream

* Tue May 27 2003  Jacek Konieczny <jajcus@jajcus.net>
- return unavailable presence on probe instead of error when user is not available (again)

* Tue May 27 2003  Jacek Konieczny <jajcus@jajcus.net>
- use one function to generate user session info both for browse and disco

* Tue May 27 2003  Jacek Konieczny <jajcus@jajcus.net>
- support for TLS-enabled libgadu and TLS

* Tue May 20 2003  Jacek Konieczny <jajcus@jajcus.net>
- use full jid in presence probe replies

* Mon May 19 2003  Jacek Konieczny <jajcus@jajcus.net>
- *** Version: 2.0.4 ***

* Mon May 19 2003  Jacek Konieczny <jajcus@jajcus.net>
- have I said "for 2.0.4"? :)

* Mon May 19 2003  Jacek Konieczny <jajcus@jajcus.net>
- updated for 2.0.4

* Mon May 19 2003  Jacek Konieczny <jajcus@jajcus.net>
- cosmetics

* Mon May 19 2003  Jacek Konieczny <jajcus@jajcus.net>
- updated for 2.0.4

* Mon May 19 2003  Jacek Konieczny <jajcus@jajcus.net>
- presence cleanups:
- all GG users use a "GG" resource
- send only one transport presence on login
- update transport presence on user presence change

* Fri May 16 2003  Jacek Konieczny <jajcus@jajcus.net>
- process all stats in a get query

* Fri May 16 2003  Mariusz Mazur <mmazur@kernel.pl>
- mental blocks rock; most likely this is the fix for the mysterious
- delay_disconnect crash :)

* Fri May 16 2003  Jacek Konieczny <jajcus@jajcus.net>
- do not touch pid-file if not configured to do so

* Wed May 14 2003  Jacek Konieczny <jajcus@jajcus.net>
- NULL dereference bug fixed

* Tue May 13 2003  Jacek Konieczny <jajcus@jajcus.net>
- do not try to use invalid session

* Mon May 12 2003  Jacek Konieczny <jajcus@jajcus.net>
- free Resource object _after_ its last use, not earlier :)

* Fri May 9 2003  Jacek Konieczny <jajcus@jajcus.net>
- wait before disconnecting after <presence type="unavailable"> is received.
- <presence type="invisible"> may come just after that

* Fri May 9 2003  Jacek Konieczny <jajcus@jajcus.net>
- presence-invisible support

* Fri May 9 2003  Jacek Konieczny <jajcus@jajcus.net>
- a function to build user's full jid

* Fri May 9 2003  Jacek Konieczny <jajcus@jajcus.net>
- presence-invisible support
- use full jids (with resource) for user messages/presence

* Fri May 9 2003  Jacek Konieczny <jajcus@jajcus.net>
- more JEP-4 compatibility "fixes"

* Wed May 7 2003  Jacek Konieczny <jajcus@jajcus.net>
- updated

* Wed May 7 2003  Jacek Konieczny <jajcus@jajcus.net>
- typo

* Wed May 7 2003  Jacek Konieczny <jajcus@jajcus.net>
- *** Version: 2.0.3 ***

* Wed May 7 2003  Jacek Konieczny <jajcus@jajcus.net>
- updates for 2.0.3

* Wed May 7 2003  Jacek Konieczny <jajcus@jajcus.net>
- include default options in the lists of available options

* Wed May 7 2003  Jacek Konieczny <jajcus@jajcus.net>
- proper <browse/> config for jabberd (copatible with active JEP-11 version)

* Wed May 7 2003  Jacek Konieczny <jajcus@jajcus.net>
- the WinJab bug is also a Psi bug

* Wed May 7 2003  Jacek Konieczny <jajcus@jajcus.net>
- implementation of the active version of JEP-11 (<item/> elements instead of
- <service/> and <user/>)
- version attribute added the service item

* Sat May 3 2003  Jacek Konieczny <jajcus@jajcus.net>
- more proxy settings

* Mon Apr 28 2003  Jacek Konieczny <jajcus@jajcus.net>
- hint about compilation on FreeBSD

* Mon Apr 28 2003  Jacek Konieczny <jajcus@jajcus.net>
- autoupdated

* Mon Apr 28 2003  Jacek Konieczny <jajcus@jajcus.net>
- *** Version: 2.0.2 ***

* Mon Apr 28 2003  Jacek Konieczny <jajcus@jajcus.net>
- updated for 2.0.2

* Mon Apr 28 2003  Jacek Konieczny <jajcus@jajcus.net>
- do not send notification request to GG server when presence type=probe is
- received (this caused annoying status changes for GG users in roster)

* Mon Apr 28 2003  Jacek Konieczny <jajcus@jajcus.net>
- translations updated

* Mon Apr 28 2003  Jacek Konieczny <jajcus@jajcus.net>
- link jggtrans with $(INTLLIBS) (needed for some OSes, like FreeBSD)

* Mon Apr 28 2003  Jacek Konieczny <jajcus@jajcus.net>
- updated from .pot (319 translated messages, 3 fuzzy translations, 1 untranslated message.)

* Mon Apr 28 2003  Jacek Konieczny <jajcus@jajcus.net>
- "import roster" option in regitration form

* Sun Apr 27 2003  Jacek Konieczny <jajcus@jajcus.net>
- only process presece packets sent to the transport itself. Presence
- cannot be different for different GG users anyway

* Sun Apr 27 2003  Jacek Konieczny <jajcus@jajcus.net>
- fixes for memory leak and possible NULL dereference, introduced by last changes

* Sun Apr 27 2003  Jacek Konieczny <jajcus@jajcus.net>
- set GG status on login
- change GG status only when this is really needed
- sens last_sys_msg to GG server on login

* Fri Apr 25 2003  Jacek Konieczny <jajcus@jajcus.net>
- "get roster" command doesn't automaticaly subscribe users any more
- new "import roster" command, that subscribes users

* Thu Apr 24 2003  Jacek Konieczny <jajcus@jajcus.net>
- tested with libgadu-1.0

* Thu Apr 24 2003  Jacek Konieczny <jajcus@jajcus.net>
- autoupdated

* Thu Apr 24 2003  Jacek Konieczny <jajcus@jajcus.net>
- *** Version: 2.0.1 ***

* Thu Apr 24 2003  Jacek Konieczny <jajcus@jajcus.net>
- updated for 2.0.1

* Thu Apr 24 2003  Jacek Konieczny <jajcus@jajcus.net>
- do not announce "presence-invisible" feature until it is really supported

* Thu Apr 24 2003  Jacek Konieczny <jajcus@jajcus.net>
- updated

* Thu Apr 24 2003  Jacek Konieczny <jajcus@jajcus.net>
- more source files

* Thu Apr 24 2003  Jacek Konieczny <jajcus@jajcus.net>
- show the GG number used to register in transport with current settings

* Tue Apr 22 2003  Jacek Konieczny <jajcus@jajcus.net>
- require libgadu >= 1.0. If you want to use a snapshot add
--with-libgadu-snapshot to configure command line

* Tue Apr 22 2003  Jacek Konieczny <jajcus@jajcus.net>
- new GG version: 5.0.5 build 111 [smoku]

* Tue Apr 22 2003  Jacek Konieczny <jajcus@jajcus.net>
- large memleak removed

* Tue Apr 22 2003  Jacek Konieczny <jajcus@jajcus.net>
- fixes for locale switching code

* Tue Apr 22 2003  Jacek Konieczny <jajcus@jajcus.net>
- "invisible" should not be enabled by default in jabber:x:data registration form

* Tue Apr 22 2003  Jacek Konieczny <jajcus@jajcus.net>
- convert the message body to utf-8 (probably disconnetion fixed)
- fail when data received is NULL (segfault fixed)

* Tue Apr 22 2003  Jacek Konieczny <jajcus@jajcus.net>
- new log translation handling

* Tue Apr 22 2003  Jacek Konieczny <jajcus@jajcus.net>
- send <presence type="unsubscribed"> to aliens
- new log translation handling

* Tue Apr 22 2003  Jacek Konieczny <jajcus@jajcus.net>
- _do_ send <presence type="subscribed"/> after successfull registration

* Tue Apr 22 2003  Jacek Konieczny <jajcus@jajcus.net>
- mesages about loading users and its failure are debug now
- new log translation handling

* Tue Apr 22 2003  Jacek Konieczny <jajcus@jajcus.net>
- pass localedir to gettext

* Tue Apr 22 2003  Jacek Konieczny <jajcus@jajcus.net>
- use "-m 755" to make sure install dirs ($localedir in particular) will be
- accessible and readable for jggtrans

* Mon Apr 21 2003  Jacek Konieczny <jajcus@jajcus.net>
- where the commit logs should be sent

* Mon Apr 21 2003  Jacek Konieczny <jajcus@jajcus.net>
- I would forget about the great translation

* Mon Apr 21 2003  Jacek Konieczny <jajcus@jajcus.net>
- *** Version: 2.0.0 ***

* Mon Apr 21 2003  Jacek Konieczny <jajcus@jajcus.net>
- updated for 2.0.0

* Mon Apr 21 2003  Jacek Konieczny <jajcus@jajcus.net>
- small updates

* Mon Apr 21 2003  Jacek Konieczny <jajcus@jajcus.net>
- pass libgadu-specific CFLAGS to linker (needed for libgadu-1.0rcX)

* Mon Apr 21 2003  Jacek Konieczny <jajcus@jajcus.net>
- updated for 2.0.0

* Mon Apr 21 2003  Jacek Konieczny <jajcus@jajcus.net>
- only "get roster" command is experimental now

* Mon Apr 21 2003  Jacek Konieczny <jajcus@jajcus.net>
- small updates

* Mon Apr 21 2003  Jacek Konieczny <jajcus@jajcus.net>
- polish translations [smoku]

* Sun Apr 20 2003  Jacek Konieczny <jajcus@jajcus.net>
- s/gived/given/

* Sat Apr 19 2003  Jacek Konieczny <jajcus@jajcus.net>
- do not gettext-translate bare newlines

* Thu Apr 17 2003  Jacek Konieczny <jajcus@jajcus.net>
- do not send system messages twice

* Thu Apr 17 2003  Jacek Konieczny <jajcus@jajcus.net>
- announce also some non-namespace features

* Wed Apr 16 2003  Jacek Konieczny <jajcus@jajcus.net>
- do not treat directories in spool_dir as registered users

* Wed Apr 16 2003  Jacek Konieczny <jajcus@jajcus.net>
- cosmetics

* Wed Apr 16 2003  Jacek Konieczny <jajcus@jajcus.net>
- version 2.0.0-test1

* Wed Apr 16 2003  Jacek Konieczny <jajcus@jajcus.net>
- updated to current sources (still most translation are missing)

* Wed Apr 16 2003  Jacek Konieczny <jajcus@jajcus.net>
- send_message() argument should be UTF-8 encoded, conversion moved to sessions.c
- system messages are sent as regular message (not chat) with msg. number in topic

* Wed Apr 16 2003  Jacek Konieczny <jajcus@jajcus.net>
- parent parameter added to form creating functions so less memory copying is done

* Wed Apr 16 2003  Jacek Konieczny <jajcus@jajcus.net>
- some more memleaks removed

* Wed Apr 16 2003  Jacek Konieczny <jajcus@jajcus.net>
- some memleaks removed

* Wed Apr 16 2003  Jacek Konieczny <jajcus@jajcus.net>
- ACL bugfixes

* Wed Apr 16 2003  Jacek Konieczny <jajcus@jajcus.net>
- do not send presence errors to self

* Wed Apr 16 2003  Jacek Konieczny <jajcus@jajcus.net>
- #include <locale.h> was missing.

* Wed Apr 16 2003  Jacek Konieczny <jajcus@jajcus.net>
- project-local suppressions don't make sens, so removed

* Tue Apr 15 2003  Jacek Konieczny <jajcus@jajcus.net>
- all requests should be removed from list when destroyed

* Tue Apr 15 2003  Jacek Konieczny <jajcus@jajcus.net>
- memleaks hunting

* Mon Apr 14 2003  Mariusz Mazur <mmazur@kernel.pl>
- remote-userlist is no more

* Mon Apr 14 2003  Jacek Konieczny <jajcus@jajcus.net>
- requests cleanup

* Mon Apr 14 2003  Jacek Konieczny <jajcus@jajcus.net>
- compiler warning removed

* Mon Apr 14 2003  Jacek Konieczny <jajcus@jajcus.net>
- pubdir change on registration cleanup

* Mon Apr 14 2003  Jacek Konieczny <jajcus@jajcus.net>
- some memleaks and uninitialized data usage fixed (thanks to valgrind)

* Mon Apr 14 2003  Jacek Konieczny <jajcus@jajcus.net>
- include acl.h

* Mon Apr 14 2003  Jacek Konieczny <jajcus@jajcus.net>
- ACL examples

* Mon Apr 14 2003  Jacek Konieczny <jajcus@jajcus.net>
- do not limit use of statistics to admins only, ACL may be used for better access control

* Mon Apr 14 2003  Jacek Konieczny <jajcus@jajcus.net>
- ACLe

* Mon Apr 14 2003  Jacek Konieczny <jajcus@jajcus.net>
- header comments

* Mon Apr 14 2003  Jacek Konieczny <jajcus@jajcus.net>
- admins are those _allowed_, not disallowed :-)

* Mon Apr 14 2003  Jacek Konieczny <jajcus@jajcus.net>
- packet/message statistics gathering

* Mon Apr 14 2003  Jacek Konieczny <jajcus@jajcus.net>
- user counting fixed
- allow statistics gathering only to admins (it takes quite a lot of resources,
- when queried periodically)

* Mon Apr 14 2003  Jacek Konieczny <jajcus@jajcus.net>
- fixes for online user browsing using disco

* Mon Apr 14 2003  Jacek Konieczny <jajcus@jajcus.net>
- JEP-0030: service discovery

* Mon Apr 14 2003  Jacek Konieczny <jajcus@jajcus.net>
- JEP-0039 (statistics gathering) implementation NFY

* Mon Apr 14 2003  Jacek Konieczny <jajcus@jajcus.net>
- detailed info about contacts (names,city etc.) removed

* Mon Apr 14 2003  Jacek Konieczny <jajcus@jajcus.net>
- show server address for hub-driven connections too

* Sun Apr 13 2003  Mariusz Mazur <mmazur@kernel.pl>
- ooops... almost forgot to commit this: killed put_roster code, and
- made get_roster subscribe new contacts automaticaly... nice :)

* Sun Apr 13 2003  Jacek Konieczny <jajcus@jajcus.net>
- some fixes

* Sun Apr 13 2003  Jacek Konieczny <jajcus@jajcus.net>
- store current, not next, server info in server_info. This is much more useful for browsing

* Sun Apr 13 2003  Jacek Konieczny <jajcus@jajcus.net>
- show server address where user is connected or connecting

* Sun Apr 13 2003  Jacek Konieczny <jajcus@jajcus.net>
- browsing of online user (only for admin)

* Sun Apr 13 2003  Mariusz Mazur <mmazur@kernel.pl>
- cosmetics

* Sun Apr 13 2003  Jacek Konieczny <jajcus@jajcus.net>
- <admin/> element

* Sun Apr 13 2003  Jacek Konieczny <jajcus@jajcus.net>
- send presence error when subscription fails (which will never occur)

* Sun Apr 13 2003  Jacek Konieczny <jajcus@jajcus.net>
- put <reported/> only in the first stanza of search results

* Sun Apr 13 2003  Jacek Konieczny <jajcus@jajcus.net>
- cosmetics

* Sun Apr 13 2003  Jacek Konieczny <jajcus@jajcus.net>
- searching with jabber:x:data, seems to work

* Sun Apr 13 2003  Jacek Konieczny <jajcus@jajcus.net>
- cleanups

* Sat Apr 12 2003  Mariusz Mazur <mmazur@kernel.pl>
- sending authorization to a contact results in receiving an authorization
- from that contact... it's more idiot proof now

* Sat Apr 12 2003  Mariusz Mazur <mmazur@kernel.pl>
- "typo" in debug message

* Sat Apr 12 2003  Mariusz Mazur <mmazur@kernel.pl>
- when removing authorization from a contact transport logged off; fixed

* Fri Apr 11 2003  Mariusz Mazur <mmazur@kernel.pl>
- reverted last change- the core of the problem is elsewhere

* Fri Apr 11 2003  Mariusz Mazur <mmazur@kernel.pl>
- errormessage stating that a configuration file for an account wasn't
- found is now displayed via debug() and not g_warning() because
- this error is triggered on almost every occasion so it just
- floods the logs without any good reason

* Fri Apr 11 2003  Mariusz Mazur <mmazur@kernel.pl>
- some cleaning in the legacy register code

* Fri Apr 11 2003  Jacek Konieczny <jajcus@jajcus.net>
- more simplifications: a function to create empty form

* Fri Apr 11 2003  Jacek Konieczny <jajcus@jajcus.net>
- form creation simplified (using functions from forms.h)
- public directory change via jabber:x:data finished
- some other cleanups

* Fri Apr 11 2003  Jacek Konieczny <jajcus@jajcus.net>
- properly handle RT_CHANGE (public tirectory write result)

* Fri Apr 11 2003  Jacek Konieczny <jajcus@jajcus.net>
- save user after confirming, because unconfirmed user will not be saved
- process GG_EVENT_PUBDIR50_WRITE. The fact that it cannot be handled properly
- for legacy jabber:x:register doesn't mean that it shouldn't be handled at all

* Fri Apr 11 2003  Jacek Konieczny <jajcus@jajcus.net>
- files with functions for creating jabber:x:data forms added

* Thu Apr 10 2003  Jacek Konieczny <jajcus@jajcus.net>
- public directory change using jabber:x:data implemented (NFY)
- some fixes for legacy pubdir change code

* Thu Apr 10 2003  Mariusz Mazur <mmazur@kernel.pl>
- we ignore GG_PUBDIR50_WRITE since it's of no use to us

* Thu Apr 10 2003  Mariusz Mazur <mmazur@kernel.pl>
- fixed segfault

* Wed Apr 9 2003  Jacek Konieczny <jajcus@jajcus.net>
- do not reveal full OS version

* Tue Apr 8 2003  Jacek Konieczny <jajcus@jajcus.net>
- GG password change. After the password is changed the annoying message
- doesn't show any more :-)

* Tue Apr 8 2003  Jacek Konieczny <jajcus@jajcus.net>
- send messages to full jid (with resource)

* Sun Apr 6 2003  Jacek Konieczny <jajcus@jajcus.net>
- user registration via jabber:x:data

* Sun Apr 6 2003  Mariusz Mazur <mmazur@kernel.pl>
- gettext support finished in 95% anything else should come up while
- using jggtrans

* Sun Apr 6 2003  Jacek Konieczny <jajcus@jajcus.net>
- legacy interface to locale changing

* Sun Apr 6 2003  Jacek Konieczny <jajcus@jajcus.net>
- user locale setting loading fixed

* Sun Apr 6 2003  Mariusz Mazur <mmazur@kernel.pl>
- finished gettext

* Sun Apr 6 2003  Mariusz Mazur <mmazur@kernel.pl>
- gettext support

* Sun Apr 6 2003  Jacek Konieczny <jajcus@jajcus.net>
- use data gathering to change account options
- fixed segfault when pubdir data are empty in registration form

* Sun Apr 6 2003  Mariusz Mazur <mmazur@kernel.pl>
- switched URL to jggtrans' project homepage

* Sun Apr 6 2003  Jacek Konieczny <jajcus@jajcus.net>
- request "hash" must be unique so counter is used instead of time

* Sun Apr 6 2003  Mariusz Mazur <mmazur@kernel.pl>
- I guess neither .patch nor .diff will be commited and I often have them
- inside this dir

* Sun Apr 6 2003  Jacek Konieczny <jajcus@jajcus.net>
- some compiler warnings removed

* Sun Apr 6 2003  Jacek Konieczny <jajcus@jajcus.net>
- _() is not the same as N_()

* Sat Apr 5 2003  Mariusz Mazur <mmazur@kernel.pl>
- update-ggpubdir-when-registering works... the thing is hackish, ugly
- and it smells, but it *works* and I'll redesign it later

* Sat Apr 5 2003  Jacek Konieczny <jajcus@jajcus.net>
- i18n infrastructure seems complete. Now only testing, bugfixing and translations are needed.

* Sat Apr 5 2003  Jacek Konieczny <jajcus@jajcus.net>
- cosmetics

* Fri Apr 4 2003  Jacek Konieczny <jajcus@jajcus.net>
- perliminary gettext support

* Fri Apr 4 2003  Jacek Konieczny <jajcus@jajcus.net>
- gettext support
- support for non-snapshot libgadu versions

* Fri Apr 4 2003  Jacek Konieczny <jajcus@jajcus.net>
- cosmetics

* Fri Apr 4 2003  Jacek Konieczny <jajcus@jajcus.net>
- another NULL dereference fixed (bug found by [venglin])

* Fri Apr 4 2003  Jacek Konieczny <jajcus@jajcus.net>
- another NULL pointer dereference fixed [venglin]

* Fri Apr 4 2003  Jacek Konieczny <jajcus@jajcus.net>
- segfault caused by NULL pointer dereference fixed [venglin]

* Fri Apr 4 2003  Jacek Konieczny <jajcus@jajcus.net>
- another patcher :-)

* Fri Apr 4 2003  Jacek Konieczny <jajcus@jajcus.net>
- possible NULL-dereference problem removed

* Thu Apr 3 2003  Mariusz Mazur <mmazur@kernel.pl>
- finished pubdir-update-when-registering code... only to find out it has One
- Big Synchronization Issue that needs addressing :( Going to sleep;
- will finish it tomorrow

* Thu Apr 3 2003  Mariusz Mazur <mmazur@kernel.pl>
- typo
- no email

* Tue Mar 25 2003  Jacek Konieczny <jajcus@jajcus.net>
- GG client version number in vcard [smoku]

* Mon Mar 24 2003  Jacek Konieczny <jajcus@jajcus.net>
- *** Version: 1.4.1 ***

* Mon Mar 24 2003  Jacek Konieczny <jajcus@jajcus.net>
- cosmetics

* Mon Mar 24 2003  Jacek Konieczny <jajcus@jajcus.net>
- updates for 1.4.1

* Mon Mar 24 2003  Jacek Konieczny <jajcus@jajcus.net>
- send "help" as one message. It may be messed by multithreaded servers otherwise.

* Mon Mar 24 2003  Jacek Konieczny <jajcus@jajcus.net>
- GG version detection: 5.0.3- 5.0.5 [smoku]

* Mon Mar 24 2003  Jacek Konieczny <jajcus@jajcus.net>
- saving of user settings (invisible/friends-only) [smoku]

* Mon Mar 24 2003  Jacek Konieczny <jajcus@jajcus.net>
- timestamps for delayed messages added
- handling of delayed chat messages fixed

* Mon Mar 24 2003  Jacek Konieczny <jajcus@jajcus.net>
- searching people by email is not supported

* Mon Mar 17 2003  Mariusz Mazur <mmazur@kernel.pl>
- searching people by email is not supported

* Fri Feb 28 2003  Mariusz Mazur <mmazur@kernel.pl>
- small fix for multiple servers support

* Thu Feb 6 2003  Jacek Konieczny <jajcus@jajcus.net>
- autorestart (which worked only when-D and-d where given) fixed

* Wed Feb 5 2003  Jacek Konieczny <jajcus@jajcus.net>
- *** Version: 1.4.0 ***

* Wed Feb 5 2003  Mariusz Mazur <mmazur@kernel.pl>
- <conn_timeout/> set to 60

* Wed Feb 5 2003  Jacek Konieczny <jajcus@jajcus.net>
- updates for 1.4.0

* Wed Feb 5 2003  Jacek Konieczny <jajcus@jajcus.net>
- updates

* Wed Feb 5 2003  Jacek Konieczny <jajcus@jajcus.net>
- mmazur is a regular developer now, not just a patch author :-)

* Wed Feb 5 2003  Jacek Konieczny <jajcus@jajcus.net>
- description of <servers/> element

* Wed Feb 5 2003  Jacek Konieczny <jajcus@jajcus.net>
- description of <servers/> element

* Tue Feb 4 2003  Jacek Konieczny <jajcus@jajcus.net>
- fixed segfault on empty search result

* Tue Feb 4 2003  Jacek Konieczny <jajcus@jajcus.net>
- fixed segfault on bad registration input

* Tue Feb 4 2003  Jacek Konieczny <jajcus@jajcus.net>
- version: 1.4.0-test1
- required libgadu version: 20030130

* Tue Feb 4 2003  Jacek Konieczny <jajcus@jajcus.net>
- s/gg_server/gg_servers/, s/Server/GgServer/

* Tue Feb 4 2003  Jacek Konieczny <jajcus@jajcus.net>
- compiler warnings removed

* Tue Feb 4 2003  Jacek Konieczny <jajcus@jajcus.net>
- cosmetics

* Tue Feb 4 2003  Jacek Konieczny <jajcus@jajcus.net>
- segfault, when no "active" seqrch key is given, fixed

* Mon Feb 3 2003  Mariusz Mazur <mmazur@kernel.pl>
- fixed sending errors

* Mon Feb 3 2003  Mariusz Mazur <mmazur@kernel.pl>
- implemented the new libgadu search api

* Wed Jan 29 2003  Jacek Konieczny <jajcus@jajcus.net>
- s/gg_server/g_list_first(gg_server)/ where the first server is needed

* Tue Jan 28 2003  Mariusz Mazur <mmazur@kernel.pl>
- switched from static table to GList in the multiple servers support code;
- needs testing

* Mon Jan 27 2003  Mariusz Mazur <mmazur@kernel.pl>
- server list support (if connection to first server failed, try connecting
- to the next one)

* Sat Jan 25 2003  Mariusz Mazur <mmazur@kernel.pl>
- typo

* Wed Jan 22 2003  Jacek Konieczny <jajcus@jajcus.net>
- *** Version: 1.3.1 ***

* Wed Jan 22 2003  Jacek Konieczny <jajcus@jajcus.net>
- Swiergot added

* Wed Jan 22 2003  Jacek Konieczny <jajcus@jajcus.net>
- updates for 1.3.1

* Wed Jan 22 2003  Jacek Konieczny <jajcus@jajcus.net>
- cosmetics

* Wed Jan 22 2003  Jacek Konieczny <jajcus@jajcus.net>
- remove pid file on exit (suggested by [swiergot])
- write the pid file before dropping privilages, so it may be placed in /var/run
- clear pid file on exit if it cannot be removed

* Wed Jan 22 2003  Jacek Konieczny <jajcus@jajcus.net>
- return proper jabberid in vCard and search result

* Wed Jan 22 2003  Jacek Konieczny <jajcus@jajcus.net>
- add "-Wall" to CFLAGS

* Wed Jan 22 2003  Jacek Konieczny <jajcus@jajcus.net>
- crash caused by <presence> messages with empty <priority/> fixed [smoku]
- similar, usually buggy, code rewritten
- code cleanup

* Thu Jan 16 2003  Jacek Konieczny <jajcus@jajcus.net>
- *** Version: 1.3.0 ***

* Thu Jan 16 2003  Jacek Konieczny <jajcus@jajcus.net>
- updates

* Thu Jan 16 2003  Jacek Konieczny <jajcus@jajcus.net>
- updates for 1.3.0

* Thu Jan 16 2003  Jacek Konieczny <jajcus@jajcus.net>
- pkg-config support for libgadu detection

* Thu Jan 16 2003  Jacek Konieczny <jajcus@jajcus.net>
- log information about restart/exit

* Wed Jan 15 2003  Mariusz Mazur <mmazur@kernel.pl>
- vim temp files

* Wed Jan 15 2003  Jacek Konieczny <jajcus@jajcus.net>
- 1.2.4-test3

* Wed Jan 15 2003  Jacek Konieczny <jajcus@jajcus.net>
- disable broken "get roster"/"put roster" commands

* Wed Jan 15 2003  Jacek Konieczny <jajcus@jajcus.net>
- updated GG client version table [smoku]

* Wed Jan 15 2003  Jacek Konieczny <jajcus@jajcus.net>
- restart only when connection is broken or SIGHUP received

* Wed Jan 15 2003  Jacek Konieczny <jajcus@jajcus.net>
- include patch authors nicknames for use in ChangeLog entries

* Wed Jan 15 2003  Jacek Konieczny <jajcus@jajcus.net>
- check libgadu after pthreads [smoku]

* Wed Jan 15 2003  Jacek Konieczny <jajcus@jajcus.net>
- jabber:iq:version client query support. [smoku]

* Wed Jan 15 2003  Jacek Konieczny <jajcus@jajcus.net>
- write files only if modified (this doesn't work anyway :-( )

* Wed Jan 15 2003  Jacek Konieczny <jajcus@jajcus.net>
- 1.2.4-test2

* Wed Jan 15 2003  Jacek Konieczny <jajcus@jajcus.net>
- cosmetics

* Wed Jan 15 2003  Jacek Konieczny <jajcus@jajcus.net>
- restart after jabber connection is broken

* Wed Jan 15 2003  Jacek Konieczny <jajcus@jajcus.net>
- default value parameter added to config_load_int()

* Wed Jan 15 2003  Jacek Konieczny <jajcus@jajcus.net>
- cosmetics

* Wed Jan 15 2003  Jacek Konieczny <jajcus@jajcus.net>
- cosmetics

* Tue Jan 14 2003  Jacek Konieczny <jajcus@jajcus.net>
- support (experimental) for userlist stored on GG server

* Tue Jan 14 2003  Jacek Konieczny <jajcus@jajcus.net>
- "friends only" and "invisible" commands

* Tue Jan 14 2003  Jacek Konieczny <jajcus@jajcus.net>
- automake update

* Mon Jan 13 2003  Jacek Konieczny <jajcus@jajcus.net>
- working on message-commands

* Mon Jan 13 2003  Jacek Konieczny <jajcus@jajcus.net>
- in presence_probe() take stream from argument, not from session (which may be
- undefined)

* Mon Jan 13 2003  Jacek Konieczny <jajcus@jajcus.net>
- stop processing jabber:iq:gateway after sending an error

* Mon Jan 13 2003  Jacek Konieczny <jajcus@jajcus.net>
- drop user session, when registration form is rejected (patch by mmazur)

* Mon Jan 13 2003  Jacek Konieczny <jajcus@jajcus.net>
- typo

* Mon Jan 13 2003  Jacek Konieczny <jajcus@jajcus.net>
- don't complain about jabber:iq:version

* Sun Jan 12 2003  Jacek Konieczny <jajcus@jajcus.net>
- unused functions removed

* Sun Jan 12 2003  Jacek Konieczny <jajcus@jajcus.net>
- typo (patch by mmazur)

* Tue Jan 7 2003  Jacek Konieczny <jajcus@jajcus.net>
- typo

* Mon Dec 30 2002  Jacek Konieczny <jajcus@jajcus.net>
- Version: 1.2.3

* Mon Dec 30 2002  Jacek Konieczny <jajcus@jajcus.net>
- don't allow control characters

* Mon Dec 30 2002  Jacek Konieczny <jajcus@jajcus.net>
- missing INSTALL file added

* Mon Dec 30 2002  Jacek Konieczny <jajcus@jajcus.net>
- updates for 1.2.3

* Mon Dec 30 2002  Jacek Konieczny <jajcus@jajcus.net>
- GG_STATUS_BUSY (which is "zaraz wracam" in GG) translated to "XA" instead of "DND"

* Mon Dec 30 2002  Jacek Konieczny <jajcus@jajcus.net>
- typos

* Sun Dec 29 2002  Jacek Konieczny <jajcus@jajcus.net>
- missing files added to SOURCES

* Sun Dec 29 2002  Jacek Konieczny <jajcus@jajcus.net>
- updates for 1.2.3

* Sun Dec 29 2002  Jacek Konieczny <jajcus@jajcus.net>
- do not set status string if not given by GG user

* Sun Dec 29 2002  Jacek Konieczny <jajcus@jajcus.net>
- initialize status for user contacts (patch by mmazur)

* Sun Dec 29 2002  Jacek Konieczny <jajcus@jajcus.net>
--g and-u command line options descriptions fixed (thanks to mmazur)

* Sun Dec 29 2002  Jacek Konieczny <jajcus@jajcus.net>
- use custom character conversion function instead of iconv() which is broken
- in some implementations (at least in glibc 2.2)

* Sun Dec 29 2002  Jacek Konieczny <jajcus@jajcus.net>
- use custom character conversion function instead of iconv() which is broken
- in some implementations (at least in glibc 2.2)

* Wed Dec 25 2002  Jacek Konieczny <jajcus@jajcus.net>
- Version: 1.2.2

* Wed Dec 25 2002  Jacek Konieczny <jajcus@jajcus.net>
- Updates for 1.2.2

* Wed Dec 25 2002  Jacek Konieczny <jajcus@jajcus.net>
- poprawiona kowersja pustych string�w

* Wed Dec 25 2002  Jacek Konieczny <jajcus@jajcus.net>
- tag <HOME/> w <ADDR/>
- dodatkowe (pewnie niepotrzebne) zabezpieczenia, przed null-dereference

* Tue Dec 10 2002  Jacek Konieczny <jajcus@jajcus.net>
- uaktualnienie

* Tue Dec 10 2002  Jacek Konieczny <jajcus@jajcus.net>
- Version: 1.2.1
- fixes for compilation on FreeBSD

* Tue Dec 10 2002  Jacek Konieczny <jajcus@jajcus.net>
- Tomasz Sterna added as the first "patcher" :-)

* Tue Dec 10 2002  Jacek Konieczny <jajcus@jajcus.net>
- transport version query support

* Tue Dec 10 2002  Jacek Konieczny <jajcus@jajcus.net>
- copy user query for request. Original query will be freed when its processing ends.

* Tue Dec 10 2002  Jacek Konieczny <jajcus@jajcus.net>
- proper GG status change when no reason is given

* Mon Dec 9 2002  Jacek Konieczny <jajcus@jajcus.net>
- Version: 1.2.0

* Mon Dec 9 2002  Jacek Konieczny <jajcus@jajcus.net>
- more memleaks removed

* Sun Dec 8 2002  Jacek Konieczny <jajcus@jajcus.net>
- prepare to for 1.2.0

* Sun Dec 8 2002  Jacek Konieczny <jajcus@jajcus.net>
- some memory leaks removed

* Sun Dec 8 2002  Jacek Konieczny <jajcus@jajcus.net>
- some memory leaks removed

* Sat Dec 7 2002  Jacek Konieczny <jajcus@jajcus.net>
- compiler warnings removed

* Sat Dec 7 2002  Jacek Konieczny <jajcus@jajcus.net>
- poprawki dla `make distcheck`

* Sat Dec 7 2002  Jacek Konieczny <jajcus@jajcus.net>
- updates for new autoconf/automake

* Fri Dec 6 2002  Jacek Konieczny <jajcus@jajcus.net>
- cleanup and small fixes

* Fri Dec 6 2002  Jacek Konieczny <jajcus@jajcus.net>
- contact IP/port/version info

* Fri Dec 6 2002  Jacek Konieczny <jajcus@jajcus.net>
- Contact IP/port/version info support

* Fri Dec 6 2002  Jacek Konieczny <jajcus@jajcus.net>
- prepare for userlist import

* Fri Dec 6 2002  Jacek Konieczny <jajcus@jajcus.net>
- workaroud for threded/non-threaded libgadu versions incompabilities

* Fri Dec 6 2002  Jacek Konieczny <jajcus@jajcus.net>
- simplified

* Fri Dec 6 2002  Jacek Konieczny <jajcus@jajcus.net>
- more ignores

* Fri Dec 6 2002  Jacek Konieczny <jajcus@jajcus.net>
- more ignores

* Tue Jun 11 2002  Jacek Konieczny <jajcus@jajcus.net>
-1

* Tue Jun 11 2002  Jacek Konieczny <jajcus@jajcus.net>
- Version: 1.1.0

* Mon Jun 10 2002  Jacek Konieczny <jajcus@jajcus.net>
- presence change reason support

* Thu Jun 6 2002  Jacek Konieczny <jajcus@jajcus.net>
- +1

* Wed Jun 5 2002  Jacek Konieczny <jajcus@jajcus.net>
- version 1.0.1

* Wed Jun 5 2002  Jacek Konieczny <jajcus@jajcus.net>
- allow to configure server address and port for gg_login()

* Sat May 4 2002  Jacek Konieczny <jajcus@jajcus.net>
- updates for new libgadu

* Sat Apr 13 2002  Jacek Konieczny <jajcus@jajcus.net>
- 1.0.0 changes

* Sat Apr 13 2002  Jacek Konieczny <jajcus@jajcus.net>
- Version: 1.0.0

* Sun Mar 24 2002  Jacek Konieczny <jajcus@jajcus.net>
- ctags support

* Mon Mar 4 2002  Jacek Konieczny <jajcus@jajcus.net>
- fixed crash when user is not found on vCard lookup

* Tue Feb 26 2002  Jacek Konieczny <jajcus@jajcus.net>
- fix for crash on bad jid in message

* Sun Feb 24 2002  Jacek Konieczny <jajcus@jajcus.net>
- fixed bug causing hang on some searches

* Sun Feb 24 2002  Jacek Konieczny <jajcus@jajcus.net>
- updates for 0.9.9 release

* Sun Feb 24 2002  Jacek Konieczny <jajcus@jajcus.net>
- updates for latest libgadu

* Sat Feb 23 2002  Jacek Konieczny <jajcus@jajcus.net>
- support for large messages

* Sat Feb 23 2002  Jacek Konieczny <jajcus@jajcus.net>
- fix for bug on unconvertable characters

* Sat Feb 23 2002  Jacek Konieczny <jajcus@jajcus.net>
- more fixes

* Sat Feb 23 2002  Jacek Konieczny <jajcus@jajcus.net>
- more fixes

* Sat Feb 23 2002  Jacek Konieczny <jajcus@jajcus.net>
- hopefully fixed shutdown crash and some related crashes

* Sat Feb 23 2002  Jacek Konieczny <jajcus@jajcus.net>
- updates

* Fri Feb 22 2002  Jacek Konieczny <jajcus@jajcus.net>
- auto reconnect (to gg server) support

* Fri Feb 22 2002  Jacek Konieczny <jajcus@jajcus.net>
- do not free() users on exit, there should be none. If they are any left print warning.

* Mon Feb 11 2002  Jacek Konieczny <jajcus@jajcus.net>
- added timeout/interval settings (I thought they are already there)

* Fri Feb 8 2002  Jacek Konieczny <jajcus@jajcus.net>
- Version: 0.9.8

* Wed Feb 6 2002  Jacek Konieczny <jajcus@jajcus.net>
- docs updates

* Wed Feb 6 2002  Jacek Konieczny <jajcus@jajcus.net>
- more namespaces for jabber.xml <browse/> section

* Wed Feb 6 2002  Jacek Konieczny <jajcus@jajcus.net>
- s/x-gg/x-gadugadu/

* Wed Feb 6 2002  Jacek Konieczny <jajcus@jajcus.net>
- s/libgg/libgadu/

* Mon Feb 4 2002  Jacek Konieczny <jajcus@jajcus.net>
- back to old error handling

* Mon Feb 4 2002  Jacek Konieczny <jajcus@jajcus.net>
- more changes with error handling

* Mon Feb 4 2002  Jacek Konieczny <jajcus@jajcus.net>
- HUP also to libgg

* Mon Feb 4 2002  Jacek Konieczny <jajcus@jajcus.net>
- let libgg handle errors

* Sun Feb 3 2002  Jacek Konieczny <jajcus@jajcus.net>
- jggtrans in config root

* Sun Feb 3 2002  Jacek Konieczny <jajcus@jajcus.net>
- config file name changes

* Sun Feb 3 2002  Jacek Konieczny <jajcus@jajcus.net>
- config file name changes

* Sun Feb 3 2002  Jacek Konieczny <jajcus@jajcus.net>
- s/\<ggtrans\>/jggtrans/ (mainly config file name)

* Sun Feb 3 2002  Jacek Konieczny <jajcus@jajcus.net>
- support for multiple user resources and their priorities

* Sun Feb 3 2002  Jacek Konieczny <jajcus@jajcus.net>
- functions to change uid/gid
- print active session status on SIGUSR

* Sun Feb 3 2002  Jacek Konieczny <jajcus@jajcus.net>
- fuctions for converting users status information between GG and Jabber

* Sat Feb 2 2002  Jacek Konieczny <jajcus@jajcus.net>
- +1

* Sat Feb 2 2002  Jacek Konieczny <jajcus@jajcus.net>
- missing files added

* Sat Feb 2 2002  Jacek Konieczny <jajcus@jajcus.net>
- strip whitespaces from configuration files entries

* Sat Feb 2 2002  Jacek Konieczny <jajcus@jajcus.net>
- Error message, when cannot connect to Jabber server

* Sat Feb 2 2002  Jacek Konieczny <jajcus@jajcus.net>
- fixed register bug

* Sat Feb 2 2002  Jacek Konieczny <jajcus@jajcus.net>
- another WinJab bug workaround

* Sat Feb 2 2002  Jacek Konieczny <jajcus@jajcus.net>
- browse support, seems to work

* Sat Feb 2 2002  Jacek Konieczny <jajcus@jajcus.net>
- Use "x-gg" as service type (until gg is registered)

* Sat Feb 2 2002  Jacek Konieczny <jajcus@jajcus.net>
- improved/simplified <iq/> and namespace support, preparation for browsing

* Sat Feb 2 2002  Jacek Konieczny <jajcus@jajcus.net>
- +1

* Fri Feb 1 2002  Jacek Konieczny <jajcus@jajcus.net>
- WinJab workaround fix

* Fri Feb 1 2002  Jacek Konieczny <jajcus@jajcus.net>
- WinJab "VCARD" bug workaround

* Wed Jan 30 2002  Jacek Konieczny <jajcus@jajcus.net>
- info about licensing and RCS Id tag in header of each source file

* Wed Jan 30 2002  Jacek Konieczny <jajcus@jajcus.net>
- info about sending user data to sms-express.com Sp. z o.o. in registration instructions

* Wed Jan 30 2002  Jacek Konieczny <jajcus@jajcus.net>
- 2 less

* Wed Jan 30 2002  Jacek Konieczny <jajcus@jajcus.net>
- support for system messages--- now sent only once and from the transport,
- not UIN=0

* Wed Jan 30 2002  Jacek Konieczny <jajcus@jajcus.net>
- debug code enabled by default (without this users cannot send usefull bug reports)

* Fri Jan 25 2002  Jacek Konieczny <jajcus@jajcus.net>
- +1 bug

* Thu Jan 24 2002  Jacek Konieczny <jajcus@jajcus.net>
- display "Pong not received" beafore sending next ping

* Thu Jan 24 2002  Jacek Konieczny <jajcus@jajcus.net>
- send ping, even if GG server doesn't respond

* Wed Jan 23 2002  Jacek Konieczny <jajcus@jajcus.net>
- make ping_timeout work for all pings. Don't hardcode the timeout value.

* Wed Jan 23 2002  Jacek Konieczny <jajcus@jajcus.net>
- +1

* Wed Jan 23 2002  Jacek Konieczny <jajcus@jajcus.net>
- fix for segfault on bad <iq type="set"/>

* Tue Jan 22 2002  Jacek Konieczny <jajcus@jajcus.net>
- support for type="error" in <presence/>, <iq/> and message (fix for nasty DoS)

* Mon Jan 21 2002  Jacek Konieczny <jajcus@jajcus.net>
- three new entries

* Mon Jan 21 2002  Jacek Konieczny <jajcus@jajcus.net>
- fix for crash when querying uin=0 for vcard

* Wed Jan 16 2002  Jacek Konieczny <jajcus@jajcus.net>
- changed most g_strcasecmp to strcmp

* Wed Jan 16 2002  Jacek Konieczny <jajcus@jajcus.net>
- support for <remove/> in jabber:iq:register requests

* Tue Jan 15 2002  Jacek Konieczny <jajcus@jajcus.net>
- version up (0.9 is already released)

* Tue Jan 15 2002  Jacek Konieczny <jajcus@jajcus.net>
- don't confirm presence when not connected or not available

* Tue Jan 15 2002  Jacek Konieczny <jajcus@jajcus.net>
- do not install anything

* Tue Jan 15 2002  Jacek Konieczny <jajcus@jajcus.net>
- s/pl/Pl/

* Tue Jan 15 2002  Jacek Konieczny <jajcus@jajcus.net>
- dokumentacja

* Tue Jan 15 2002  Jacek Konieczny <jajcus@jajcus.net>
- moved to sbindir

* Tue Jan 15 2002  Jacek Konieczny <jajcus@jajcus.net>
- help message fixed

* Tue Jan 15 2002  Jacek Konieczny <jajcus@jajcus.net>
- sample config files

* Tue Jan 15 2002  Jacek Konieczny <jajcus@jajcus.net>
- fixed two presence bugs:
- 	- sending "show" instead of "status"
- 	- crash on <presence type="unavailable"/>

* Tue Jan 15 2002  Jacek Konieczny <jajcus@jajcus.net>
- fixed "wrong 'to'" message

* Mon Jan 14 2002  Jacek Konieczny <jajcus@jajcus.net>
- fixed SEGV caused by not accessible log file

* Mon Jan 14 2002  Jacek Konieczny <jajcus@jajcus.net>
- pid file support

* Mon Jan 14 2002  Jacek Konieczny <jajcus@jajcus.net>
- updates

* Mon Jan 14 2002  Jacek Konieczny <jajcus@jajcus.net>
- logging (to syslog and/or file)
- config file set by configure script or command line

* Mon Jan 14 2002  Jacek Konieczny <jajcus@jajcus.net>
- set config directory

* Mon Jan 14 2002  Jacek Konieczny <jajcus@jajcus.net>
- confirm user presence, sending it back

* Sun Jan 13 2002  Jacek Konieczny <jajcus@jajcus.net>
- log handler
- command-line options
- daemon mode

* Sat Jan 12 2002  Jacek Konieczny <jajcus@jajcus.net>
- support for jabber:iq:gateway namespace

* Sat Jan 12 2002  Jacek Konieczny <jajcus@jajcus.net>
- <presence type="probe"\> fixes

* Fri Jan 11 2002  Jacek Konieczny <jajcus@jajcus.net>
- remember "to" of <iq/>, so we have proper "from" in result

* Fri Jan 11 2002  Jacek Konieczny <jajcus@jajcus.net>
- xmlns="jabber:iq:agent" support

* Fri Jan 11 2002  Jacek Konieczny <jajcus@jajcus.net>
- support for <presence type="probe"/>

* Fri Jan 11 2002  Jacek Konieczny <jajcus@jajcus.net>
---enable-debug for configure

* Fri Jan 11 2002  Jacek Konieczny <jajcus@jajcus.net>
- don't install libxode

* Fri Jan 11 2002  Jacek Konieczny <jajcus@jajcus.net>
- headers cleanup

* Fri Jan 11 2002  Jacek Konieczny <jajcus@jajcus.net>
- header cleanup
- support for pinging and timeout

* Wed Jan 9 2002  Jacek Konieczny <jajcus@jajcus.net>
- better error handling
- memory allocation cleanup

* Wed Jan 9 2002  Jacek Konieczny <jajcus@jajcus.net>
- s/instructions/register_instructions/

* Wed Jan 9 2002  Jacek Konieczny <jajcus@jajcus.net>
- formating of strings in config file (eg. instructions). Minor config file format changes

* Mon Jan 7 2002  Jacek Konieczny <jajcus@jajcus.net>
- use g_lib_main and GIOChannel instead of select() and own FdHandler

* Mon Jan 7 2002  Jacek Konieczny <jajcus@jajcus.net>
- big endian check

* Mon Jan 7 2002  Jacek Konieczny <jajcus@jajcus.net>
- improvements

* Mon Jan 7 2002  Jacek Konieczny <jajcus@jajcus.net>
- basic info

* Mon Jan 7 2002  Jacek Konieczny <jajcus@jajcus.net>
- make it really build only static library

* Mon Jan 7 2002  Jacek Konieczny <jajcus@jajcus.net>
- ./configure script is executed from ../configure

* Mon Jan 7 2002  Jacek Konieczny <jajcus@jajcus.net>
- autoconf/automake/libtool support

* Mon Jan 7 2002  Jacek Konieczny <jajcus@jajcus.net>
- make only static libraries

* Sat Jan 5 2002  Jacek Konieczny <jajcus@jajcus.net>
- search fixed. Now searching using several fields should work.

* Sat Jan 5 2002  Jacek Konieczny <jajcus@jajcus.net>
- fixes in registration/unregitration/change functions

* Fri Jan 4 2002  Jacek Konieczny <jajcus@jajcus.net>
- some work on registration: unregitration, changing user data (not finished)

* Fri Jan 4 2002  Jacek Konieczny <jajcus@jajcus.net>
- debug() macro

* Fri Jan 4 2002  Jacek Konieczny <jajcus@jajcus.net>
- debuging and other messages output using glib. Some debugging cleanups

* Thu Jan 3 2002  Jacek Konieczny <jajcus@jajcus.net>
- fix to charset convertion when sending messages to GG

* Thu Jan 3 2002  Jacek Konieczny <jajcus@jajcus.net>
- "make dep" fixed

* Thu Jan 3 2002  Jacek Konieczny <jajcus@jajcus.net>
- UTF8 support
- search support
- user vCard fetch support

* Thu Jan 3 2002  Jacek Konieczny <jajcus@jajcus.net>
- ignore .deps

* Thu Jan 3 2002  Jacek Konieczny <jajcus@jajcus.net>
- more ignores

* Thu Jan 3 2002  Jacek Konieczny <jajcus@jajcus.net>
- some ignores

* Tue Jan 1 2002  Jacek Konieczny <jajcus@jajcus.net>
- Wreszcie co� dzia�a:
- 	- Rejestracja
- 	- Powiadamianie o obecno�ci w sieci
- 	- Wiadomo�ci, chat

* Mon Dec 31 2001  Jacek Konieczny <jajcus@jajcus.net>
- proper handshake

* Mon Dec 31 2001  Jacek Konieczny <jajcus@jajcus.net>
- Initial revision

* Mon Dec 31 2001  Jacek Konieczny <jajcus@jajcus.net>
- New repository initialized by cvs2svn.
