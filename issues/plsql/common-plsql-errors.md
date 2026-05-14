# Common PL/SQL Errors & Solutions

## ORA-06502: PL/SQL: numeric or value error

### Error Message
```
ORA-06502: PL/SQL: numeric or value error: character to number conversion error
```

### Causes
- Attempting to convert non-numeric string to number
- Numeric overflow in arithmetic operation
- Invalid date conversion
- Buffer too small for data

### Solution
```plsql
-- INCORRECT
DECLARE
    v_number NUMBER;
BEGIN
    v_number := TO_NUMBER('ABC');  -- This will fail
END;
/

-- CORRECT
DECLARE
    v_number NUMBER;
BEGIN
    BEGIN
        v_number := TO_NUMBER('123');
    EXCEPTION
        WHEN VALUE_ERROR THEN
            DBMS_OUTPUT.PUT_LINE('Invalid number format');
            v_number := 0;
    END;
END;
/
```

---

## ORA-01422: exact fetch returns more than requested number of rows

### Error Message
```
ORA-01422: exact fetch returns more than requested number of rows
```

### Causes
- SELECT INTO query returns multiple rows
- Query not specific enough
- Missing WHERE clause condition

### Solution
```plsql
-- INCORRECT
DECLARE
    v_item_id NUMBER;
BEGIN
    SELECT inventory_item_id INTO v_item_id
    FROM mtl_system_items_b;
    -- Returns multiple rows - ERROR
END;
/

-- CORRECT
DECLARE
    v_item_id NUMBER;
BEGIN
    SELECT inventory_item_id INTO v_item_id
    FROM mtl_system_items_b
    WHERE organization_id = 101
    AND   segment1 = 'ITEM123';
    -- Now returns single row
END;
/
```

---

## ORA-04091: table is mutating, trigger may not see it

### Error Message
```
ORA-04091: table %s is mutating, trigger may not see it
```

### Causes
- Trigger trying to read/modify same table it's triggered on
- Row-level trigger referencing parent table during DML
- Cycle in trigger execution

### Solution
```plsql
-- INCORRECT TRIGGER
CREATE TRIGGER tr_items_update
AFTER UPDATE ON mtl_system_items_b
FOR EACH ROW
BEGIN
    -- This will fail
    SELECT COUNT(*) INTO v_count
    FROM mtl_system_items_b
    WHERE organization_id = :NEW.organization_id;
END;
/

-- CORRECT: Use Statement-level trigger
CREATE TRIGGER tr_items_update
AFTER UPDATE ON mtl_system_items_b
FOR EACH STATEMENT
BEGIN
    -- This works - statement level
    SELECT COUNT(*) INTO v_count
    FROM mtl_system_items_b
    WHERE organization_id = 101;
END;
/

-- OR: Use package with compound trigger
CREATE OR REPLACE PACKAGE pkg_item_triggers AS
END pkg_item_triggers;
/

CREATE OR REPLACE TRIGGER tr_items_compound
    FOR UPDATE ON mtl_system_items_b
    COMPOUND TRIGGER
    
    v_count NUMBER;
    
    AFTER EACH ROW IS
    BEGIN
        -- Row-level logic
        NULL;
    END AFTER EACH ROW;
    
    AFTER STATEMENT IS
    BEGIN
        -- Access table here
        SELECT COUNT(*) INTO v_count
        FROM mtl_system_items_b;
    END AFTER STATEMENT;
END tr_items_compound;
/
```

---

## ORA-20001: Custom Application Error

### Error Message
```
ORA-20001: <custom message>
```

### Best Practice
```plsql
DECLARE
    v_item_id NUMBER := 0;
BEGIN
    IF v_item_id IS NULL THEN
        RAISE_APPLICATION_ERROR(-20001, 'Item ID cannot be null');
    END IF;
    
EXCEPTION
    WHEN OTHERS THEN
        -- Log error
        INSERT INTO error_log(error_msg, error_code) 
        VALUES (SQLERRM, SQLCODE);
        -- Re-raise
        RAISE;
END;
/
```

---

## ORA-01403: no data found

