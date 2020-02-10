DESC = Mueller English-Russian Dictionary
URL = http://mueller-dict.sourceforge.net/
SRC_CHARSET = utf-8
dictdir = $(datadir)/dict
SRC = $(top_srcdir)/src
SUFFIXES = .index .dict .dict.dz
VPATH =

# substitutions from `configure'
#LOCALE = en_US.utf-8
#CHARSET = utf-8

DICTFMT_FLAGS = --headword-separator \; --break-headwords --columns=0 -c5 -u $(URL)

if UTF8_FLAG
DICTFMT_FLAGS += --utf8
else
DICTFMT_FLAGS += --locale=$(LOCALE)
endif

DICTZIP_FLAGS = -k

if FORMAT
PREFMT = $(PERL) $(SRC)/scripts/prefmt -q
else
PREFMT = cat
endif

CONV = $(PERL) $(SRC)/scripts/conv
CONV_FLAGS = -f $(SRC_CHARSET) -t $(CHARSET)
if IPAUNICODE
CONV_FLAGS += -p
endif

INDEX_FILES = mueller-dict.index mueller-abbrev.index \
	mueller-geo.index mueller-names.index mueller-base.index
DICT_FILES = mueller-dict.dict mueller-abbrev.dict \
	mueller-geo.dict mueller-names.dict mueller-base.dict
DZ_FILES = mueller-dict.dict.dz mueller-abbrev.dict.dz \
	mueller-geo.dict.dz mueller-names.dict.dz mueller-base.dict.dz

if COMPRESS
dict_DATA = $(DZ_FILES)
CLEANFILES = *.dict
.SECONDARY: $(DICT_FILES)
else
CLEANFILES = *.dz
dict_DATA = $(DICT_FILES)
endif

dict_DATA += $(INDEX_FILES)
EXTRA_DIST = $(dict_DATA)

mueller-abbrev.dict: $(SRC)/mueller-abbrev
	$(PREFMT) <$(SRC)/mueller-abbrev | $(CONV) $(CONV_FLAGS) | \
	$(DICTFMT) $(DICTFMT_FLAGS) -s "$(DESC) (abbreviations)" mueller-abbrev

mueller-base.dict: $(SRC)/mueller-base
	$(PREFMT) <$(SRC)/mueller-base | $(CONV) $(CONV_FLAGS) | \
	$(DICTFMT) $(DICTFMT_FLAGS) -s "$(DESC) (base)" mueller-base

mueller-dict.dict: $(SRC)/mueller-dict
	$(PREFMT) <$(SRC)/mueller-dict | $(CONV) $(CONV_FLAGS) | \
	$(DICTFMT) $(DICTFMT_FLAGS) -s "$(DESC) (introduction)" mueller-dict

mueller-geo.dict: $(SRC)/mueller-geo
	$(PREFMT) <$(SRC)/mueller-geo | $(CONV) $(CONV_FLAGS) | \
	$(DICTFMT) $(DICTFMT_FLAGS) -s "$(DESC) (place-names)" mueller-geo

mueller-names.dict: $(SRC)/mueller-names
	$(PREFMT) <$(SRC)/mueller-names | $(CONV) $(CONV_FLAGS) | \
	$(DICTFMT) $(DICTFMT_FLAGS) -s "$(DESC) (personal names)" mueller-names

.dict.index:
	@if test -f $@; then :; else \
		rm -f $<; \
		$(MAKE) $(AM_MAKEFLAGS) $<; \
	fi

.dict.dict.dz:
	$(DICTZIP) $(DICTZIP_FLAGS) $<

DISTCLEANFILES = *.index *.dict *.dz
