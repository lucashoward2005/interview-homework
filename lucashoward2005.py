
#imports
import sys
import boto3
from influxdb import InfluxDBClient

#lambda handler
def lambda_handler(event, context):
    
    #init ec2 object using boto3
    ec2 = boto3.resource('ec2')

    #create filter for tag homework with value lucashoward2005 and instance state running
    filter = [{
        'Name': 'tag:homework',
        'Values': ['lucashoward2005'] },
        {'Name': 'instance-state-name',
        'Values': ['running']
        }]

    #get all instances that match the filter
    instances = ec2.instances.filter(Filters=filter)
    num_instances = len(list(instances.all()))

    #insert code
    result = insertNumberIntoInfluxDB(num_instances)

    #return result
    return result
    
    #instances.

    # TODO implement
    #return 'Hello from Lambda'

def insertNumberIntoInfluxDB(number):
    
    #Localized Import of influxdb module
    #from influxdb import InfluxDBClient
  
    #Harcoded connection variables... in a real environment you'd probably want to grab these from a S3/keystore dependent on the event?
    influx_port = 8086
    influx_hostname = 'ec2-54-200-187-28.us-west-2.compute.amazonaws.com'
    influx_database = 'homework'
      

    #create client... real world wouldn't want hard coding more then likely
    client = InfluxDBClient(host=influx_hostname,port=influx_port,database=influx_database)

    #data to write
    data = [{
              "measurement": "homework",
              "fields": { "lucashoward2005": number }
           }]
             
    #insert 
    result = client.write_points(data)
    
    #return result
    return result
    
