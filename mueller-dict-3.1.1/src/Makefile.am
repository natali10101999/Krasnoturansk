SUBDIRS = scripts
EXTRA_DIST = mueller-abbrev mueller-dict mueller-names mueller-base mueller-geo

check-local:
	@for file in $(EXTRA_DIST); do \
		echo "  \`$$file' verification..."; \
		$(PERL) $(srcdir)/scripts/check-order $$file; \
		$(PERL) $(srcdir)/scripts/check-trans $$file; \
	done
