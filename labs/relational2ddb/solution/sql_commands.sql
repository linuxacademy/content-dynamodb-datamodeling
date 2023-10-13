/* Connect to the MySQL source database using the database public IP provided for the lab: */

    mysql -h <SOURCE_DATABASE_PUBLIC_IP> -u cloud_user -pbettertogether employees

/* Take a look at the tables in the database: */

    SHOW tables;

/* Review the `employees` table: */

    DESCRIBE employees;

/* Review the `dms_source` table: */

    DESCRIBE dms_source;

/* Review the full details of the first 10 rows of the `dms_source` table: */

    SELECT * FROM dms_source LIMIT 10\G

/* Note that the `title_to_date` and `dept_to_date` values are set to `9999-01-01` for all 10 rows. This special value indicates that this is the latest data available, and is useful in filtering the data. */

/* Enter `quit` to exit the table */
