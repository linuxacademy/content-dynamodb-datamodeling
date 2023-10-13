/* Create the dms_source table: */

CREATE TABLE
    dms_source
SELECT
    employees.*,
    titles.title,
    titles.from_date AS title_from_date,
    titles.to_date AS title_to_date,
    salaries.salary,
    salaries.from_date AS salary_from_date,
    salaries.to_date AS salary_to_date,
    dept_emp.dept_no as department_number,
    departments.dept_name as department_name,
    dept_emp.from_date AS dept_from_date,
    dept_emp.to_date AS dept_to_date
FROM (SELECT * FROM employees LIMIT 500) employees
    INNER JOIN titles ON employees.emp_no=titles.emp_no
    INNER JOIN salaries ON employees.emp_no=salaries.emp_no
    INNER JOIN dept_emp ON employees.emp_no=dept_emp.emp_no
    INNER JOIN departments ON dept_emp.dept_no=departments.dept_no;

/* Frequent Queries (Access Patterns) */

/* DynamoDB will allow us to utilize the query function on our new table, but the following queries are shown as an example of what can be done through the CLI to obtain the requested access patterns. Below is a list of the frequent queries or access patterns requested for this lab: */

/* Get the department name, title, employee ID, first name, last name, and salary for all employees in the **Development** department with the title **Senior Engineer** (only including **most recent salary**): */

   SELECT
    departments.dept_name AS "Department Name",
    titles.title AS "Title",
    employees.emp_no AS "Employee ID",
    employees.first_name AS "First Name",
    employees.last_name AS "Last Name",
    salaries.salary AS "Salary"
   FROM employees
    INNER JOIN salaries ON employees.emp_no=salaries.emp_no
    INNER JOIN dept_emp ON employees.emp_no=dept_emp.emp_no
    INNER JOIN departments ON dept_emp.dept_no=departments.dept_no
    INNER JOIN titles on employees.emp_no=titles.emp_no
   WHERE
    salaries.to_date="9999-01-01"
   AND
    departments.dept_name="Development"
   AND
    titles.title="Senior Engineer";

/* Get all information about an employee in the **Production** department with the full name **Hercules Benzmuller**: */
 
   SELECT
    employees.*,
    titles.title,
    titles.from_date AS "Title from",
    titles.to_date AS "Title to",
    salaries.salary,
    salaries.from_date AS "Salary from",
    salaries.to_date AS "Salary to",
    departments.dept_name,
    dept_emp.from_date AS "Department from",
    dept_emp.to_date AS "Department to"
   FROM employees
    INNER JOIN titles on employees.emp_no=titles.emp_no
    INNER JOIN salaries ON employees.emp_no=salaries.emp_no
    INNER JOIN dept_emp ON employees.emp_no=dept_emp.emp_no
    INNER JOIN departments ON dept_emp.dept_no=departments.dept_no
   WHERE
    departments.dept_name="Production"
   AND
    employees.first_name="Hercules"
   AND
    employees.last_name="Benzmuller";

/* Get all employees with the title **Engineer**, returning only **most recent salary**: */

   SELECT
    employees.*,
    titles.title,
    titles.from_date AS "Title from",
    titles.to_date AS "Title to",
    salaries.salary,
    salaries.from_date AS "Salary from",
    salaries.to_date AS "Salary to",
    departments.dept_name,
    dept_emp.from_date AS "Department from",
    dept_emp.to_date AS "Department to"
   FROM employees
    INNER JOIN titles on employees.emp_no=titles.emp_no
    INNER JOIN salaries ON employees.emp_no=salaries.emp_no
    INNER JOIN dept_emp ON employees.emp_no=dept_emp.emp_no
    INNER JOIN departments ON dept_emp.dept_no=departments.dept_no
   WHERE
    titles.title="Engineer"
   AND
    salary.to_date="9999-01-01";
   
/* Get all employees in the **Production** department hired between **1999 and 2001**: */
   
   SELECT
    employees.*,
    titles.title,
    titles.from_date AS "Title from",
    titles.to_date AS "Title to",
    salaries.salary,
    salaries.from_date AS "Salary from",
    salaries.to_date AS "Salary to",
    departments.dept_name,
    dept_emp.from_date AS "Department from",
    dept_emp.to_date AS "Department to"
   FROM employees
    INNER JOIN titles on employees.emp_no=titles.emp_no
    INNER JOIN salaries ON employees.emp_no=salaries.emp_no
    INNER JOIN dept_emp ON employees.emp_no=dept_emp.emp_no
    INNER JOIN departments ON dept_emp.dept_no=departments.dept_no
   WHERE
    departments.dept_name="Production"
   AND
    UNIX_TIMESTAMP(employees.hire_date) BETWEEN UNIX_TIMESTAMP("1999-01-01") AND UNIX_TIMESTAMP("2001-01-01");

/* Get all employees in the **Development** department who had a **title change** in the **6 months before January 1, 2001**: */

   SELECT
    employees.*,
    titles.title,
    titles.from_date AS "Title from",
    titles.to_date AS "Title to",
    salaries.salary,
    salaries.from_date AS "Salary from",
    salaries.to_date AS "Salary to",
    departments.dept_name,
    dept_emp.from_date AS "Department from",
    dept_emp.to_date AS "Department to"
   FROM employees
    INNER JOIN titles on employees.emp_no=titles.emp_no
    INNER JOIN salaries ON employees.emp_no=salaries.emp_no
    INNER JOIN dept_emp ON employees.emp_no=dept_emp.emp_no
    INNER JOIN departments ON dept_emp.dept_no=departments.dept_no
   WHERE
    departments.dept_name="Development"
   AND
    UNIX_TIMESTAMP(titles.from_date) BETWEEN UNIX_TIMESTAMP("2000-06-01") AND UNIX_TIMESTAMP("2001-01-01");
