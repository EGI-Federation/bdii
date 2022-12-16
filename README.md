# BDII

Documentation: [bdii.readthedocs.io](http://bdii.readthedocs.io).

## Function

The Berkeley Database Information Index (BDII) consists of two or more standard
LDAP databases that are populated by an update process. Port forwarding is used
to enable one or more databases to serve data while one database is being
refreshed. The databases are refreshed cyclically. Any incoming connection is
forwarded to the most recently updated database, while old connections are
allowed to linger until it is the turn of their database to be refreshed and
restarted. The update process obtains LDIF from either doing an `ldapsearch` on
LDAP URLs or by running a local script (given by a URL with "file" protocol)
that generates LDIF. The LDIF is then inserted into the LDAP database. Options
exist to update the list of LDAP URLs from a web page and to use an LDIF file
from a web page to modify the data before it is inserted into the database.

## Cache use

Whenever a remote server is contacted and the `ldapsearch` command times out the
update process tries to find an (old) cached entry in the `/var/cache/`
directory. If no entry is found a message is printed to the logfile.

_Attention!_ If the remote host cannot be contacted due to a connection problem
no cached entry is taken. No message is printed to the logfile.

## Compressed Content Exchange Mechanism (CCEM)

The Compressed Content Exchange Mechanism is intended to speed up the gathering
of information in case of a `ldapsearch` to another BDII instance. The update
process first tries to find the entry containing the compressed content of the
queried instance and subsequently adds the information to its upcoming database.
If the CCEM fails the normal procedure as described in the previous paragraph is
executed. The CCEM function is enabled by default in version `>= 3.9.1`. To
disable, add the following to your `bdii.conf`:

```shell
BDII_CCEM=no
```

## BDII Status Information Mechanism (BSIM)

The BDII Status Information Mechanism is intended to allow better monitoring
possibilities, spotting of upraising problems and resulting error prevention.
It adds status information about the BDII instance into the `o=infosys` root
containing metrics like the number of entries added in the last cycle, the time
to do so, etc. The description of those metrics can be found in the
`etc/BDII.schema` file.

## Installing from source

```shell
$ make install
```

- Build dependencies: None
- Runtime dependencies: openldap, python3

## Installing from packages

### On RHEL-based systems

For RHEL-based systems, it's possible to install packages from two sources:

- [EGI UMD packages](https://go.egi.eu/umd) build from this repository, and
  tested to work with other components part of the Unified Middleware
  Distribution.
- [Fedora and EPEL packages](https://packages.fedoraproject.org/search?query=bdii)
  maintained by Mattias Ellert.

### On debian

[Official debian packages](https://packages.debian.org/search?keywords=bdii)
are maintained by Mattias Ellert.

## Building packages

### Building a RPM

The required build dependencies are:

- rpm-build
- make
- rsync
- systemd-rpm-macros, for RHEL >= 8

```shell
# Checkout tag to be packaged
$ git clone https://github.com/EGI-Federation/bdii.git
$ cd bdii
$ git checkout X.X.X
# Building in a container
$ docker run --rm -v $(pwd):/source -it quay.io/centos/centos:7
[root@2fd110169c55 /]# yum install -y rpm-build make rsync
[root@2fd110169c55 /]# cd /source && make rpm
```

The RPM will be available into the `build/RPMS` directory.

### Building a deb

Debian build files maintained by Mattias Ellert are available in the
[Debian Salsa GitLab](https://salsa.debian.org/ellert/bdii/).

## Preparing a release

- Prepare a changelog from the last version, including contributors' names
- Prepare a PR with
  - Updating version and changelog in `CHANGELOG` and `bdii.spec`
  - Updating `codemeta.json`, if needed
- Once the PR has been merged tag and release a new version in GitHub
  - Packages will be built using GitHub Actions and attached to the release page

## History

This work started under the EGEE project, and was hosted and maintained for a
long time by CERN. This is now hosted here on GitHub, maintained by the BDII
community with support of members of the EGI Federation.
