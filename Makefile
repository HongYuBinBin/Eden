# Build the site into _site/.
#   make html   build every page and copy images, code excerpts and assets
#   make clean  remove the build output
# Pages are content/**/*.typ (paths containing "_" are skipped). Other files under content/ are copied as-is.

TYP_FILES := $(shell find content -name '*.typ' -not -path '*/_*')
HTML_FILES := $(patsubst content/%.typ,_site/%.html,$(TYP_FILES))
STATIC_FILES := $(shell find content -type f -not -name '*.typ' -not -path '*/_*')
STATIC_OUT := $(patsubst content/%,_site/%,$(STATIC_FILES))

html: $(HTML_FILES) $(STATIC_OUT) assets

_site/%.html: content/%.typ config.typ lib/review.typ
	@mkdir -p $(@D)
	typst compile --root . --features html --format html $< $@

_site/%: content/%
	@mkdir -p $(@D)
	cp $< $@

assets:
	@mkdir -p _site/assets
	@cp -r assets/* _site/assets/

clean:
	rm -rf _site

.PHONY: html clean assets
