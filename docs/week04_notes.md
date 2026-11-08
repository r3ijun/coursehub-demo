# CourseHub - Buoi 4

- Migration 001: enrollment_events.
- Demo class: RACE-01, capacity = 1.
- POST /enrollments: lock class_sections bang FOR UPDATE.
- Concurrency test: 1 request 201, 1 request 409.
- Performance data: 100000 rows, dataset=performance.
- Index: idx_enrollment_events_dataset_student_time.

## Ket qua do EXPLAIN (ANALYZE, BUFFERS)
- Truoc khi tao Index (Before INDEX):
  - Scan type: Seq Scan on enrollment_events + Sort (top-N heapsort, Memory: 31kB).
  - Rows Removed by Filter: 99181 (actual rows = 820 -> Limit 50).
  - Buffers: shared hit=1137.
  - Planning Time: 1.234 ms.
  - Execution Time: 5.689 ms.
- Sau khi tao Index (After INDEX):
  - Scan type: Index Scan using idx_enrollment_events_dataset_student_time (khong can Sort).
  - Rows Removed by Filter: 0 (doc dung 50 dong theo Index Cond).
  - Buffers: shared hit=53.
  - Planning Time: 0.113 ms.
  - Execution Time: 0.109 ms.