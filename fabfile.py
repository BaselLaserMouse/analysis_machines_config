import re
from itertools import chain, repeat

from fabric import task
from patchwork import files

# TODO make verbosity configurable
# import logging
# logging.basicConfig(level=logging.DEBUG)

# list of available machines, excluding:
# - the_beast (windows machine),
# - composter (Petr's machine),
# - pickaxe (Rob's machine),
# - joiner (Bainsaw's machine),
# - jigsaw (dead machine :/).
machines = [
    'gluegun',
    'harvester',
    'blender',
    'jackhammer',
    'lawnmower',
    'roomba',
    'strimmer',
    'sander',
    'grinder',
    'projector',
    'chainsaw',
    'wheelbarrow',
    'sledgehammer',
    'penknife',
    'scythe',
    'sprinkler',
    'nailgun'
]

hosts = ['{}.mrsic-flogel.swc.ucl.ac.uk'.format(m) for m in machines]

# users mapping, from SWC login to logins found on machines
swc_users = {
    'adilk': [],
    'akhilkevich': ['andreik'],
    'alexanderf': ['alexf'],
    'antoninb': ['blota'],
    'dulciev': ['dulciev'],
    'francescag': [],
    'francoisc': ['chabrol'],
    'hernandom': ['hernandom'],
    'ioanag': ['gasler'],
    'ivanao': ['orsolici'],
    'ivanv': ['ivan'],
    'kellyc': ['clancy'],
    'lisah': [],
    'lauras': ['lauras'],
    'maximer': ['rioma'],
    'majas': ['majas'],
    'michellel': [],
    'mitraj': ['javadzam'],
    'morganer': ['rothmo', 'morgane'],
    'naureeng': ['naureeng'],
    'nicolev': ['nicolev'],
    'petrz': ['znamensk', 'petr'],
    'rajam': ['raja'],
    'robc': ['rob'],
    'shoheif': ['shohei', 'furutach'],
    'sonjah': [],
    'takahirok': ['kanamori'],
    'tommf': [],
}

# reverse mapping from machines logins to SWC logins
machines_users = dict(
    chain.from_iterable(zip(v, repeat(k)) for k, v in swc_users.items())
)


@task(hosts=hosts)
def run(ctx, cmd):
    """run a command, by default on all analysis machines"""
    ctx.run(cmd)


@task(hosts=hosts)
def list_users(ctx):
    """list users having a home directory and match them with SWC login"""

    host = ctx.run('hostname', hide=True).stdout.strip()
    homes = ctx.run('ls -1 /home', hide=True).stdout.strip().split('\n')

    known_users = [user for user in homes if user in machines_users]
    unknown_users = [user for user in homes if user not in machines_users]

    print('###', host, '###')
    print('SWC users:', ', '.join(known_users))
    print('other users:', ', '.join(unknown_users))


@task
def add_winstor(ctx, user=None):
    """add winstor mount point for a user"""

    # check user exist on the machine and in SWC
    homes = ctx.run('ls -1 /home', hide=True).stdout.strip().split('\n')
    if user not in homes:
        host = ctx.run('hostname', hide=True).stdout.strip()
        print('"{}" user does not have a home folder on {}!'
              .format(user, host))
        return

    if user not in machines_users:
        print('"{}" user is not a SWC user!'.format(user))
        return

    # create user mount point, if needed
    mount_point = '/mnt/{user}/winstor'.format(user=user)
    files.directory(ctx, mount_point, sudo=True)

    # add a line to /etc/fstab, if needed
    fstab_path = '/etc/fstab'

    if not files.contains(ctx, fstab_path, mount_point):
        mount_point_string = (
            '\n'
            '# winstor storage for {user}\n'
            '//winstor.ad.swc.ucl.ac.uk/winstor {mount} cifs '
            'username={swc},vers=3.0,noauto,users 0 0'
            .format(mount=mount_point, swc=machines_users[user], user=user)
        )

        # files.append(ctx, fstab_path, mount_point_string, sudo=True)
        ctx.sudo('sh -c \'echo "{new_lines}" >>{fstab} \''
                 .format(new_lines=mount_point_string, fstab=fstab_path))
        print('[fstab] winstor added for {}'.format(user))


@task(hosts=hosts)
def add_winstor_all(ctx):
    """add winstor mount for all SWC users found"""

    homes = ctx.run('ls -1 /home', hide=True).stdout.strip().split('\n')
    users = [user for user in homes if user in machines_users]

    for user in users:
        add_winstor(ctx, user)


@task
def add_swc_homes(ctx, user=None):
    """add swc-homes mount point for a user"""

    # check user exist on the machine and in SWC
    homes = ctx.run('ls -1 /home', hide=True).stdout.strip().split('\n')
    if user not in homes:
        host = ctx.run('hostname', hide=True).stdout.strip()
        print('"{}" user does not have a home folder on {}!'
              .format(user, host))
        return

    if user not in machines_users:
        print('"{}" user is not a SWC user!'.format(user))
        return

    # create user mount point, if needed
    mount_point = '/mnt/{user}/swc-homes'.format(user=user)
    files.directory(ctx, mount_point, sudo=True)

    # add a line to /etc/fstab, if needed
    fstab_path = '/etc/fstab'

    if not files.contains(ctx, fstab_path, mount_point):
        mount_point_string = (
            '\n'
            '# swc-homes storage for {user}\n'
            '//swc-homes.ad.swc.ucl.ac.uk/{swc} {mount} cifs '
            'username={swc},vers=3.0,noauto,users 0 0'
            .format(mount=mount_point, swc=machines_users[user], user=user)
        )

        # files.append(ctx, fstab_path, mount_point_string, sudo=True)
        ctx.sudo('sh -c \'echo "{new_lines}" >>{fstab} \''
                 .format(new_lines=mount_point_string, fstab=fstab_path))
        print('[fstab] swc-homes added for {}'.format(user))


@task(hosts=hosts)
def add_swc_homes_all(ctx):
    """add swc-homes mount for all SWC users found"""

    homes = ctx.run('ls -1 /home', hide=True).stdout.strip().split('\n')
    users = [user for user in homes if user in machines_users]

    for user in users:
        add_swc_homes(ctx, user)


@task(hosts=hosts)
def btrfs_scrub(ctx):
    """check state of BTRFS scrub operations"""

    btrfs_pattern = re.compile(' on (.+) type btrfs ')
    mounts = ctx.run('mount', hide=True).stdout.strip().split('\n')
    mounts = [btrfs_pattern.search(mount) for mount in mounts]
    mounts = [mount.groups()[0] for mount in mounts if mount is not None]

    host = ctx.run('hostname', hide=True).stdout.strip()
    for mount in mounts:
        print(host, mount)
        ctx.sudo('btrfs scrub status {}'.format(mount))
