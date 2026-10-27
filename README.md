Section 1: Project Title, Purpose, and Scope

Title: DistributedCyberPhysicalSystem

Purpose: Our project addresses the problem of having to SSH into the Sense HAT Pi to view the sensor readings. Using SSH requires users to run separate commands to view different readings and rerun those commands when they want to see updated data. Our Distributed Cyber-Physical System allows a user to see all data on the HMI Pi touchscreen in real time. This makes viewing data more convenient and allows users to easily check if the Sense HAT Pi is connected and communicating with the system. The system also saves the sensor readings for further viewing and analysis. The intended users are people who need to monitor sensor readings, observe changes in environmental conditions, and check connection status.

Scope: 

HMI Pi Role (Services hosted, UI role, data processing): Will display the sensor readings from the Sense HAT Pi on its touchscreen and show the connection status of the Sense HAT Pi. It processes, organizes, and stores each reading.

Sense HAT Pi Role (Sensors/actuators polled, daemons hosted): It collects environmental readings from its sensors and sends it to the HMI Pi through the classroom network.

Remote Storage / Infrastructure Role (NAS Database, MQTT Broker, or SFTP/SCP Server): Provide storage to sensor readings so that a users can access past readings. We will use a NAS database.

Optional Additional Nodes (Other Sandbox Table Pis or PLCs—note table consultation if applicable): N/A

Out-of-Scope Boundaries (List 1–2 features your team is intentionally excluding to ensure completion by Week 15): Prediction of environmental measurements and notification system

Section 3: Non-Functional Requirements

3.1 Unprivileged Socket Port Allocation

The project will use the following application ports: TCP port 5091 for sensor readings, UDP port 5092 for heartbeat messages, TCP port 5093 for commands and configuration, TCP port 5094 for sensor events and diagnostics, and TCP port 8090 for the Flask dashboard over HTTP. The HMI Pi will also use TCP port 5432 to connect to the remote PostgreSQL database on the classroom NAS.

All project application services shall use unprivileged ports between 1025 and 65535. Port assignments shall be maintained in a shared configuration file in the GitHub repository rather than hard-coded in multiple locations. SSH on port 22 shall be used only for system administration and shall not be used as an application data channel. No project application service shall bind to a privileged port at or below 1024.

3.2 Network Interface Management

The HMI Pi shall use its existing classroom network address, 192.168.5.92.

The Sense HAT Pi shall use its existing classroom network address, 192.168.5.93.

Project services shall not change the eth0 IP configuration, default route, or network bridging.

The wlan0 interface shall remain unchanged and shall not carry project traffic.

SSH access to both Raspberry Pis shall remain available during normal project operation.

3.3 Classroom LAN Confinement

Project communication shall be restricted to the classroom subnet 192.168.5.0/24.

Services shall communicate only with configured project nodes and the confirmed NAS address.

The system shall not perform network discovery, port scanning, or unnecessary broadcast or multicast traffic.

Heartbeat messages shall be sent only to the configured HMI Pi address.

3.4 Linux CLI Auditability and Verification

During the final demonstration, the team shall use Linux command-line tools to verify the running system.

Check IP addresses:

ip -br addr

Check listening TCP/UDP sockets and processes:

sudo ss -tulpn

Check all TCP/UDP sockets and connections:

sudo ss -tunap

Check port ownership:

sudo lsof -nP -i

Check routes and connectivity:

ip route show default
ping -c 4 192.168.5.93

Check Ethernet link status:

sudo ethtool eth0

Observe heartbeat traffic:

sudo tcpdump -i eth0 -nn udp port 5092 -c 10

Observe sensor data traffic:

sudo tcpdump -i eth0 -nn tcp port 5091 -c 10

The team shall verify the six planned communication channels, associated processes, network connectivity, and observed traffic during the final demonstration. The team shall distinguish listening sockets from established connections when presenting the results.

3.5 Reboot and Startup Reproducibility

The Sense HAT Pi shall start its sensor service automatically through systemd.

The HMI Pi shall start the Docker Compose application automatically after boot.

Chromium shall open the Flask dashboard in kiosk mode on the HMI Pi touchscreen.

Clients shall retry connections every two seconds until the other node becomes available.

The complete system shall become operational within 180 seconds of a cold reboot, with a target startup time of 90 seconds.

The repository README shall include the architecture diagram, socket and port assignments, setup instructions, configuration requirements, and startup commands.
