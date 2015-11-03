from solar import events as evapi
from solar.core.resource import virtual_resource as vr
from solar.interfaces.db import get_db

import yaml

db = get_db()

STORAGE = {'objects_ceph': True,
           'osd_pool_size': 2,
           'pg_num': 128}

KEYSTONE = {'admin_token': 'abcde'}


NETWORK_SCHEMA = {
    'endpoints': {'eth1': {'IP': ['10.0.0.3/24']}},
    'roles': {'ceph/replication': 'eth1',
              'ceph/public': 'eth1'}
    }

NETWORK_METADATA = yaml.load("""
    solar-dev1:
      uid: '1'
      fqdn: solar-dev1
      network_roles:
        ceph/public: 10.0.0.3
        ceph/replication: 10.0.0.3
      node_roles:
        - ceph-mon
      name: solar-dev1

    """)


def deploy():
    db.clear()
    resources = vr.create('nodes', 'templates/nodes.yaml', {'count': 2})
    first_node, second_node = [x for x in resources if x.name.startswith('solar-dev')]

    library2 = vr.create('library2', 'resources/fuel_library',
        {'temp_directory': '/tmp/solar',
       'puppet_modules': '/etc/fuel/modules',
       'git':{'branch': 'master', 'repository': 'https://github.com/stackforge/fuel-library'},
       'librarian_puppet_simple': 'true'})[0]
    
    ceph_compute = vr.create('ceph_compute1', 'resources/ceph_compute',
        {'storage': STORAGE,
         'keystone': KEYSTONE,
         'network_scheme': NETWORK_SCHEMA,
         'ceph_monitor_nodes': NETWORK_METADATA,
         'ceph_primary_monitor_node': NETWORK_METADATA,
         'role': 'compute',
         })[0]

    second_node.connect(ceph_compute, {}) 

    library2.connect(ceph_compute, {'puppet_modules': 'puppet_modules'})

    evapi.add_dep(second_node.name, ceph_compute.name, actions=('run',))


if __name__ == '__main__':
    deploy()
