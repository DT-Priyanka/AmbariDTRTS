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
from resource_management import Script

class DtRtsClient(Script):
  def install(self, env):
    import params
    Execute('echo Installing packages > /tmp/mylogs.txt')
    env.set_params(params)
    self.install_datatorrent_repo()
    self.install_packages(env)
    self.configure(env)

  def configure(self, env, upgrade_type=None):
    import params
    env.set_params(params)

  def stop(self, env):
    print 'Stop the service'

  def start(self, env):
    import params
    env.set_params(params)
    print 'Start the service'

  def status(self, env):
    print 'Status of the service'

  def install_datatorrent_repo(self):
      import os
      distribution = platform.linux_distribution()[0].lower()
      if distribution in ['centos', 'redhat'] and not os.path.exists('/etc/yum.repos.d/datatorrent.repo'):
          Execute('curl -o /etc/yum.repos.d/datatorrent.repo **changethis https://repos.fedorapeople.org/repos/dchen/apache-maven/datatorrent.repo')
      elif distribution in ['Ubuntu'] and not os.path.exists('/etc/apt/sources.list.d/datatorrent.list'):
          Execute('echo "deb https://www.datatorrent.com/downloads/repos/apt/ /" > /etc/apt/sources.list.d/datatorrent.list')
          Execute('wget -O - https://www.datatorrent.com/downloads/repos/apt/keyFile | apt-key add -')
          Execute('apt-get update')

if __name__ == "__main__":
  DtRtsClient().execute()
