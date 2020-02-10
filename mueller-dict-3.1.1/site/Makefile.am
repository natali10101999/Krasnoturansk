SUBDIRS = scripts cgi-bin images
TARGETS = index-koi8r.html index-windows1251.html index-iso88595.html \
	index-maccyrillic.html index-cp866.html index-utf8.html

CONVERT = $(PERL) $(srcdir)/scripts/convert
CONVERT_FLAGS =

all-local: $(TARGETS)

index-koi8r.html: $(srcdir)/index.html.ru
	rm -f $(TARGETS); \
	$(CONVERT) $(CONVERT_FLAGS) $(srcdir)/index.html.ru

index-windows1251.html index-iso88595.html index-maccyrillic.html \
index-cp866.html index-utf8.html: index-koi8r.html
	@if test -f $@; then :; else \
		rm -f index-koi8r.html; \
		$(MAKE) $(AM_MAKEFLAGS) index-koi8r.html; \
	fi

EXTRA_DIST = $(TARGETS) index.html script.js style.css index.html.ru \
	robots.txt  pad_file.xml
MAINTAINERCLEANFILES = index-*.html
