# ElasticSearchSnapshotting
This script can be set in a cron job in any of the nodes to take a snapshot of an elastic search cluster and delete the older snapshots. Also email notification is used to notify in case of failure.

To use this script, 
1. Setup a elasticsearch snapshot repo.
2. Register the repo with the cluster.
3. Rename the repo name in the script as registered.
Reference : https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-snapshots.html
