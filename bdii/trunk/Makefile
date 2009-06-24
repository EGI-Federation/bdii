#!/usr/bin/make -f

metadata=config
name:=$(shell grep NAME ${metadata} | sed 's/^[^:]*: //' )
version:=$(shell grep VERSION ${metadata} | sed 's/^[^:]*: //' )
release:=$(shell grep RELEASE ${metadata} | sed 's/^[^:]*: //' )
prefix:=$(shell grep PREFIX ${metadata} | sed 's/^[^:]*: //' )
packager:=$(shell grep PACKAGER ${metadata} | sed 's/^[^:]*: //' )
description:=$(shell grep DESCRIPTION ${metadata} | sed 's/^[^:]*: //' )
group:=$(shell grep GROUP ${metadata} | sed 's/^[^:]*: //' )
topdir:=$(shell rpm --eval %_topdir 2>/dev/null || echo ${pwd}/scratch )
debian=${topdir}/BUILD/${name}-${version}/DEBIAN

.PHONY: 

all: 

install: 
	@mkdir -p $(prefix)/opt/bdii/bin/
	@mkdir -p $(prefix)/opt/bdii/etc
	@mkdir -p $(prefix)/opt/glite/etc/gip/ldif
	@mkdir -p $(prefix)/opt/glite/etc/gip/provider
	@mkdir -p $(prefix)/opt/glite/etc/gip/plugin
	@mkdir -p $(prefix)/etc/init.d/
	@mkdir -p $(prefix)/etc/logrotate.d/	
	@mkdir -p $(prefix)/etc/cron.d/	
	@mkdir -p $(prefix)/var/bdii/db/stats
	@mkdir -p $(prefix)/var/bdii/db/glue2
	@mkdir -p $(prefix)/var/bdii/archive	
	@mkdir -p $(prefix)/var/log/bdii

	@install -m 0755 etc/init.d/bdii      $(prefix)etc/init.d
	@install -m 0755 bin/bdii-update      $(prefix)opt/bdii/bin
	@install -m 0755 bin/bdii-proxy       $(prefix)opt/bdii/bin
	@install -m 0644 etc/bdii.conf	      $(prefix)opt/bdii/etc/
	@install -m 0644 etc/BDII.schema     $(prefix)opt/bdii/etc/
	@install -m 0644 etc/bdii-slapd.conf  $(prefix)opt/bdii/etc/
	@install -m 0644 etc/DB_CONFIG        $(prefix)opt/bdii/etc/
	@install -m 0644 etc/default.ldif     $(prefix)opt/glite/etc/gip/ldif
	@install -m 0644 etc/logrotate.d/bdii $(prefix)etc/logrotate.d
	@install -m 0644 etc/cron.d/bdii-proxy $(prefix)etc/cron.d

clean:
	@rm -f *~ *.deb
	@rm -rf scratch
dist:
	@mkdir -p  ${topdir}/SOURCES/
	@tar --gzip --exclude ".svn" --exclude "build" --exclude "*.deb" \
	-cf ${topdir}/SOURCES/${name}-${version}.src.tgz *

rpm: dist
	@mkdir -p  ${topdir}/RPMS/noarch
	@mkdir -p  ${topdir}/SRPMS/
	@mkdir -p  ${topdir}/SPECS/
	@mkdir -p  ${topdir}/BUILD/
	@rpmbuild -ba --define="_topdir ${topdir}" ${name}.spec

deb: dist
	@mkdir -p ${debian}
	@tar -zxf ${topdir}/SOURCES/${name}-${version}.src.tgz -C ${topdir}/BUILD/${name}-${version} 
	@rm -f ${topdir}/BUILD/${name}-${version}/config 
	@rm -f ${topdir}/BUILD/${name}-${version}/Makefile 
	@rm -f ${topdir}/BUILD/${name}-${version}/*.spec 
	@rm -f ${topdir}/BUILD/${name}-${version}/INSTALLED_FILES
	@sed -i "s/Package:.*/Package: ${name}/" ${debian}/control
	@sed -i "s/Version:.*/Version: ${version}/" ${debian}/control
	@sed -i "s/Maintainer:.*/Maintainer: ${packager}/" ${debian}/control
	@sed -i "s/Description:.*/Description: ${description}/" ${debian}/control
	@sed -i "s/Section:.*/Section: ${group}/" ${debian}/control

	@dpkg -ba ${topdir}/BUILD/${name}-${version} ${name}-${version}.deb