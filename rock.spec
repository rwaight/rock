%global _rockdir /usr/share/rock
%global _sysconfdir /etc/rocknsm
%global _sbindir /usr/sbin

Name:           rock
Version:        3.0.0
Release:        1

Summary:        Network Security Monitoring collections platform

License:        BSD
URL:            http://rocknsm.io/
Source0:        https://github.com/rocknsm/%{name}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildArch:      noarch

Requires:       ansible >= 2.7.0
Requires:       python-jinja2
Requires:       python-markupsafe
Requires:       pyOpenSSL
Requires:       python-netaddr
Requires:       libselinux-python
Requires:       git
Requires:       crudini

%description
ROCK is a collections platform, in the spirit of Network Security Monitoring.

%prep
%setup -q

%build


%install
rm -rf %{buildroot}
DESTDIR=%{buildroot}

#make directories
mkdir -p %{buildroot}/%{_rockdir}/roles
mkdir -p %{buildroot}/%{_rockdir}/playbooks
mkdir -p %{buildroot}/%{_sbindir}
mkdir -p %{buildroot}/%{_sysconfdir}

# Install ansible files
install -p -m 755 bin/rock %{buildroot}/%{_sbindir}/
install -p -m 755 bin/rock_setup %{buildroot}/%{_sbindir}/
install -p -m 755 bin/deploy_rock.sh %{buildroot}/%{_sbindir}/
install -m 644 etc/hosts.ini %{buildroot}/%{_sysconfdir}/
cp -a roles/. %{buildroot}/%{_rockdir}/roles
cp -a playbooks/. %{buildroot}/%{_rockdir}/playbooks

# make dir and install tests
mkdir -p %{buildroot}/%{_rockdir}/tests
cp -a tests/. %{buildroot}/%{_rockdir}/tests

