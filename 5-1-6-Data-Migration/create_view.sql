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

CREATE TABLE dms_source_materialized SELECT * FROM dms_source;
