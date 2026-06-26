.PHONY: release tag help

VERSION := $(shell cat VERSION)

help:
	@echo "Available commands:"
	@echo "  make tag     - Create git tag for current version"
	@echo "  make release - Create GitHub release for current version"

tag:
	git tag -a v$(VERSION) -m "v$(VERSION)"
	git push origin v$(VERSION)

release:
	gh release create v$(VERSION) \
		--title "水利Skills v$(VERSION)" \
		--notes-file CHANGELOG.md
