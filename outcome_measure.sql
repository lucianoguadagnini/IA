-- Module 8 Practice - Exercise 2a, the outcome measure.
-- Reproducible by anyone with report access to the ServiceNow credentialing
-- table (exported to the reporting database). Two timestamps are mandatory
-- and non-editable after they are set: received_at (intake step) and
-- enabled_at (last of the 4 enablement systems). Withdrawn files are
-- reported separately, never silently excluded.
--
-- Parameters:  :cohort_start, :cohort_end  (files received in the window)
--              :baseline_start, :baseline_end

-- 1. Primary measure: on-time rate and p90 for the cohort ------------------
WITH files AS (
    SELECT
        number,
        received_at,
        enabled_at,
        withdrawn_at,
        DATEDIFF(day, received_at, enabled_at) AS elapsed_days
    FROM u_credentialing
    WHERE received_at >= :cohort_start
      AND received_at <  :cohort_end
),
closed AS (
    SELECT * FROM files WHERE enabled_at IS NOT NULL
)
SELECT
    COUNT(*)                                                    AS files_closed,
    SUM(CASE WHEN elapsed_days <= 30 THEN 1 ELSE 0 END) * 1.0
        / COUNT(*)                                              AS on_time_rate,
    AVG(elapsed_days * 1.0)                                     AS avg_days,
    PERCENTILE_CONT(0.90) WITHIN GROUP (ORDER BY elapsed_days)  AS p90_days,
    (SELECT COUNT(*) FROM files WHERE withdrawn_at IS NOT NULL) AS withdrawn,
    (SELECT COUNT(*) FROM files
      WHERE enabled_at IS NULL AND withdrawn_at IS NULL)        AS still_open
FROM closed;

-- 2. Volume guard: cohort intake vs. baseline intake -----------------------
SELECT
    (SELECT COUNT(*) FROM u_credentialing
      WHERE received_at >= :cohort_start AND received_at < :cohort_end)
        AS cohort_volume,
    (SELECT COUNT(*) FROM u_credentialing
      WHERE received_at >= :baseline_start AND received_at < :baseline_end)
        AS baseline_volume;
-- Falsifier fires if cohort_volume < 0.8 * baseline_volume (normalised to
-- window length): a faster number driven by less work does not count.

-- 3. Anti-gaming guard: verification defect rate --------------------------
-- u_credentialing_audit holds the monthly blind re-review of a 10% random
-- sample by a senior verifier who did not work the file.
SELECT
    DATE_TRUNC('month', reviewed_at)                                AS month,
    COUNT(*)                                                        AS sampled,
    SUM(CASE WHEN material_error = 1 THEN 1 ELSE 0 END) * 1.0
        / COUNT(*)                                                  AS defect_rate
FROM u_credentialing_audit
WHERE reviewed_at >= :baseline_start
GROUP BY DATE_TRUNC('month', reviewed_at)
ORDER BY month;
-- Falsifier fires if any cohort month exceeds the baseline defect rate by
-- more than one percentage point.

-- 4. Per-step waits, so a miss can be attributed to a step ----------------
SELECT
    step_name,
    AVG(DATEDIFF(day, prev_step_completed_at, step_started_at) * 1.0) AS avg_wait_days,
    AVG(working_minutes * 1.0)                                          AS avg_working_min
FROM u_credentialing_steps
WHERE received_at >= :cohort_start AND received_at < :cohort_end
GROUP BY step_name
ORDER BY avg_wait_days DESC;