%files
%doc README.md LICENSE CONTRIBUTING.md
%config %{_rockdir}/playbooks/group_vars/all.yml
%config %{_rockdir}/playbooks/ansible.cfg
%config %{_sysconfdir}/hosts.ini
%ghost %{_sysconfdir}/config.yml
%defattr(0644, root, root, 0755)
%{_rockdir}/playbooks/roles
%{_rockdir}/roles/*
%{_rockdir}/playbooks/*.yml
%{_rockdir}/playbooks/templates/*
%{_rockdir}/tests/*


%attr(0755, root, root) %{_sbindir}/rock
%attr(0755, root, root) %{_sbindir}/rock_setup
%attr(0755, root, root) %{_sbindir}/deploy_rock.sh

%changelog
* Thu May 05 2021 spartan782 <john.hall7688@hotmail.com>
- Remove yq as it is no longer a package
- Update python requirements with python2 purge

* Tue Apr 21 2020 Derek Ditch <derek@rocknsm.io>
- Improves kafka and zookeeper reliability (derek@rocknsm.io)
- Improve multi-node unit testing (derek@rocknsm.io)
- Add diag function to rock command for troubleshooting (koelslaw@gmail.com)
- Improve formating of JSON logs in rock status command (10247070+nstrik159@users.noreply.github.com)
- Adjust the start to update order for Suricata  (#533) (jeff.geiger@gmail.com)
- Add @dcode's fix for multinode . (#532) (jeff.geiger@gmail.com)

* Sat Feb 15 2020 Derek Ditch <derek@rocknsm.io> 2.5.0-2
- Enhances to multinode setup to be more reliable (espeically w/ elasticsearch)
- Fixes startup logic for Zeek
- Improvements to molecule testing framework for multinode testing
- Globally rename bro to zeek to align with upstream
- Migrate to maxmind GeoIP v2 for everything (zeek, suricata, logstash)
- Modularization of Logstash pipeline and ECS 1.4 compatibility

* Thu Aug 22 2019 Derek Ditch <derek@rocknsm.io> 2.5.0-1
- Updated roles to work with ECS pipeline
- Added XFS Quotas  (#473)
- Added Suricata Community ID (#469)
- Cleanups around testing and CI
- Now requires Ansible 2.8
- Cleaned up tasks to be more resilient
- Adding filebeat role to remove duplicate logic.
* Sat Apr 13 2019 Derek Ditch <derek@rocknsm.io> 2.4.2-1
- Change elastic node name to the inventory hostname Fixes #447

* Thu Apr 11 2019 Derek Ditch <derek@rocknsm.io> 2.4.1-1
- Fix Kibana index pattern for Elastic7 calc fields
-

* Thu Apr 11 2019 Derek Ditch <derek@rocknsm.io> 2.4.0-1
- Upgrade Elastic Stack to 7.x
- Add molecule test harness with full yaml and ansible linting
- Text-based User Interface to configure, deploy, and manage node(s)
- Added ansible conveniences like tags to better target deployments
- Upgrade to Java 11 for Elastic, Logstash, Zookeeper, and Kafka
- Add logging of Ansible plays
- Remove remaining snort leftovers
- Refactor Elasticsearch for rolling restarts
- Adjust roles to allow remote deployment

* Fri Feb 22 2019 Derek Ditch <derek@rocknsm.io> 2.3.0-3
- Remove suricata-update from packages. It's in suricata now.

* Fri Feb 22 2019 Derek Ditch <derek@rocknsm.io> 2.3.0-2
- Bump release to fix version conflict

* Fri Feb 22 2019 Derek Ditch <derek@rocknsm.io> 2.3.0-1
- New: Add ability to do multi-host deployment of sensor + data tiers (#339, bndabbs@gmail.com)
- New: Integrate Docket into Kibana by default (derek@rocknsm.io)
- New: Improvements and additional Kibana dashboards (spartan782)
- Fixes: issue with Bro failing when monitor interface is down (#343, bndabbs@gmail.com)
- Fixes: issue with services starting that shouldn’t (#346, therealneu5ron@gmail.com)
- Fixes: race condition on loading dashboards into Kibana (#356, derek@rocknsm.io)
- Fixes: configuration for Docket allowing serving from non-root URI (#361, derek@rocknsm.io)
- Change: zeek log retention value to one week rather than forever (#345, sean.cochran@gmail.com)
- Change: Greatly improve documentation  (#338, sean.cochran@gmail.com)
- Change: Reorganize README (#308, bradford.dabbs@elastic.co)
- Change: Move ECS to rock-dashboards repo (#305, derek@rocknsm.io)
- Change: Move RockNSM install paths to filesystem heirarchy standard locations (#344, bndabbs@gmail.com)

* Fri Jan 25 2019 Bradford Dabbs <brad@dabbs.io> 2.3.0-1
- Update file paths to match new structure
- Bump minimum Ansible version to 2.7

* Tue Oct 30 2018 Derek Ditch <derek@rocknsm.io> 2.2.0-2
- Fixed issue with missing GPG keys (derek@rocknsm.io)
- Update logrotate configuration (derek@rocknsm.io)

* Fri Oct 26 2018 Derek Ditch <derek@rocknsm.io> 2.2.0-1
- Added support for Elastic Stack 6.4 (derek@rocknsm.io>
- Added initial support for Elastic Common Schema in Tech Preview (derek@rocknsm.io)
- Updated vars for lighttpd tests (derek@rocknsm.io)
- Removed cruft perl packages no longer needed for pulledpork.
  (derek@rocknsm.io)
- Merges in Lighttpd config and several bug fixes. (#329)
  (dcode@rocknsm.io)
- Enable/Install suricata update by default (dcode@rocknsm.io)
- Adjust 'when' for the cron job and rename local source.
  (jeff.geiger@gmail.com)
- Remove pulledpork. (jeff.geiger@gmail.com)
- Add configuration for suricata-update. (jeff.geiger@gmail.com)
- Add closing tag (bradford.dabbs@elastic.co)
- Add ISO download links (bradford.dabbs@elastic.co)
- Replace logo with latest version (bradford.dabbs@elastic.co)
- Reorganize README (bradford.dabbs@elastic.co)
- Move ECS to rock-dashboards repo (derek@rocknsm.io)

* Tue Aug 21 2018 Derek Ditch <derek@rocknsm.io> 2.1.0-2
- Move ECS to rock-dashboards repo

* Tue Aug 21 2018 Derek Ditch <derek@rocknsm.io> 2.1.0-1
- Introducing Docket, a REST API and web UI to query multiple stenographer instances
- Added Suricata-Update to manage Suricata signatures
- Added GPG signing of packages and repo metadata
- Added functional tests using [testinfra](https://testinfra.readthedocs.io/en/latest/)
- Initial support of [Elastic Common Schema](https://github.com/elastic/ecs)
- Includes full Elastic (with permission) stack including features formerly known as X-Pack
- Elastic stack is updated to 6.x
- Elastic dashboards, mappings, and Logstash config moved to module-like construct
- Suricata is updated to 4.x
- Bro is updated to 2.5.4
- Deprecated Snort
- Deprecated Pulled Pork

* Thu Jun 08 2017 spartan782 <john.hall7688@hotmail.com> 2.0.5-1
- Tito files added.
- rock.spec added.
- sign_rpm.sh added.
