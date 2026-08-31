import boto3
import argparse
from colorama import Fore, Style, init

init(autoreset=True)

ec2 = boto3.client('ec2', region_name='ap-southeast-1')

def backup(instance_id):
    response = ec2.describe_instances(InstanceIds=[instance_id])
    instance = response['Reservations'][0]['Instances'][0]
    volume_id = instance['BlockDeviceMappings'][0]['Ebs']['VolumeId']

    snapshot = ec2.create_snapshot(
        VolumeId=volume_id,
        Description=f'Backup of {instance_id}'
    )

    print(f"Snapshot started for {instance_id}")
    print(f"Snapshot ID: {snapshot['SnapshotId']}")

def list_snapshots():
    response = ec2.describe_snapshots(OwnerIds=['self'])
    
    if not response['Snapshots']:
        print("No snapshots found.")
        return
    
    print(f"{'Snapshot_ID':<25} {'Description':<32} {'Start_Time':<32} {'State':<15}")
    print("-" * 105)
    
    for snapshot in response['Snapshots']:
        snapshot_id = snapshot['SnapshotId']
        description = snapshot['Description']
        state = snapshot['State']
        start_time = snapshot['StartTime']

        if state == 'completed':
            state = Fore.GREEN + state + Style.RESET_ALL
        elif state == 'pending':
            state = Fore.YELLOW + state + Style.RESET_ALL
        elif state == 'error':
            state = Fore.RED + state + Style.RESET_ALL

        print(f"{snapshot_id:<25} {description:<32} {start_time} {state:<15}")

def delete_snapshot(snapshot_id):
    try:
        ec2.delete_snapshot(SnapshotId=snapshot_id)
        print(f"Snapshot {snapshot_id} has been deleted.")
    except Exception as e:
        print(f"Error: {e}")

def snapshot_info(snapshot_id):
    try:
        response = ec2.describe_snapshots(SnapshotIds=[snapshot_id])
        snapshot = response['Snapshots'][0]

        print(f"Snapshot ID: {snapshot['SnapshotId']}")
        print(f"Volume ID: {snapshot['VolumeId']}")
        print(f"State:       {snapshot['State']}")
        print(f"Progress:    {snapshot['Progress']}")
        print(f"Start Time:  {snapshot['StartTime']}")
        print(f"Description: {snapshot['Description']}")
    
    except Exception as e:
        print(f"Error: {e}")

def main():
    parser = argparse.ArgumentParser(description='EC2 Backup Tool')
    parser.add_argument('action', choices=['backup', 'list', 'delete', 'info'],
                        help='Action to perform')
    parser.add_argument('--instance-id', help='EC2 Instance ID')
    parser.add_argument('--snapshot-id', help='EC2 Snapshot ID')

    args = parser.parse_args()

    if args.action == 'backup':
        if not args.instance_id:
            print("Error: --instance-id required for backup action")
            return
        backup(args.instance_id)

    elif args.action == 'list':
        list_snapshots()
        
    elif args.action == 'delete':
        if not args.snapshot_id:
            print("Error: --snapshot-id required for delete action")
            return
        delete_snapshot(args.snapshot_id)

    elif args.action == 'info':
        if not args.snapshot_id:
            print("Error: --snapshot-id required for info action")
            return
        snapshot_info(args.snapshot_id)

if __name__ == '__main__':
    main()



    
