#!/usr/bin/python
# change accordingly  - which python
#
# sample run
# example1: ./mk_roles.py role2 user1@somedomain (user to new role)
# example2: ./mk_roles.py role1 user2@somedomain (new user to existing role)
import ConfigParser, os, sys
import datetime
from shutil import copyfile

config = ConfigParser.ConfigParser()

# role == group 
group = sys.argv[1]
user = sys.argv[2]

# make a backup 
dest='roles.ini.' + datetime.datetime.now().strftime("%d-%M-%Y_%I:%M:%S")
copyfile('roles.ini', dest)
config.read('roles.ini')

# example 1 
if not config.has_section(group):
	config.add_section(group)
	config.set(group, 'users', '"%s"'%user)
	config.set(group, 'permissions', '"module/director, director/hosts, director/services, module/monitoring, monitoring/command/*"')
	config.set(group, 'director/filter/hostgroups', '"%s"'%group)
	config.set(group, 'monitoring/filter/objects', '"hostgroup_name=%s"'%group)
	
# example 2
elif config.has_section(group):
	current_users = config.get(group, 'users')
	if user in current_users:
		print "User %s has already assgined role within group %s"%(user, group)
	else:
		current_users = current_users.strip('"')
		current_users += ", %s"%user
	        config.set(group, 'users', '"%s"'%current_users)
else:
	pass

with open('roles.ini', 'wb') as configfile:
	config.write(configfile)

print "icingaweb2 role successfully set"
