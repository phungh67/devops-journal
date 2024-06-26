# Back to navigator: [Table of contents ](Journal%20001%253A%20DevOps%20101.md)
# Back to main topic: [Section 2](How%20to%20setup%20a%20HA%20database%20cluster.md)

  # 1. Database replication
  Refer to replication on context of database: 
  > Replication in the database context refers to the process of copying and maintaining database objects, such as tables, schemas, and entire databases, across multiple database servers or instances. This ensures that the data is consistently available in multiple locations, which can be used for various purposes such as improving data availability, fault tolerance, load balancing, and disaster recovery.

  > Replication enables data from one MySQL database server (known as a source) to be copied to one or more MySQL database servers (known as replicas). Replication is asynchronous by default; replicas do not need to be connected permanently to receive updates from a source. Depending on the configuration, you can replicate all databases, selected databases, or even selected tables within a database.
  [MySQL documentation](https://dev.mysql.com/doc/refman/8.4/en/replication.html)

  **To be short:** Replication is a process that make all your database server always have the same dataset at any point of time.

  # 2. Ways of replication
  Assume that we use InnoDB, which engine the famous ``MySQL`` used. This will refer 2 methods that are widely used to replicate data.
  - Bin log replication.
  - Global transaction ID replication (GTID).
  
  # 2.1 Bin log way
  - **What is the bin log?**
  Bin log is short called of binary log, a file (in text form, encoded) that contains all recored of activity of a database. These activity includes: ``DELETE``, ``UPDATE``, ``CREATE``, ``ALTER`` and ``INSERT`` or even ``DROP``.
  The bin log acts as a source for recovering, replicating and even auditing.
  - **Form of bin log**
  It has 3 types of form: 
    - Statement-based logging: Logged SQL statement into file, exclude read-only or dropped transaction. Convenient with transaction that apply to a large number of rows, columns and tables.
    - Row-based logging: Logged actual data changes (the affected rows). Will product a large data for bin log.
    - Mixed: contain statement-based and row-based. Server will decide when to use row or statement.
  - **Must set rule to rotate, remove or archive binlog for storage space**
  # 2.2 Global transaction ID
  - **Definition**
  It is a unique identifier assigned to each transaction that is commited in a MySQL database. This is globally, so it is very easy to tracked across all nodes. Format of this ID: ``UID_of_machine:ID_of_transaction``. When an ID is assined to a transaction, it can not be changed, with this, consistency is ensure.
  - **Life cycle**
  ![gtid-life-cycle](../Figures/gtid-lifecycle.jpg)

  - **Sample configuration**
    ```conf
    [mysqld]
    log-bin                         = mysql-bin
    server-id                       = 1
    port                            = 13306
    bind-address                    = 0.0.0.0
    binlog-format                   = row
    gtid_mode                       = on
    enforce-gtid-consistency        = on
    ```

  - **Result**
    ```sql
    mysql> SHOW VARIABLES LIKE '%gtid%';
    +----------------------------------+-------------------------------------------+
    | Variable_name                    | Value                                     |
    +----------------------------------+-------------------------------------------+
    | binlog_gtid_simple_recovery      | ON                                        |
    | enforce_gtid_consistency         | ON                                        |
    | gtid_executed                    | 50521d8a-339c-11ef-a1b9-005056b1a635:1-22 |
    | gtid_executed_compression_period | 0                                         |
    | gtid_mode                        | ON                                        |
    | gtid_next                        | AUTOMATIC                                 |
    | gtid_owned                       |                                           |
    | gtid_purged                      |                                           |
    | session_track_gtids              | OFF                                       |
    +----------------------------------+-------------------------------------------+
    9 rows in set (0.29 sec)
    ```
  # Back to [top](#back-to-navigator-table-of-contents)