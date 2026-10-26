# DistributedCyberPhysicalSystem
Title: DistributedCyberPhysicalSystem
Purpose: Our project addresses the problem of having to SSH into the Sense HAT Pi to view the sensor readings. Using SSH requires users to run separate commands to view different readings and rerun those commands when they want to see updated data. Our Distributed Cyber-Physical System allows a user to see all data on the HMI Pi touchscreen in real time. This makes viewing data more convenient and allows users to easily check if the Sense HAT Pi is connected and communicating with the system. The system also saves the sensor readings for further viewing and analysis. The intended users are people who need to monitor sensor readings, observe changes in environmental conditions, and check connection status.
Scope: 
HMI Pi Role (Services hosted, UI role, data processing): _Will display the sensor readings from the Sense HAT Pi on its touchscreen and show the connection status of the Sense HAT Pi. It processes, organizes, and stores each reading.____
Sense HAT Pi Role (Sensors/actuators polled, daemons hosted): __It collects environmental readings from its sensors and sends it to the HMI Pi through the classroom network._______
Remote Storage / Infrastructure Role (NAS Database, MQTT Broker, or SFTP/SCP Server): __Provide storage to sensor readings so that a users can access past readings. We will use a NAS database _________________
Optional Additional Nodes (Other Sandbox Table Pis or PLCs—note table consultation if applicable): N/A
Out-of-Scope Boundaries (List 1–2 features your team is intentionally excluding to ensure completion by Week 15): prediction of environmental measurements and notification system
