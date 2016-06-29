"""
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Ambari Agent

"""

import sys
import os
import logging
from resource_management import *
from resource_management.libraries.functions.check_process_status import check_process_status
from resource_management.libraries.resources.hdfs_resource import HdfsResource
from resource_management.core.resources.service import Service

class DtRtsClient(Script):
  def install(self, env):
    import params
    env.set_params(params)
    self.install_datatorrent_repo()
    self.install_packages(env)
    self.add_hdfs_folder(env)

  def configure(self, env, upgrade_type=None):
    import params
    env.set_params(params)

  def stop(self, env):
    import params
    env.set_params(params)
    Service('dtgateway', action='stop')

  def start(self, env):
    import params
    env.set_params(params)
    Service('dtgateway', action='start')

  def status(self, env):
    check_process_status('/var/run/datatorrent/dtgateway.pid')

  def install_datatorrent_repo(self):
      import os
      import platform
      distribution = platform.linux_distribution()[0].lower()
      if distribution.lower() in ['centos', 'redhat'] and not os.path.exists('/etc/yum.repos.d/datatorrent.repo'):
          Execute('curl -o /etc/yum.repos.d/datatorrent.repo https://www.datatorrent.com/downloads/repos/yum/repo/datatorrent-rts.repo')
          Execute('curl -sO https://www.datatorrent.com/downloads/repos/apt/keyFile')
          Execute('rpm --import keyFile')
      elif distribution.lower() in ['ubuntu'] and not os.path.exists('/etc/apt/sources.list.d/datatorrent.list'):
          Execute('echo "deb https://www.datatorrent.com/downloads/repos/apt/ /" > /etc/apt/sources.list.d/datatorrent.list')
          Execute('wget -O - https://www.datatorrent.com/downloads/repos/apt/keyFile | apt-key add -')
          Execute('apt-get update')

  def add_hdfs_folder(self, env):
      import params
      import os
      env.set_params(params)
      homeDir = '/user/' + params.datatorrent_username
      params.HdfsResource(homeDir,
                        type="directory",
                        action="create_on_execute",
                        owner=params.datatorrent_username,
                        group=params.datatorrent_groupname,
                        mode=0755,
                        recursive_chown=True,
                        recursive_chmod=True
                        )

if __name__ == "__main__":
  DtRtsClient().execute()
