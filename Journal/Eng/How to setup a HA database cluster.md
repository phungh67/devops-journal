#Database
  # Back to navigator: [Table of contents ](https://github.com/phungh67/devops-database)
  # Pre-requisiste: [Replication method](What%20is%20replica.md)
  # 1. Database problem
  As usual, database is used to store a large amount of data. In general programming, or "playground" coding, we are care little about database, because that only needs some variables, arrays or something. But in the production environment, data is stored to a database.
  Monitoring and provisioning database is a critical process can take about 40% percent of an application succession. The role for this job is called DBA, database administrator, but now, database administration not only DBA's responsible, it falls to DevOps engineer.
  # 2. Database replication
  There are some criteria that need to ensure about database.
  - It must be high availability, which means, if a disaster occurs, the database server will still online to handle requests from clients.
  - Data consistency, even if server is down and recovered after that, data will not be lost (and should not be overwritten by false value too).
  
  So, what's exactly "database replication"?
  **Replication**: is a process that every data will be copy synchronously or asynchronously for a source to a number of replicas and, in that process, all server (source and replicas) must have the same dataset. Every transaction (or changes) that executed on source (or writer) must been replicated on every nodes too.

  There are a number of ways to replicate a database, but which to choose depend on the application and infrastructure as well. Here is a list of commonly used replication method.
    - Master - slave replication: This replication is the domaint way of database replicating method with a master and many slaves. Asynchronous is usually implement.
    - Multi master replication: Many masters and slaves. Write operation can be executed on any masters, with a little delay (all master should be acknowldeged the transaction before applying it), all will be commit as usual.
    - NDB: To-be-added
  
  Furthermore, we can classify replication method with protocol, like synchronous and asynchronous, semi-synchronous,...

  Into the deep of replica model...

  ## 2.1 Master - slave model
  **Definition** This is the most dominated model in morden day. It consists 1 master server act as the source and responsible for write opertaion. Any replicas will be used for read only operation.

  ![mysql-replica-master-slave](../Figures/database-master-slave.jpg)

  As the illustrated above, the master node wil "extract" all the upcoming transaction (which have been executed successfully and written to log) to binlog file. The replicas will try to retrieve the bin log from master (after a short delay since it is asynchronous) and pass it to relay log. SQL thread of replica will read the relay log, replay the transaction and apply it. The replica will send a notification to master that it has completed the replication progress.
  Important parameters to monitor in replication progress:
    ``second_behind_master`` or ``replica_lag``: indicate the position of "current" slave with current position of master. When replication progress is happening, the replica will read the relay log from a specific position of a specific binlog file setup earlier, it will compare with current position of binlog from master to begin replicating. Second behind is zero means the replicas have the dame dataset with master.

  **Pros:**
  - Easy to setup, since only one master, all setup across replicas will point to that one, no needs to worry about command, syntax,...
  - Provide a reliable setup of replication, all data in master/source will be copied and executed into replicas after a short delay (asynchronous) or nearly immediately (synchronous).
  - High performance for read operation.
  
  **Cons:**
  - Single point of failure, if the master is donw, there is a small (or large) downtime, all depends on how quickly a replica is promoted to master.
  - As a result, data in the period from master down to new master promoted is lost (if client continues sending new data). And, when the "old" master rejoins the cluster, the "unexpected" data it received before crashing is still present.
  
  Till now, master slave is still the dominant method of database replication because it is reliable and suited for many kind of applcation.

  ---

  **Configuration**
  This is the instruction to setup replication between two server, 1 master and 1 replica.

  - Turn of writing on all databases, if this is "fresh", "just installed" database, this step is not necessary. 
    ```SQL
    SET @@GLOBAL.read_only = ON;
    ```
    This command with ensure all on-going transaction will be commited (finish) or rollback and no further transaction will happen.
  - For better preparation, shut down the database as well, can use ``mysqladmin`` of simply the ``service`` command of Linux OS.
  - Edit the configuration file of MySQL service as the following, adding options are not necessary but add it depends on user's need.
    ```conf
    [mysqld]
    bind-address                  = 0.0.0.0   # allow MySQL bound to all interface or just public IP for external reach
    port                          = 13306     # custom port of MySQL
    log_error                     = /var/log/mysql/error.log  # location of error log
    log-bin                       = mysql-bin                 # prefix of MySQL bin log
    server-id                     = 1                         # set the server unique id, mandatory with binlog replication
    binlog-format                 = row                       # can be set as statement or mixed
    gtid_mode                     = on                        # replica with GTID
    enforce-gtid-consistency      = on                        # ensure GTID consistency, all ID will be applied only once
    ```
    - The above configuration is a sample for setup two MySQL server in master-salve architecture. Replica is done by using GTID method
  
  ## 2.2. Multi-master model
  **Definition** This method allows multi write to multi master at a time. With this feature, longer respond time is oblivious. Every time a write from client is executed on a master, all the remaining masters will receive that transaction as well, when all masters apply successfully, they will send "ack signal" (acknowledgement) to original master (which received the transaction), after that, transaction is considered as commited.

  ![multi-master-architecture](../Figures/multi-master.jpg)

  In above illustrator, a master will have a set of replicas with the same role as single "master-slave" model. All read will be preformed in replica set.

  **Pros**
  - This model is suited for collaboration platform where handles multi write requests at the same time but requests consistency. Some famous examples are: Git, Office 365, Google Docs,...
  - A transaction will be considered as successfully executed when all nodes acknowledge it and applied it, data consistency of this model is higher than single master model. At any time, all servers always have the same dataset.
  - High performance of write operation.
  
  **Cons**
  - "Split brain" is a common case in this architecture. When a master is down, cluster will continue working as usual but when the node is healthy again and rejoin the cluster, if it have more data than the exisiting dataset, conflict will happen.
  - Increase point of failure, when many master nodes are reside at the same subnets (virtual) or same data center (physical), chance of system down is increased.
  - High respond time. Because it is requires all nodes to acknowledge transaction, respond time will increase rapidly. It will likely increase as a multipler of the number of master node.
  
  ---

  **Configuration**
  This configuration is for setting up a master-master relationship between two MySQL servers. Server 1 will be master and slave of server 2. Server 2 will be master ans slave of server 1.

  - As the same as single master, the first step is stop all on-going transaction, take a backup (for recovery) and shutdown the database.
  - Setup these parameters in configuration file
    - master 1:
        ```conf
        [mysqld]

        server-id               = 1
        log-bin                 = "mysql-bin"
        relay-log               = "mysql-relay-log"
        auto-increment-increment= 2
        auto-increment-offset   = 1
        replicate-same-server-id= 0
        net_read_timeout        = 5000
        net_write_timeout       = 5000
        ```
    - master 2:
        ```conf
        [mysqld]

        server-id               = 2
        log-bin                 = "mysql-bin"
        relay-log               = "mysql-relay-log"
        auto-increment-increment= 2
        auto-increment-offset   = 2
    replicate-same-server-id= 0
        net_read_timeout        = 5000
        net_write_timeout       = 5000
        ```
    
  - There are some parameters that needs to be paid attention to.
    - First: ``server-id`` this is some sort of ID of server, help server indetifies each other.
    - Second: ``auto-increment-increment`` this is an important parameter. All transaction will be indexed in binlog and their id must be different, if not, collision will happen. For example, between 2 master, 1 master will write records with id: 1,3,5,7 and the other will be 2,4,6,8, otherwise, replication process will be corrupt (due to overwrite). Along with this parameter is ``auto-increment-offset`` is the step between 2 records (in a server).
    - Last: ``replicate-same-server-id``  avoid loop in replication. Does not replicate records that originate from same server
  
  # 2.3. Multi master wil Galera cluster
  In mutli-master scenario, "split-brain" is a common error. Moreover, conflict between nodes must be resolve (this will likely happend when a transaction is not complete but another write request is sent to master nodes). To aviod these errors, some work-around from DBA is necessary, or some tools, solutions can resolve this.
  One of the common tool to overcome these errors is Galera.
  Galera is a cluster control tool which can control MySQL servers and transforms MySQL cluster into a real multi-master cluster in nearly synchronous way.

  ![glalera-work](../Figures/galera-workflow.jpg)

  Galera works base on "certificate-base-replication". As in above illustration, everytime a transaction comes from client, it will be put into a writeset, where it will be inspected carefully and all nodes will perform analysis process to make sure if this transaction is applied, it will not cause any conflict across the cluster, after approved by all nodes, the server (which originally receive this request) will commit it and response back to client.
  This method will avoid "split brain" and "conflict" of multi-master scenario.

  Galera does not use binlog nor GTID, it uses WSREP (writeset replica).

  ![write-set-replica](../Figures/galeara-cluster.jpg)

  ---

  **Configuration**
  ```conf
    [mysqld]
    binlog_format                   = ROW
    default-storage-engine          = innodb
    innodb_autoinc_lock_mode        = 2
    bind-address                    = 0.0.0.0                                               # listening address, can be public IP
    port                            = 13306                                                 # mysql port, re-map to avoid conflict with HA proxy

    # Galera Provider Configuration
    wsrep_on                        = ON
    wsrep_provider                  = /usr/lib/galera/libgalera_smm.so

    # Galera Cluster Configuration
    wsrep_cluster_name              = "mysql-cluster"                                       # custom name for cluster
    wsrep_cluster_address           = "gcomm://172.16.98.102,172.16.98.103,172.16.98.104"   # a set of all node's IPs

    # Galera Synchronization Configuration
    wsrep_sst_method                = rsync

    # Galera Node Configuration
    wsrep_node_address              = "172.16.98.102"                                       # current node's address
    wsrep_node_name                 = "mysql-node-001"                                      # current node's name
  ```

  # 3. NDB with MySQL

  Sketch of NDB with 4 data nodes and 2 mysql nodes

  ```sql
      +---------------------+
      | Management Node (MGM)|
      +---------------------+
               |
               v
      +---------------------+
      |       Network       |
      +---------------------+
               |
               v
      +--------------------+    +--------------------+
      |    SQL Node        |    |     SQL Node       |
      | (MySQL Server)     |    |  (MySQL Server)    |
      +--------------------+    +--------------------+
                 |                     |
                 v                     v
          +---------------------+ +---------------------+
          |     Data Node 1     | |     Data Node 2     |
          |       (NDBD)        | |       (NDBD)        |
          +---------------------+ +---------------------+
                    |                     |
                    v                     v
          +---------------------+ +---------------------+
          |     Data Node 3     | |     Data Node 4     |
          |       (NDBD)        | |       (NDBD)        |
          +---------------------+ +---------------------+
  ```

  Components of NDB (Network database)
  - **Management node - MGM**: Does not contain any data itself, manages configuration and monitoring the cluster. Handle node failure, start, stop node, provide interface for administrator tasks. The daemon ``ndb_mgmd``
  - **Data node - NDBD**: Storing and managing the data in the cluster. There are two ways of storing data, on disk or on memory, on disk is recommend if the dataset is large, internal memory is expensive to use for this kind of tasks. This node will handle data distribution, data partitioning, data replicating,... The daemon of this node ``ndbd`` of ``ndbmtd`` depends on version of NDB software.
  - **Mysql node - MYSQLD**: This node with MYSQL client install is repsonsible for connection from application. The daemon ``mysqld``.
  - **API node**: This node allow direct API call to database without using SQL, depends on situation to construct this node.
  
  ## 3.1. Data storage/ partition/ fragement in NDB

  Data in NDB is stored into partition (or fragemented).
  - A table with its data will be distributed across all nodes of cluster. The primary key of table will determine which partition go to which node.
  - For example, if the database has 1 table and 3 nodes, each node will container one-of-third of the table.
  - NDB is redundancy, which means in every node, a replica of other nodes are present. This diagram will illustrate more clearly:
  ```sql
  +----------------+     +----------------+     +----------------+     +----------------+
  |    Node N1     |     |    Node N2     |     |    Node N3     |     |    Node N4     |
  |                |     |                |     |                |     |                |
  |  Fragment 1    |<--> |  Fragment 2    |<--> |  Fragment 3    |<--> |  Fragment 4    |
  |  (Primary)     |     |  (Primary)     |     |  (Primary)     |     |  (Primary)     |
  |  Fragment 4    |     |  Fragment 1    |     |  Fragment 2    |     |  Fragment 3    |
  |  (Secondary)   |     |  (Secondary)   |     |  (Secondary)   |     |  (Secondary)   |
  +----------------+     +----------------+     +----------------+     +----------------+
  ```

  - A specific table is divided into 4 fragements, each will lie on a node of this cluster and this will have an additionaly replica in other node (in production, almost every node all have replica of other nodes).
  - When node N1 is down and fragement 1 is lost, the management node will handle fail over process, the replica on node N2 will take over the role as the main data of fragement 1, ensure no data losing.
  
  ## 3.2 Data storage mechanism
  - Location: data is stored on data node of cluster.
  - Data can be stored both in-memory and on disk.
  - It is further divided into these components:
    - **Memory buffer**: ``DataMemory`` stores actual data rows and ``IndexMemory`` stores indexes.
    - **Disk storage**: ``DataDisk`` for storing huge size data, ``RedoLogs`` captures all changes to the data for recovering purpose, ``UndoLogs`` for rolling back transactions in case failure.
  
  ## 3.3 Advantages and disadvantages
  
  **Adavantages**
  - *High availability*: Data is replicated across all nodes, if failure occurs, data is not losing.
  - *Automatic failove*: Because of data partitioning, if a node fails, another node can take up the down node immediately with exactly the same dataset.
  - *Scalability*: More nodes can be added into cluster to improve performance. Traffic between nodes can be handle in a distributed way.
  - *Performance*: With in-memory storage, accessing to data takes less time.
  - *Fault tolerance*: Data is redundancy, always available and cosistent.
  - *Distribution*: Can be setup across multi datacenter.
  
  **Disadvantages**
  - *Complexity*: It is hard to setup and maintenance with a number of nodes to monitor which with different roles and hardware requirements.
  - *Resource consumption*: Require bandwidth to communicate with other nodes, with MySQL node and with management node. Require resources for in-memory storage, and disk space if data set becomes too large.
  - *Limited support*: It is not InnoDB or MyISAM enine.

  # 4. How to setup a "real" database cluster
  This section will guide you how to setup a simple database cluster to connect with our CURD application on [section 1](Construct%20a%20simple%20CRUD%20application%20from%20scratch.md). This database will act as a single source to store user data, application data, etc, ...
  
  To bring it as closer as production environment, HA proxy and keepalive are used too.

  To read more about HA proxy (a brief, to know what is it, how's it working and how to config it in a simple way), please refer to this:

  To read about keepalived, a software to help fail-over process and create a VIP (Virtual IP), please refer to this:

  ## 4.1. Preparation
  That's it, prepare your VMs for constructing a new database cluster on your own.

  For best practice, you can create with EC2 (from AWS) or with Oracle VMs, or Vargant, depends on your choice.

  Frist, install MySQL server.
  ```bash
  sudo apt update
  sudo apt install mysql-server
  sudo systemctl start mysql.server
  ```

  Second, configure for administrator user. This is mandatory if your want to perform the "best practice" method (which means, setup & config as you are working on a production environment with no expection, no stupid config).
  ```bash
  sudo mysql # this will log you in, with root privilege
  ```

  ```sql
  ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'password';
  ```

  Remember to use a strong password with at least 8 characters, upper case, lower case, number and special character.

  After that, using command ``quit`` to return to terminal

  Perform ``sudo mysql_secure_installation`` to complete MySQL installation. Remember to read carefully each line, each requirements and each instrucions given by MySQL shell.

  ## 4.2. Customize your SQL
  Because we're going to setup an HA cluster, which will come with a load balancer, a VIP (virtual IP) so that a problem comes: "Port conflict". The easiest way to solve this is: default port changing. To do so, modify configuration file of MySQL is enough.

  ```bash
  sudo vim /etc/mysq/my.cnf

  [mysqld]

  server-id               = 1                       # indentical for server ID
  log-bin                 = "mysql-bin"             # bin log prefix
  relay-log               = "mysql-relay-log"       # relay log for replication
  bind-address            = 0.0.0.0                 # bin port, because MySQL bind to localhost by default
  port                    = 13306                   # change listening port to 13306
  ```

  The below configuration is about to setup a master server with ``server-id=1``. The best way to illustrate is learn how to setup a simple cluster with 1 master and 1 replica and the above is how to setup a master. If you want to get the configuration file, please refer to [this file](../MySQL/my.cnf), you will find that ``my.cnf`` is also a blank file in ``/etc/mysql`` and yes, that is the file to hold your personal configuration without making any "wrong" changes to original configuration file.

  Assume that you have completed setup and restart successfully database with new configuration, if not, please ensure that you have ``[mysqld]`` at the top line, MySQL will not run if the configuration file does not begin with that clause.

  Next, make sure port ``13306`` is open and reachable.
  
  From replica machine, try this command
  ```bash
  telnet ip_address_of_master 13306
  ```
  If the command return successful code like ``press ^] to exit``, wola, you are good to go, if not, debug it.

  When the master is done, begin with replica. Becasue we have only 1 replica, this is quite simple. Repeat the process above to install MySQL, change root password and config, but this with different ``server-id``, you can assign 2 or 3, no matter with the number since we have only two servers.

  Now, this is the moment of truth, from the master, execute these commands:

  ```sql
  mysql> FLUSH TABLES WITH READ LOCK;
  ```

  This command ensure that all transactions after this command will not be permitted, because if transactions are still be made during replication setup, error will occur.

  **This guide is using binlog position as replica method, about GTID, check below section**

  After lock all tables, execute this command to know the current status of bin log (which file is currently processed and which position)

  ```sql
  mysql> SHOW BINARY LOG STATUS\G
  *************************** 1. row ***************************
             File: mysql-bin.000003
          Position: 73
          Binlog_Do_DB: test
          Binlog_Ignore_DB: manual, mysql
          Executed_Gtid_Set: 3E11FA47-71CA-11E1-9E33-C80AA9429562:1-5
  1 row in set (0.00 sec)
  ```

  For example, above command shows that binlog is currently at number 3 file with the position 73. The replica needs to know these information to estanblish replication process correctly. Remember to note down filename and position.

  A very **IMPORTANT** thing to know that, in replica process, username and password of replica use will be store as plain text, which means every one access to database can read and take over the control of that account. Minumum privilege is recommend.

  Using these commands to create a new user for replication purpose only with minimum privileges:
  ```sql
  mysql> CREATE USER 'repl'@'%.example.com' IDENTIFIED BY 'password';
  mysql> GRANT REPLICATION SLAVE ON *.* TO 'repl'@'%.example.com';
  ```
  The `%` indicates that the account `repl` can access the database from anywhere, you can specify subnet, or a specific IP at will, using `%` for the wildcard character.

  After the replication user is created, on slaves, execute these command:
  ```sql
  change master to 
  master_host='host_ip',
  master_user='replica_username',
  master_password='replica_user_password',
  master_port='host_mysqL_port',
  master_log_file='name_of_current_bin_log_file',
  master_log_pos='position_of_current_bin_log',
  get_master_public_key=1;
  ```

  If executed successfully, you can invoke the replication process by ``start slave``. Using command ``show slave status`` to monitor the process. If ``second_behind_master`` is zero, it can be considered as replication process are setup completed.

  But one important thing to know that: even ``second_behind_master`` drop to zero, it does not mean that every transactions executed on master are deliveried and applied to slaves. Many reasons to explain, network delay, disk high I/O, resources consumption,... ``second_behind_master`` just indicated that, every transactions that I/O thread in slaves have pulled to rely logs have been applied successfully. In order to ensure the replication on a 'production' environment, you should query some variables like `gtid-execution-set` on both master and slaves to ensure they are up-to-date.


  



  # Back to [top](#back-to-navigator-table-of-contents)