import click
import subprocess
import pymongo
import sys

@click.command()
@click.option('--run/--no-run', default=None, help="run mongod with `--dbpath`")
@click.option('--info/--no-info', default=False, help="the names of the databases")
@click.option('--create', default=None, help="create a database, specify a name")
@click.option('--delete', default=None, help="delete a database, specify a name")
@click.option('--shutdown/--no-shutdown', default=None, help='shutdown the database server using `--dbpath`')
@click.option('--dbpath', default=None, help='specify the dbpath to run or remove')

def handle(run, info, create, delete, shutdown, dbpath):
    if run:
        dbrun(dbpath)

    if create:
        client = pymongo.MongoClient('localhost', 27017)
        dbcreate(client, create)

    if info:
        client = pymongo.MongoClient('localhost', 27017)
        dbinfo(client)
        
    if delete:
        client = pymongo.MongoClient('localhost', 27017)
        dbdelete(client, delete)

    if shutdown:
        dbshutdown(dbpath)
        
def dbrun(dbpath):
    command = ['mongod']
    if dbpath:
        command.append('--dbpath')
        command.append(dbpath)
    subprocess.Popen(command)

def dbcreate(client, dbname):
    db = client[dbname]
    collection = db['setup-collection']
    collection.insert({'setup-data' : True})
    
def dbinfo(client):
    click.echo('list of databases')
    for name in client.database_names():
        click.echo('database: {0}'.format(name))

def dbdelete(client, dbname):
    if click.confirm('Do you want to delete the {0} database?'.format(dbname)):
        client.drop_database(dbname)
    click.echo('deleted the {0} database'.format(dbname))

def dbsetup():
    #Add some test data to the database
    pass

def dbshutdown(dbpath):
    if "linux" in sys.platform or "darwin" in sys.platform:
        command = ['mongo']
        command.append('--eval')
        command.append('db.getSiblingDB(\'admin\').shutdownServer()')
        subprocess.call(command)
    else:
        click.echo('your {0} platform is not supported.'.format(sys.platform))
        if click.confirm('Try the mongo shell option anyway?'):
            command = ['mongo']
            command.append('--eval')
            command.append('db.getSiblingDB(\'admin\').shutdownServer()')
            subprocess.call(command)

if __name__ == "__main__":
    handle()
    

# python dbhandle.py --run --dbpath=/home/fyc/Documents/Projects/NIST/CoRR/github/mongo-data/data
