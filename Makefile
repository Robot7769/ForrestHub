
release-tag:
	@VERSION=$$(cat ForrestHub-app/VERSION) && \
	echo "Releasing version $$VERSION" && \
	git tag -a $$VERSION -m "Release version $$VERSION" && \
	git push origin $$VERSION
