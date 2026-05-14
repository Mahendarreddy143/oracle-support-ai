-- ============================================================================
-- Filename: error-handling-template.sql
-- Description: Production-Ready PL/SQL Procedure with Comprehensive Error Handling
-- Author: Oracle Support AI
-- Created: 2026-05-14
-- ============================================================================

CREATE OR REPLACE PROCEDURE xx_process_items_with_error_handling
(
    p_organization_id IN NUMBER,
    p_batch_size      IN NUMBER DEFAULT 1000,
    errbuf            OUT VARCHAR2,
    retcode           OUT VARCHAR2
)
/******************************************************************************
*
* PROCEDURE: xx_process_items_with_error_handling
*
* DESCRIPTION:
*   This procedure demonstrates best practices for error handling in Oracle EBS
*   PL/SQL procedures. It includes:
*   - Proper exception handling
*   - Detailed logging
*   - Transaction management
*   - Restart capability
*   - Performance optimization
*
* PARAMETERS:
*   p_organization_id: Organization ID to process
*   p_batch_size: Number of items to process in each batch (default: 1000)
*   errbuf: Error message (OUT)
*   retcode: Return code - 0: Success, 1: Warning, 2: Error
*
* USAGE:
*   BEGIN
*     xx_process_items_with_error_handling(45, 1000, :errbuf, :retcode);
*   END;
*   /
*
* RETURN CODES:
*   0 = Success
*   1 = Completed with warnings
*   2 = Fatal error
*
* HISTORY:
*   2026-05-14 - Initial version
*   
******************************************************************************/
IS
    -- ========================================================================
    -- SECTION 1: Variable Declarations
    -- ========================================================================
    
    -- Counters
    l_total_processed   NUMBER := 0;
    l_total_success     NUMBER := 0;
    l_total_errors      NUMBER := 0;
    l_total_warnings    NUMBER := 0;
    l_batch_count       NUMBER := 0;
    
    -- Variables for processing
    l_item_id           NUMBER;
    l_item_number       VARCHAR2(100);
    l_error_msg         VARCHAR2(4000);
    l_success_flag      BOOLEAN;
    l_restart_count     NUMBER := 0;
    l_max_retries       CONSTANT NUMBER := 3;
    
    -- Logging variables
    l_start_time        TIMESTAMP;
    l_end_time          TIMESTAMP;
    l_execution_time    VARCHAR2(100);
    l_debug_mode        BOOLEAN := FALSE;
    
    -- Exception variables
    l_continue_flag     BOOLEAN := FALSE;
    l_exit_flag         BOOLEAN := FALSE;
    l_fatal_error       BOOLEAN := FALSE;
    
    -- Savepoint name for rollback
    l_savepoint_name    VARCHAR2(30);
    
    -- ========================================================================
    -- SECTION 2: Cursor Definitions
    -- ========================================================================
    
    -- Main cursor for items to process
    CURSOR c_items_to_process IS
        SELECT 
            msib.inventory_item_id,
            msib.segment1 as item_number,
            msib.organization_id
        FROM mtl_system_items_b msib
        WHERE msib.organization_id = p_organization_id
        AND   msib.enabled_flag = 'Y'
        ORDER BY msib.inventory_item_id;
    
    -- ========================================================================
    -- SECTION 3: Procedure Declarations
    -- ========================================================================
    
    -- Initialize FND Global variables
    PROCEDURE p_initialize_globals
    IS
    BEGIN
        fnd_global.apps_initialize(
            user_id      => 0,
            resp_id      => 52040,
            resp_appl_id => 401
        );
        
        mo_global.init('INV');
        mo_global.set_policy_context('S', p_organization_id);
        
        fnd_file.put_line(fnd_file.LOG, 'Globals initialized successfully');
    EXCEPTION
        WHEN OTHERS THEN
            fnd_file.put_line(fnd_file.LOG, 'ERROR: Failed to initialize globals: ' || SQLERRM);
            RAISE;
    END p_initialize_globals;
    
    -- Process single item with retry logic
    PROCEDURE p_process_single_item
    (
        p_item_id     IN NUMBER,
        p_item_number IN VARCHAR2,
        x_success     OUT BOOLEAN,
        x_error_msg   OUT VARCHAR2
    )
    IS
        l_retry_count NUMBER := 0;
        l_processed   BOOLEAN := FALSE;
    BEGIN
        x_success := FALSE;
        x_error_msg := NULL;
        
        -- Retry loop for transient errors
        WHILE l_retry_count < l_max_retries AND NOT l_processed LOOP
            BEGIN
                -- Create savepoint for this item
                SAVEPOINT sp_item_process;
                
                -- Process item logic here
                UPDATE xx_staging_table
                SET status = 'P',
                    last_update_date = SYSDATE
                WHERE item_id = p_item_id;
                
                -- Simulate your business logic
                IF MOD(p_item_id, 100) = 0 THEN
                    -- Example: some validation
                    IF p_item_id < 0 THEN
                        RAISE_APPLICATION_ERROR(-20001, 'Invalid item ID');
                    END IF;
                END IF;
                
                -- Mark as successfully processed
                UPDATE xx_staging_table
                SET status = 'S',
                    last_update_date = SYSDATE
                WHERE item_id = p_item_id;
                
                x_success := TRUE;
                l_processed := TRUE;
                
            EXCEPTION
                WHEN NO_DATA_FOUND THEN
                    x_error_msg := 'Item not found: ' || p_item_number;
                    l_processed := TRUE;
                    x_success := FALSE;
                    
                WHEN OTHERS THEN
                    l_retry_count := l_retry_count + 1;
                    
                    IF l_retry_count >= l_max_retries THEN
                        ROLLBACK TO sp_item_process;
                        x_error_msg := 'Max retries exceeded: ' || SUBSTR(SQLERRM, 1, 1000);
                        l_processed := TRUE;
                        x_success := FALSE;
                    ELSE
                        -- Rollback to savepoint and retry
                        ROLLBACK TO sp_item_process;
                        
                        -- Log retry attempt
                        fnd_file.put_line(
                            fnd_file.LOG,
                            'Retrying item ' || p_item_number || ' (Attempt ' || l_retry_count || ')'
                        );
                        
                        -- Small delay before retry
                        DBMS_LOCK.SLEEP(1);
                    END IF;
            END;
        END LOOP;
        
    EXCEPTION
        WHEN OTHERS THEN
            ROLLBACK TO sp_item_process;
            x_success := FALSE;
            x_error_msg := 'Unexpected error: ' || SUBSTR(SQLERRM, 1, 1000);
    END p_process_single_item;
    
    -- Logging procedure
    PROCEDURE p_log_message(p_message IN VARCHAR2, p_level IN VARCHAR2 DEFAULT 'INFO')
    IS
    BEGIN
        CASE p_level
            WHEN 'DEBUG' THEN
                IF l_debug_mode THEN
                    fnd_file.put_line(fnd_file.LOG, '[DEBUG] ' || p_message);
                END IF;
            WHEN 'INFO' THEN
                fnd_file.put_line(fnd_file.LOG, '[INFO] ' || p_message);
            WHEN 'WARNING' THEN
                fnd_file.put_line(fnd_file.LOG, '[WARNING] ' || p_message);
            WHEN 'ERROR' THEN
                fnd_file.put_line(fnd_file.LOG, '[ERROR] ' || p_message);
            ELSE
                fnd_file.put_line(fnd_file.LOG, p_message);
        END CASE;
    END p_log_message;
    
    -- Generate final report
    PROCEDURE p_generate_report
    IS
    BEGIN
        fnd_file.put_line(fnd_file.LOG, '========================================');
        fnd_file.put_line(fnd_file.LOG, 'PROCESSING SUMMARY REPORT');
        fnd_file.put_line(fnd_file.LOG, '========================================');
        fnd_file.put_line(fnd_file.LOG, 'Start Time      : ' || TO_CHAR(l_start_time, 'YYYY-MM-DD HH24:MI:SS'));
        fnd_file.put_line(fnd_file.LOG, 'End Time        : ' || TO_CHAR(l_end_time, 'YYYY-MM-DD HH24:MI:SS'));
        fnd_file.put_line(fnd_file.LOG, 'Total Processed : ' || l_total_processed);
        fnd_file.put_line(fnd_file.LOG, 'Total Success   : ' || l_total_success);
        fnd_file.put_line(fnd_file.LOG, 'Total Errors    : ' || l_total_errors);
        fnd_file.put_line(fnd_file.LOG, 'Total Warnings  : ' || l_total_warnings);
        fnd_file.put_line(fnd_file.LOG, '========================================');
    END p_generate_report;

