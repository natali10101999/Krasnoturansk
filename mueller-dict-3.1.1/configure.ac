dnl Process this file with autoconf to produce a configure script.

AC_INIT([mueller-dict], [3.1.1], [smersh@users.sourceforge.net])
AC_PREREQ([2.59])
AC_CONFIG_SRCDIR([src/mueller-base])
AM_INIT_AUTOMAKE([1.9.0])
AM_MAINTAINER_MODE

AC_ARG_ENABLE(preformat,
	[AS_HELP_STRING([--enable-preformat],
		[preformat dictionaries before processing])],
	[test "x$enableval" = xyes || test "x$enableval" = xno ||
		AC_MSG_ERROR([--enable-preformat: bad value: $enableval])],
	[enableval=no]
)
AC_MSG_NOTICE([enable preformating: $enableval])
AM_CONDITIONAL(FORMAT, [test "x$enableval" = xyes])

AC_ARG_ENABLE(IPA-unicode,
	[AS_HELP_STRING([--enable-IPA-unicode],
		[convert transcription into the IPA Unicode])],
	[test "x$enableval" = xyes || test "x$enableval" = xno ||
		AC_MSG_ERROR([--enable-IPA-unicode: bad value: $enableval])],
	[enableval=no]
)
AC_MSG_NOTICE([IPA unicode: $enableval])
AM_CONDITIONAL(IPAUNICODE, [test "x$enableval" = xyes])

AC_ARG_ENABLE(compression,
	[AS_HELP_STRING([--disable-compression],
		[do not compress dictionary files])],
	[test "x$enableval" = xyes || test "x$enableval" = xno ||
		AC_MSG_ERROR([--enable-compression: bad value: $enableval])],
	[enableval=yes]
)
AC_MSG_NOTICE(compress dictionaries: $enableval)
AM_CONDITIONAL(COMPRESS, [test "x$enableval" = xyes])

AC_ARG_ENABLE(locale,
	[AS_HELP_STRING([--enable-locale=<locale>],
		[locale used for sorting indexes [en_US.utf-8]])],
	[case "$enableval" in
		yes|no) AC_MSG_ERROR([--enable-locale: must be valid locale name]);;
		*) LOCALE="$enableval";;
	esac
	charset_form_locale=`echo "$LOCALE" | sed -n '/.\./ s/^.*\.//p'`]
)
test -z "$LOCALE" && LOCALE=en_US.utf-8
AC_SUBST(LOCALE)
AC_MSG_NOTICE([locale: $LOCALE])

AM_CONDITIONAL([UTF8_FLAG], [echo $LOCALE | grep -i '\.utf-\?8$' >/dev/null])

AC_ARG_ENABLE(charset,
	[AS_HELP_STRING([--enable-charset=<charset>],
		[output charset [UTF-8]])],
	[case "$enableval" in
		yes|no) AC_MSG_ERROR([--enable-charset: must be valid charset name]);;
		*) CHARSET="$enableval";;
	esac]
)
if test -z "$CHARSET"; then
	if test -n "$charset_form_locale"; then
		CHARSET="$charset_form_locale"
	else
		CHARSET=UTF-8
	fi
fi
AC_SUBST(CHARSET)
AC_MSG_NOTICE([charset: $CHARSET])

dnl Checks for programs.
MISSING="${SHELL} \$(top_srcdir)/missing"
AC_CHECK_PROG(PERL, perl, perl, [${MISSING} perl])
AC_CHECK_PROG(DICTFMT, dictfmt, dictfmt, [${MISSING} dictfmt])
AC_CHECK_PROG(DICTZIP, dictzip, dictzip, [${MISSING} dictzip])

AC_CONFIG_FILES([Makefile dict/Makefile src/Makefile src/scripts/Makefile
	site/Makefile site/cgi-bin/Makefile site/images/Makefile
	site/scripts/Makefile])
AC_OUTPUT
