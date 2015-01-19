#!/usr/bin/python


def es_plugin(module, name, version, state='present', backup=False):
	changed = False
	reasons = []

	plugin_path = '/usr/share/elasticsearch/plugins/{name}'.format(name=name)
	plugin_version_path = '/usr/share/elasticsearch/plugins/{name}/elasticsearch-{name}-{version}.jar'.format(name=name, version=version)
	manager_path = '/usr/share/elasticsearch/bin/plugin'
	plugin_pkg_name = 'elasticsearch/elasticsearch-{name}/{version}'.format(name=name, version=version)

	import os.path
	import subprocess
	installed = os.path.exists(plugin_path)
	out_of_date = not os.path.exists(plugin_version_path)

	if state == 'present':
		if not installed:
			subprocess.check_call([manager_path, '--install', plugin_pkg_name])
			changed = True
			reasons.append('plugin was not installed and state is `present\'')
	elif state == 'latest':
		if not installed:
			subprocess.check_call([manager_path, '--install', plugin_pkg_name])
			changed = True
			reasons.append('plugin was not installed and state is `latest\'')
		elif out_of_date:
			subprocess.check_call([manager_path, '--remove', plugin_pkg_name])
			subprocess.check_call([manager_path, '--install', plugin_pkg_name])
			changed = True
			reasons.append('plugin was installed, but out of date and state is `latest\'')
	else:
		if installed:
			subprocess.check_call([manager_path, '--remove', plugin_pkg_name])
			changed = True
			reasons.append('plugin was installed and state is `absent\'')
	return changed, reasons


def main():

	arg_spec = {'name': {'type': 'str', 'required': True},
	            'version': {'type': 'str', 'required': True},
	            'state':   {'type': 'str', 'default': 'present', 'choices': ['present', 'absent', 'latest']},
	            }

	module = AnsibleModule(argument_spec=arg_spec)

	import os.path
	name = module.params['name']
	version = module.params['version']
	state = module.params['state']

	changed, reasons = es_plugin(module, name, version, state)

	module.exit_json(name=name, version=version, changed=changed, msg='OK', reasons=reasons)

from ansible.module_utils.basic import *
main()