### Error Message
```
ORA-01403: no data found
```

### Causes
- SELECT INTO returns no rows
- Cursor FETCH returns no rows
- Reference to non-existent collection element

### Solution
```plsql
-- CORRECT: Handle NO_DATA_FOUND
DECLARE
    v_item_id NUMBER;
BEGIN
    SELECT inventory_item_id INTO v_item_id
    FROM mtl_system_items_b
    WHERE segment1 = 'NONEXISTENT';
    
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        DBMS_OUTPUT.PUT_LINE('Item not found');
        v_item_id := NULL;
END;
/
```

---

## ORA-00001: unique constraint violated

### Error Message
```
ORA-00001: unique constraint (SCHEMA.CONSTRAINT_NAME) violated
```

### Solution
```plsql
BEGIN
    INSERT INTO items(item_id, item_number)
    VALUES(1, 'ITEM001');
    
EXCEPTION
    WHEN DUP_VAL_ON_INDEX THEN
        DBMS_OUTPUT.PUT_LINE('Item already exists');
        -- Update instead
        UPDATE items 
        SET item_number = 'ITEM001_UPDATED'
        WHERE item_id = 1;
END;
/
```

---

## ORA-02292: integrity constraint violated - child record found

### Error Message
```
ORA-02292: integrity constraint (SCHEMA.FK_NAME) violated - child record found
```

### Solution
```plsql
-- Delete child records first
BEGIN
    DELETE FROM mtl_item_sub_inventories
    WHERE inventory_item_id = 123;
    
    DELETE FROM mtl_system_items_b
    WHERE inventory_item_id = 123;
    
    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        RAISE;
END;
/
```

---

## ORA-04068: existing state of packages has been discarded

### Causes
- Package recompiled while session is using it
- Session references package that was dropped/recreated

### Solution
```plsql
-- Disconnect and reconnect session
-- Or use PRAGMA SERIALLY_REUSABLE

CREATE OR REPLACE PACKAGE pkg_example AS
    PRAGMA SERIALLY_REUSABLE;
    
    PROCEDURE my_proc;
END pkg_example;
/
```

---

## ORA-06550: line X, column Y:

### Error Message
```
ORA-06550: line X, column Y:
PLS-XXXXX: <error message>
```

### Solution
- Check line X, column Y in code
- Verify SQL/PL/SQL syntax
- Check for undefined variables
- Verify object privileges

```plsql
-- Example: undefined variable
DECLARE
BEGIN
    DBMS_OUTPUT.PUT_LINE(v_undefined_var);  -- ORA-06550
END;
/

-- Fix: Declare variable
DECLARE
    v_undefined_var VARCHAR2(100);
BEGIN
    DBMS_OUTPUT.PUT_LINE(v_undefined_var);
END;
/
```

---

## Best Practices for Error Handling

### 1. Always use Exception Handlers
```plsql
BEGIN
    -- Main code
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        -- Handle no data
    WHEN DUP_VAL_ON_INDEX THEN
        -- Handle duplicate
    WHEN OTHERS THEN
        -- Handle all other errors
END;
/
```

### 2. Log Errors Properly
```plsql
CREATE TABLE error_log (
    error_id NUMBER PRIMARY KEY,
    error_code NUMBER,
    error_msg VARCHAR2(4000),
    stack_trace CLOB,
    created_date DATE
);

BEGIN
    -- code
EXCEPTION
    WHEN OTHERS THEN
        INSERT INTO error_log(error_code, error_msg, stack_trace)
        VALUES(SQLCODE, SQLERRM, DBMS_UTILITY.format_error_backtrace);
        RAISE;
END;
/
```

### 3. Use Savepoints for Rollback
```plsql
BEGIN
    SAVEPOINT sp1;
    -- Process item 1
    INSERT INTO items VALUES(1, 'ITEM1');
    
    SAVEPOINT sp2;
    -- Process item 2
    INSERT INTO items VALUES(2, 'ITEM2');
    
    -- If error in item 2
    ROLLBACK TO sp2;  -- Only rolls back item 2
    
    COMMIT;
END;
/
```
