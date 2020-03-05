# Data Migration Phase

## Access Patterns & Supporting Indexes

- Find employee by employee ID
  - Base table, query on `emp_no`
- Find all employees for a given last name
  - GSI PK: `last_name`
- Find all employees for a given title
  - GSI PK: `title`
- Find all employees for a given department
  - GSI PK: `department_name`
- Find all employees with salary >= 130,000
  - GSI PK: `salary_to_date` SK: `salary`
  - query where `salary_to_date=9999-01-01` and `salary>=130000`
- Find all current department managers
  - GSI PK: `department_manager` SK: `manager_name`
  - query GSI once for each `department_name`

## Employees DynamoDB Table Definition

```sh
./create.py
```

## MySQL Employees Sample Database

AMI ID: `amzn_lin2_mysql57_employees (ami-0aa8df173b9f8c0d3)`

- minimum t3a.2xlarge
- minimum 10 GB EBS gp2
- Security group:
  - SSH (22/tcp)
  - MySQL (3306/tcp)

Connect via `ssh -i <keypair.pem> ec2-user@<public ip>`

MySQL **read-only** user:  
username: `cloud_user`  
password: `bettertogether`  

```sh
mysql -ucloud_user -pbettertogether employees

mysql> show tables;
+----------------------+
| Tables_in_employees  |
+----------------------+
| current_dept_emp     |
| departments          |
| dept_emp             |
| dept_emp_latest_date |
| dept_manager         |
| employees            |
| salaries             |
| titles               |
+----------------------+
8 rows in set (0.00 sec)
```

MySQL **root** user (local only):  
username: `root`  
password: `Str0ngpass!`  

```sh
mysql -uroot -pStr0ngpass! employees
```

## Create Materialized View in MySQL

**Note:** You must connect to MySQL as `root` in order to create tables or views.

```sql
CREATE VIEW dms_source AS 
SELECT 
  employees.*,
  titles.title,
  titles.from_date AS title_from_date,
  titles.to_date AS title_to_date,
  salaries.salary,
  salaries.from_date AS salary_from_date,
  salaries.to_date AS salary_to_date,
  dept_emp.dept_no AS department_number,
  departments.dept_name AS department_name,
  dept_emp.from_date AS dept_from_date,
  dept_emp.to_date AS dept_to_date,
  CONCAT_WS(' ', manager.first_name, manager.last_name) AS manager_name,
  manager.emp_no AS manager_emp_no
FROM employees
  INNER JOIN titles ON employees.emp_no = titles.emp_no
  INNER JOIN salaries ON employees.emp_no = salaries.emp_no
  INNER JOIN dept_emp ON employees.emp_no = dept_emp.emp_no
  INNER JOIN departments ON dept_emp.dept_no = departments.dept_no
  INNER JOIN dept_manager dm ON dm.dept_no = departments.dept_no
  INNER JOIN employees manager ON manager.emp_no = dm.emp_no;
```

```sql
CREATE TABLE dms_source_materialized SELECT * FROM dms_source;
```

The `CREATE TABLE` command should take approximately 3 minutes to complete.

```text
mysql> CREATE TABLE dms_source_materialized SELECT * FROM dms_source;
Query OK, 13849320 rows affected (2 min 51.05 sec)
Records: 13849320  Duplicates: 0  Warnings: 0

mysql> select count(emp_no) from dms_source_materialized;
+---------------+
| count(emp_no) |
+---------------+
|      13849320 |
+---------------+
1 row in set (8.69 sec)
```

## Create DMS Access Role

Name: `DMSDynamoDBFullAccess`  
Permissions: `AmazonDynamoDBFullAccess`

Note the service access role ARN.

## DMS Replication instance

Name: `instance1`  
Class: `dms.t2.medium`  
Engine version: `3.3.1` (or latest)  

## Create Source Endpoint

Name: `employees-mysql`
Engine: `MySQL`
Username: `cloud_user`

## Create Target Endpoint

Name: `employees-dynamodb`

## DMS Task

Name: `employeestest`  
Rules: `rules.json`

## Testing the Access Patterns

```sh
./query.py
```

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
