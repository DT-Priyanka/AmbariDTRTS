from resource_management.libraries.script.script import Script
from resource_management.libraries.resources.hdfs_resource import HdfsResource
from resource_management.libraries.functions import conf_select
from resource_management.libraries.functions import hdp_select
from resource_management.libraries.functions import get_kinit_path
from resource_management.libraries.functions.default import default

# server configurations
config = Script.get_config()

# hadoop default parameters
hadoop_conf_dir = conf_select.get_hadoop_conf_dir()
hadoop_bin_dir = hdp_select.get_hadoop_dir("bin")
hadoop_home = '/usr'

datatorrent_install_dir = config['configurations']['datatorrent-rts-config']['datatorrent.install_dir']
datatorrent_username = config['configurations']['datatorrent-rts-config']['datatorrent.username']
datatorrent_groupname = config['configurations']['datatorrent-rts-config']['datatorrent.groupname']
hdfs_user = config['configurations']['hadoop-env']['hdfs_user']
hdfs_principal_name = config['configurations']['hadoop-env']['hdfs_principal_name']
hdfs_user_keytab = config['configurations']['hadoop-env']['hdfs_user_keytab']
security_enabled = config['configurations']['cluster-env']['security_enabled']
kinit_path_local = get_kinit_path(default('/configurations/kerberos-env/executable_search_paths', None))

hdfs_site = config['configurations']['hdfs-site']
default_fs = config['configurations']['core-site']['fs.defaultFS']

dfs_type = default("/commandParams/dfs_type", "")

import functools
#create partial functions with common arguments for every HdfsResource call
#to create hdfs directory we need to call params.HdfsResource in code
HdfsResource = functools.partial(
  HdfsResource,
  user=hdfs_user,
  security_enabled = security_enabled,
  keytab = hdfs_user_keytab,
  kinit_path_local = kinit_path_local,
  hadoop_bin_dir = hadoop_bin_dir,
  hadoop_conf_dir = hadoop_conf_dir,
  principal_name = hdfs_principal_name,
  hdfs_site = hdfs_site,
  default_fs = default_fs,
  dfs_type = dfs_type
 )
