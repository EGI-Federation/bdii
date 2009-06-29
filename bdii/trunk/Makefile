include CONFIG
PWD=$(shell pwd)
control=scratch/${NAME}-${VERSION}/debian/control
SCRATCH=${PWD}/scratch
DATE=$(shell date "+%a, %d %b %Y %T %z")
topdir:=$(shell rpm --eval %_topdir 2>/dev/null || ${SCRATCH} )

default: 
	@echo "Nothing to do"

clean:
	rm -f *~
	rm -rf ${SCRATCH}

sdist:
	@mkdir -p  ${SCRATCH}/SOURCES/
	tar --gzip --exclude ".svn" --exclude "scratch" -cf ${SCRATCH}/${NAME}-${VERSION}.src.tgz *

deb: sdist
	@mkdir -p ${SCRATCH}/${NAME}-${VERSION}/
	tar -zx -C ${SCRATCH}/${NAME}-${VERSION}/ -f \
	${SCRATCH}/${NAME}-${VERSION}.src.tgz
	echo "${NAME} (${VERSION}-${RELEASE}) dummy;" > ${SCRATCH}/${NAME}-${VERSION}/debian/changelog
	echo "  * No data" >>  ${SCRATCH}/${NAME}-${VERSION}/debian/changelog
	echo " -- ${PACKAGER}  ${DATE}" >> ${SCRATCH}/${NAME}-${VERSION}/debian/changelog

	@sed -i "s/Package:.*/Package: ${NAME}/" ${control}
	@sed -i "s/Source:.*/Source: ${NAME}/" ${control}
	@sed -i "s/Version:.*/Version: ${VERSION}/" ${control}
	@sed -i "s/Maintainer:.*/Maintainer: ${PACKAGER}/" ${control}
	@sed -i "s/Description:.*/Description: ${DESCRIPTION}/" ${control}
	@sed -i "s/Section:.*/Section: ${GROUP}/" ${control}
	cd ${SCRATCH}/${NAME}-${VERSION}; dpkg-buildpackage -us -uc; cd ${PWD}

rpm: sdist
	mkdir -p ${topdir}/BUILD
	mkdir -p ${topdir}/RPMS
	mkdir -p ${topdir}/SRPMS
	mkdir -p ${topdir}/SOURCES
	mkdir -p ${topdir}/SPECS
	cp ${SCRATCH}/${NAME}-${VERSION}.src.tgz ${topdir}/SOURCES
	rpmbuild --define "_topdir ${topdir}" -ba ${NAME}.spec
