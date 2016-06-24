from resource_management.libraries.script.script import Script

# server configurations
config = Script.get_config()

datatorrent_install_dir = config['configurations']['datatorrent-rts-config']['datatorrent.install_dir']
datatorrent_username = config['configurations']['datatorrent-rts-config']['datatorrent.username']
datatorrent_groupname = config['configurations']['datatorrent-rts-config']['datatorrent.groupname']
