# EC2 Backup Tool

A Python command-line tool for creating and managing backups of AWS EC2 instances using EBS snapshots. It shows which instances are running, back up an instance's storage, list existing backups, check details on a specific backup, and delete old backups.

## Features

- `backup` - Create a new EBS snapshot (backup) of a specific instance
- `list-instances` - Show all EC2 instances with their color-coded status (running/stopped/pending)
- `list` - Show all existing snapshots with their status
- `delete` - Delete a snapshot
- `info` - Show detailed information about a specific snapshot (volume ID, progress, start time)

## Prerequisites

- Python 3.6+
- AWS account with EC2 access
- `boto3` and `colorama` Python libraries
- AWS credentials configured (`aws configure`)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/S0R4Y4Y/ec2-backup-tool.git
cd ec2-backup-tool
```

2. Install dependencies:
```bash
pip3 install boto3 colorama
```

3. Configure AWS credentials:
```bash
aws configure
```

## Usage

### List all instances
```bash
python3 ec2_backup_tool.py list-instances
```

### Create a backup of an instance
```bash
python3 ec2_backup_tool.py backup --instance-id i-1234567890abcdef
```

### List all snapshots (backup)
```bash
python3 ec2_backup_tool.py list
```

### Delete a snapshot
```bash
python3 ec2_backup_tool.py delete --snapshot-id snap-1234567890abcdef
```

### Show details of a specific snapshot
```bash
python3 ec2_backup_tool.py info --snapshot-id snap-1234567890abcdef
```

## How It Works

Every EC2 instance's storage is backed by an EBS volume. This tool looks up the volume attached to a given instance, then creates an EBS snapshot of it, essentially a point-in-time backup of the instance's disk. Snapshots can later be used to restore data if an instance is lost, corrupted, or accidentally deleted. The tool uses `boto3` (AWS's Python SDK) to automate the process of finding volumes, creating snapshots, checking their status, and cleaning them up, instead of doing this manually through the AWS Console.
