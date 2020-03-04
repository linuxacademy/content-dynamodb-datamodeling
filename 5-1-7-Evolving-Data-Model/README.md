# Evolving a Data Model

## Supporting a new access pattern

> Find all current employees with tenure > N years

**Problem:**

This could be done with an LSI on `salary_to_date=9999-01-01` but this table is already in production and we can't add an LSI, only a GSI.

**Solution:**

  1. Create a batch job to parallel scan the entire table for `salary_to_date=9999-01-01` and add a new attribute `is_current=1`
  2. Create a GSI on `is_current` with SK `hire_date`.

**Considerations:**

If a salary, title, or department change then we can update this on a per-employee basis — no need to run the batch job again.

For new employee records, the `is_current` attribute needs to be accounted for in the application.