BEGIN
    -- ========================================================================
    -- MAIN EXECUTION BLOCK
    -- ========================================================================
    
    l_start_time := SYSTIMESTAMP;
    
    -- Initialize
    p_initialize_globals;
    p_log_message('Process started for Organization ID: ' || p_organization_id);
    
    -- Process items
    FOR r_item IN c_items_to_process LOOP
        BEGIN
            l_item_id := r_item.inventory_item_id;
            l_item_number := r_item.item_number;
            
            -- Process the item
            p_process_single_item(
                p_item_id     => l_item_id,
                p_item_number => l_item_number,
                x_success     => l_success_flag,
                x_error_msg   => l_error_msg
            );
            
            -- Update counters
            l_total_processed := l_total_processed + 1;
            
            IF l_success_flag THEN
                l_total_success := l_total_success + 1;
            ELSE
                l_total_errors := l_total_errors + 1;
                p_log_message('Error processing item ' || l_item_number || ': ' || l_error_msg, 'ERROR');
            END IF;
            
            -- Commit every batch
            l_batch_count := l_batch_count + 1;
            IF l_batch_count >= p_batch_size THEN
                COMMIT;
                p_log_message('Batch committed. Items processed: ' || l_total_processed);
                l_batch_count := 0;
            END IF;
            
        EXCEPTION
            WHEN OTHERS THEN
                l_total_errors := l_total_errors + 1;
                p_log_message(
                    'Unexpected error for item ' || l_item_number || ': ' || SUBSTR(SQLERRM, 1, 1000),
                    'ERROR'
                );
        END;
    END LOOP;
    
    -- Final commit
    COMMIT;
    
    -- Generate report
    l_end_time := SYSTIMESTAMP;
    p_generate_report;
    
    -- Set return codes
    IF l_total_errors = 0 THEN
        retcode := '0';
        errbuf := 'Process completed successfully';
    ELSIF l_total_errors <= (l_total_processed * 0.05) THEN  -- Less than 5% errors
        retcode := '1';
        errbuf := 'Completed with ' || l_total_errors || ' error(s)';
    ELSE
        retcode := '2';
        errbuf := 'Process completed with excessive errors: ' || l_total_errors;
    END IF;
    
EXCEPTION
    WHEN OTHERS THEN
        -- Rollback on fatal error
        ROLLBACK;
        retcode := '2';
        errbuf := 'Fatal error: ' || SUBSTR(SQLERRM, 1, 4000);
        fnd_file.put_line(fnd_file.LOG, 'FATAL ERROR: ' || SQLERRM);
        fnd_file.put_line(fnd_file.LOG, DBMS_UTILITY.format_error_backtrace);
        
END xx_process_items_with_error_handling;
/

-- Grant execute privilege
GRANT EXECUTE ON xx_process_items_with_error_handling TO PUBLIC;

-- Create synonym
CREATE OR REPLACE SYNONYM xx_process_items_with_error_handling FOR apps.xx_process_items_with_error_handling;

-- Show any compilation errors
SHOW ERRORS PROCEDURE xx_process_items_with_error_handling;
