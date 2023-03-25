#!/bin/bash
cd /home/ubuntu/linux_static/fb-zoo/ && python3 -m app.main
host=`hostname -I | awk '{print $1}'`
DESCRIBE_COMMAND=$(aws ec2 describe-instances \
		   --filters Name=network-interface.addresses.private-ip-address,Values=$host \
                   --query 'Reservations[*].Instances[*].{Instance:InstanceId}' \
                   --output text)
echo $DESCRIBE_COMMAND
#aws ec2 terminate-instances --instance-ids $DESCRIBE_COMMAND
