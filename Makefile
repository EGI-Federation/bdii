NAME=$(shell grep Name: *.spec | sed 's/^[^:]*:[^a-zA-Z]*//')
VERSION=$(shell grep Version: *.spec | sed 's/^[^:]*:[^0-9]*//')
RELEASE=$(shell grep Release: *.spec | cut -d"%" -f1 | sed 's/^[^:]*:[^0-9]*//')
build=$(shell pwd)/build
dist=$(shell rpm --eval '%dist')
init_dir=$(shell rpm --eval '%{_initrddir}' || echo '/etc/init.d/')

default:
	@echo "Nothing to do"

install:
	@echo installing ...
	@mkdir -p $(prefix)/usr/sbin/
	@mkdir -p $(prefix)/run/bdii/
	@mkdir -p $(prefix)/var/lib/bdii/gip/ldif/
	@mkdir -p $(prefix)/var/lib/bdii/gip/provider/
	@mkdir -p $(prefix)/var/lib/bdii/gip/plugin/
	@mkdir -p $(prefix)/etc/bdii/
	@mkdir -p $(prefix)/etc/sysconfig/
	@mkdir -p $(prefix)$(init_dir)/
	@mkdir -p $(prefix)/etc/logrotate.d/
	@mkdir -p $(prefix)/var/log/bdii/
	@mkdir -p $(prefix)/usr/share/doc/bdii/
	@mkdir -p $(prefix)/usr/share/man/man1

	@install -m 0755 etc/init.d/bdii $(prefix)/$(init_dir)/
	@install -m 0644 etc/sysconfig/bdii $(prefix)/etc/sysconfig/
	@install -m 0755 bin/bdii-update $(prefix)/usr/sbin/
	@install -m 0644 etc/bdii.conf $(prefix)/etc/bdii/
	@install -m 0644 etc/BDII.schema $(prefix)/etc/bdii/
	@install -m 0640 etc/bdii-slapd.conf $(prefix)/etc/bdii/
	@install -m 0640 etc/bdii-top-slapd.conf $(prefix)/etc/bdii/
	@install -m 0644 etc/DB_CONFIG $(prefix)/etc/bdii/
	@install -m 0644 etc/DB_CONFIG_top $(prefix)/etc/bdii/
	@install -m 0644 etc/default.ldif $(prefix)/var/lib/bdii/gip/ldif/
	@install -m 0644 etc/logrotate.d/bdii $(prefix)/etc/logrotate.d
	@install -m 0644 man/bdii-update.1 $(prefix)/usr/share/man/man1/
	@install -m 0644 README.md $(prefix)/usr/share/doc/bdii/
	@install -m 0644 AUTHORS.md $(prefix)/usr/share/doc/bdii/
	@install -m 0644 COPYRIGHT $(prefix)/usr/share/doc/bdii/
	@install -m 0644 LICENSE.txt $(prefix)/usr/share/doc/bdii/

dist:
	@mkdir -p $(build)/$(NAME)-$(VERSION)/
	rsync -HaS --exclude ".git" --exclude "$(build)" * $(build)/$(NAME)-$(VERSION)/
	cd $(build); tar --gzip -cf $(NAME)-$(VERSION).tar.gz $(NAME)-$(VERSION)/; cd -

sources: dist
	cp $(build)/$(NAME)-$(VERSION).tar.gz .

prepare: dist
	@mkdir -p $(build)/RPMS/noarch
	@mkdir -p $(build)/SRPMS/
	@mkdir -p $(build)/SPECS/
	@mkdir -p $(build)/SOURCES/
	@mkdir -p $(build)/BUILD/
	cp $(build)/$(NAME)-$(VERSION).tar.gz $(build)/SOURCES
	cp $(NAME).spec $(build)/SPECS

srpm: prepare
	rpmbuild -bs --define="dist $(dist)" --define="_topdir $(build)" $(build)/SPECS/$(NAME).spec

rpm: srpm
	rpmbuild --rebuild --define="dist $(dist)" --define="_topdir $(build)" $(build)/SRPMS/$(NAME)-$(VERSION)-$(RELEASE)$(dist).src.rpm

clean:
	rm -f *~ $(NAME)-$(VERSION).tar.gz
	rm -rf $(build)

.PHONY: dist srpm rpm sources clean
