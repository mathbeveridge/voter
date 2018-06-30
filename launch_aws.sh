#!/bin/bash

#aws emr create-cluster \
    #--name "Spark cluster" \
    #--release-label emr-5.14.0 \
    #--applications Name=Spark \
    #--instance-groups \
    #--ec2-attributes SubnetId=subnet-18171730,KeyName=feb2016-keypair \
    #--instance-type m5.12xlarge --instance-count 5 --use-default-roles


aws emr create-cluster \
    --applications Name=Hadoop Name=Hive Name=Pig Name=Hue Name=Spark \
    --ebs-root-volume-size 40 \
    --ec2-attributes KeyName=feb2016-keypair,SubnetId=subnet-18171730 \
    --release-label emr-5.15.0 \
    --log-uri 's3n://aws-logs-798314792140-us-east-1/elasticmapreduce/' \
    --name 'My cluster' \
    --instance-groups '[{"InstanceCount":5,"BidPrice":"3.00","EbsConfiguration":{"EbsBlockDeviceConfigs":[{"VolumeSpecification":{"SizeInGB":128,"VolumeType":"gp2"},"VolumesPerInstance":1}]},"InstanceGroupType":"CORE","InstanceType":"m5.12xlarge","Name":"Core - 2"},{"InstanceCount":1,"BidPrice":"3.00","EbsConfiguration":{"EbsBlockDeviceConfigs":[{"VolumeSpecification":{"SizeInGB":128,"VolumeType":"gp2"},"VolumesPerInstance":1}]},"InstanceGroupType":"MASTER","InstanceType":"m5.12xlarge","Name":"Master - 1"}]' \
    --region us-east-1 \
    --use-default-roles

    #--auto-scaling-role EMR_AutoScaling_DefaultRole \
    #--termination-protected \
    #--service-role EMR_DefaultRole \
    #--scale-down-behavior TERMINATE_AT_TASK_COMPLETION \
    #--enable-debugging \
