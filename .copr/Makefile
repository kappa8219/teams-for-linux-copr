spec := teams-for-linux.spec
version := 2.25.0
source := teams-for-linux-$(version).x86_64.rpm
source_url := https://github.com/IsmaelMartinez/teams-for-linux/releases/download/v$(version)/$(source)

.PHONY: srpm
srpm:
	curl --fail --location --output $(source) $(source_url)
	rpmbuild -bs --define "_sourcedir $(CURDIR)" --define "_srcrpmdir $(outdir)" $(spec)
