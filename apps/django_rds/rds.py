"""
ec2.py provides the interfaces necessary to use amazon rds via Boto.

In order for boto to successfully connect to the correct AWS account, you will
need to set the appropriate environment variables containing the ACCESS_ID
and SECRET_KEY. These credentials can be obtained from the AWS security setup.

Perhaps add something like this to your $HOME/.profile:
export AWS_ACCESS_KEY_ID="AKIAIY..."
export AWS_SECRET_ACCESS_KEY="KSbns6..."

If you don't want your instances to go to the default ec2 region, you may
need to create a boto configuration file [1].

    [1] http://boto.cloudhackers.com/ec2_tut.html

"""

import time
import boto.rds
from boto.rds import RDSConnection
from boto.rds.parametergroup import Parameter, ParameterGroup
from django_rds import logger

class InstanceManager(object):
    """
    A class to manage RDS instances.
    """
    _defaultRegion = 'us-east-1'

    def __init__(self, connection=None):
        """
        Initialize the InstanceManager, allowing for dependency injection
        """
        if not connection:
            self.connection = RDSConnection()
        else:
            self.connection = connection

    def _getConnection(self, region=None):
        """
        get a connection to the default region endpoint
        """
        if not region:
            regionName = self._defaultRegion

        for region in boto.rds.regions():
            if region.name == regionName:
                self.region = region
                logger.info('using region %s' %(str(region.name)))
                return self.region.connect()

    def _formatInstance(self, instance):
        """
        format an instance with relevant info
        """
        return "%(id)-10s %(instance_class)-10s %(engine)-8s %(parameter_group)-20s" %(instance.__dict__)
    
    @property
    def instances(self):
        """
        list the instances available in the connection
        """
        db_instances = self.connection.get_all_dbinstances()
        instances = list()
        for i in db_instances:
            i.formatted = self._formatInstance(i)
            instances.append(i)
        return instances
    
    def modify_paramater_group(self, group_name = 'default.mysql5.5', parameter = '', type = '', value = ''):
        parameter_group = ParameterGroup(self.connection)
        parameter_group.name = group_name
        parameter = Parameter(parameter_group, parameter)
        parameter.type = type
        parameter.apply_method = 'immediate'
        parameter.apply_type = 'dynamic'
        parameter.set_value(value)
        self.connection.modify_parameter_group(group_name, [parameter])
        
    def launch(self):
        """
        launch an instance
        """
        pass

    def terminate(self, instance_id):
        """
        terminate an instance
        """
        instance = self.get_instance(instance_id)
        if instance:
            logger.debug('Successfully connected to instance %s' %(instance_id),)
            instance.terminate()
            logger.info('Instance %s terminated' %(instance_id,))
        else:
            logger.warning('Instance %s not found' %(instance_id,))

    def get_instance(self, instance_id):
        """
        get a handle to an instance by id
        """
        return self.connection.get_all_instances((instance_id,))[0].instances[0]


    def get_external_dns_name(self, instance_id):
        """
        get the dns name for the specified instance
        """
        instance = self.get_instance(instance_id)
        return instance.dns_name