spec := teams-for-linux.spec
source_url := https://github.com/IsmaelMartinez/teams-for-linux/releases/download/v2.18.1/teams-for-linux-2.18.1.x86_64.rpm

.PHONY: srpm
srpm:
	curl --fail --location --output teams-for-linux-2.18.1.x86_64.rpm $(source_url)
	rpmbuild -bs --define "_sourcedir $(CURDIR)" --define "_srcrpmdir $(outdir)" $(spec)
