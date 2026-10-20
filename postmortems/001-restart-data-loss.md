Summary: After routine restart of shortener service, all previously created short links returned 404. The link data was lost.
Impact: Users saw 404s on links that had worked, 100% of them were affected and impact is permanent.
Timeline: 20:33:54 UTC: /g5im8A returns 307 (working)
~20:35 UTC: service restarted (Ctrl+C + rerun)
20:36:51 UTC: /g5im8A returns 404
Rootcause: The operating system frees the process memory and the links dictionary that lived on memory. The service had no durable storage so its state couldn't survive any restart, whether planned or a crash.
Detection: Found by manual testing after a restart. /healthz returned 200 the whole time and 404s are client's errors so a standard success rate sli wouldn't move
Resolution: Moved link storage to PostgresSQL in Docker on a persistent volume. Verified that a link survives both an app restart and database restart.
Action Items: Restart test, done (manual, 10/20). Lookup-miss metric and alert, open.
