import boto3

# Define the EC2 client
ec2 = boto3.client('ec2')

def lambda_handler(event, context):
    """
    This function stops all EC2 instances that have a tag 'Auto-Shutdown' with a value of 'True'.
    """
    
    # Define the filter to find instances with the specific tag
    filters = [
        {
            'Name': 'tag:Auto-Shutdown',
            'Values': ['True']
        },
        {
            'Name': 'instance-state-name',
            'Values': ['running']
        }
    ]
    
    # Retrieve the instance IDs of the running instances with the tag
    instances = ec2.describe_instances(Filters=filters)
    
    # Extract instance IDs from the response
    instance_ids_to_stop = []
    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            instance_ids_to_stop.append(instance['InstanceId'])
            
    # Stop the instances if any are found
    if not instance_ids_to_stop:
        print("No running instances found with the 'Auto-Shutdown:True' tag.")
        return
    else:
        print(f"Stopping instances: {', '.join(instance_ids_to_stop)}")
        ec2.stop_instances(InstanceIds=instance_ids_to_stop)
        print("Successfully sent stop command.")
        return