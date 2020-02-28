# Data Migration Phase

## Access Patterns & Supporting Indexes

- Find employee by employee ID
  - Base table, query on emp_no
- Find all employees for a given last name
  - GSI on last_name
- Find all employees for a given title
  - GSI on title
- Find all employees for a given department
  - GSI on department_name
- Find all employees with salary >= 130,000
  - GSI PK: salary_to_date SK: salary
  - query where salary_to_date=9999-01-01 and salary>=130000
- Find all current department managers
  - GSI PK: department_manager SK: manager_name
  - query GSI once for each department_name

## MySQL Employees Sample Database

AMI ID: `ami-0aa8df173b9f8c0d3` (minimum t3a.2xlarge recommended)  
MySQL username: `cloud_user`  
MySQL password: `bettertogether`  

## Employees DynamoDB Table Definition

```sh
./create.py
```

## Replication instance

Class: `dms.t2.medium`  
Engine version: `3.3.1` (or latest)  

## DMS Task

`rules.json`

## Can't see DMS task CloudWatch Logs?

1. Create an IAM role with trusted entity `DMS`
2. Attach the `AmazonDMSCloudWatchLogsRole` managed policy
3. Save the role as `dms-cloudwatch-logs-role`

## Tip: Increasing DMS Task Logging Level to Debug

<https://aws.amazon.com/premiumsupport/knowledge-center/dms-enable-debug-logging/>

```sh
aws dms modify-replication-task \
  --replication-task-arn <task-arn> \
  --replication-task-settings file://task-settings-debug.json
```
