import boto3
import click

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

@instances.command('stop')
@click.option('--project', default=None , help = 'Please enter project name')
def list_instances(project):
    instances = search_instance(project)

    for i in instances:
        print('Stopping.......{0}'.format(i.id))
        i.stop()
    return

@instances.command('start')
@click.option('--project', default=None , help = 'Please enter project name')
def list_instances(project):
    instances = search_instance(project)

    for i in instances:
        print('starting ........{0}'.format(i.id))
        i.start()
    return

if __name__ == '__main__':
    instances()
