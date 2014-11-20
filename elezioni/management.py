__author__ = 'Vincenzo Petrungaro'

from django.db.models import signals
from django.contrib.auth.models import Group, Permission
import models
import config

def create_user_groups(app, created_models, verbosity, **kwargs):
  if verbosity>0:
    print "Initialising data post_syncdb"
  for group in config.DEFAULT_SYSTEM_GROUPS_PERMISSIONS:
    role, created = Group.objects.get_or_create(name=group)
    if verbosity>1 and created:
      print 'Creating group', group
    for perm in config.DEFAULT_SYSTEM_GROUPS_PERMISSIONS[group]:
      role.permissions.add(Permission.objects.get(codename=perm))
      if verbosity>1:
        print 'Permitting', group, 'to', perm
    role.save()

signals.post_syncdb.connect(
  create_user_groups,
  sender=models, # only run once the models are created
  dispatch_uid='elezioni.models.create_user_groups' # This only needs to universally unique; you could also mash the keyboard
)
