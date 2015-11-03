$resource = hiera($::resource_name)

$stores                = $resource['input']['stores']['value']
$default_store         = $resource['input']['default_store']['value']
$rbd_store_ceph_conf   = $resource['input']['rbd_store_ceph_conf']['value']
$rbd_store_user        = $resource['input']['rbd_store_user']['value']
$rbd_store_pool        = $resource['input']['rbd_store_pool']['value']
$rbd_store_chunk_size  = $resource['input']['rbd_store_chunk_size']['value']
$rados_connect_timeout = $resource['input']['rados_connect_timeout']['value']


glance_api_config {
  'glance_store/stores':                 value => $stores;
  'glance_store/default_store':          value => $default_store;
  'glance_store/rbd_store_ceph_conf':    value => $rbd_store_ceph_conf;
  'glance_store/rbd_store_user':         value => $rbd_store_user;
  'glance_store/rbd_store_pool':         value => $rbd_store_pool;
  'glance_store/rbd_store_chunk_size':   value => $rbd_store_chunk_size;
  'glance_store/rados_connect_timeout':  value => $rados_connect_timeout;
} ~>

service {'glance-api': }

package { 'python-ceph':
  ensure => latest,
}
