import boto3
import click
import botocore

session = boto3.Session(profile_name='shotty')
ec2 = session.resource('ec2')

def search_instance(project):

    instances = []
    if project:
        filters = [{'Name':'tag:Project','Values':[project]}]
        instances = ec2.instances.filter(Filters=filters)
    else:
        instances = ec2.instances.all()
    return instances
@click.group()
def cli():
    "To list instances volumes and snapshots"

@cli.group('volumes')
def volumes():
    """ to list volumes """
@volumes.command('list')
@click.option('--project', default=None , help = 'Please enter project name')
def list_volumes(project):
    instances = search_instance(project)

    for i in instances:
        for v in i.volumes.all():
            print(','.join((i.id,v.id,v.state,v.encrypted and "Encrypted" or "Not Encrypted",v.create_time.strftime("%c"),str(v.size)+"GBs")))
    return

@cli.group('snapshots')
def snapshots():
    """ to list snapshots """
@snapshots.command('list')
@click.option('--project', default=None , help = 'Please enter project name')
@click.option('--all','list_all',default = False,is_flag = True, help = 'List all snapshots')
def list_snapshots(project,list_all):
    instances = search_instance(project)

    for i in instances:
        for v in i.volumes.all():
            for s in v.snapshots.all():
                print(','.join((s.id,s.progress,s.state,s.encrypted and "Encrypted" or "Not Encrypted",
                s.start_time.strftime("%c"),str(s.volume_size)+"GBs")))

                if s.state == 'completed' and not list_all : break
    return

@cli.group('instances')
def instances():
    """ To list and operate instances"""
@instances.command('list')
@click.option('--project', default=None , help = 'Please enter project name')
def list_instances(project):
    instances = search_instance(project)

    for i in instances:
        tags = {t['Key']:t['Value'] for t in i.tags or []}
        print(','.join((i.id,i.instance_type,i.state['Name'],i.public_dns_name,tags.get('Project','<No Project>'))))
    return

@instances.command('snapshots')
@click.option('--project', default=None , help = 'to create snapshots')
def create_snapshots(project):
    instances = search_instance(project)

    for i in instances:
        print('stopping instance ......{0}'.format(i.id))
        i.stop()
        i.wait_until_stopped()
        print('instance is stopped... brewing snapshot...{0}'.format(i.id))
        for v in i.volumes.all():
            if has_pending_snapshot():
                print("skipping {0}, snapshot already in progress".format(v.id))
                continue

            print('creating snapshot .......{0}'.format(v.id))
            v.create_snapshot(Description="snapshots created By Nandeesh")
            print('starting instance.....{0}'.format(i.id))
        i.start()
        i.wait_until_running()
    print('Job Done....!')
    return()

@instances.command('stop')
@click.option('--project', default=None , help = 'Please enter project name')
def stop_instances(project):
    instances = search_instance(project)

    for i in instances:
        print('Stopping.......{0}'.format(i.id))
        try:
            i.stop()
        except botocore.exceptions.ClientError as e:
            print('stopping not possible....{0}. '.format(i.id) + str(e))
    return

@instances.command('start')
@click.option('--project', default=None , help = 'Please enter project name')
def start_instances(project):
    instances = search_instance(project)

    for i in instances:
        print('starting ........{0}'.format(i.id))
        try:
            i.start()
        except botocore.exceptions.ClientError as e:
            print('starting not possible....{0}. '.format(i.id) + str(e))
    return

if __name__ == '__main__':
    cli()
