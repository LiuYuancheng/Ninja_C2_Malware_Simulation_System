#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        __init__.py
#
# Purpose:     The regular package init module to init the customer "lib".
#
# Author:      Yuancheng Liu
#
# Created:     2014/01/15
# Copyright:   Copyright (c) 2024 LiuYuancheng
# License:     MIT License
#-----------------------------------------------------------------------------

"""
Package Info

Name: lib

Description:
- provide the module used for the infra monitor hub's frontend web host and the 
backend data base handler .

Modules inclided in the current package: 

1. ConfigLoader.py: 
- Provide API to load the not stand text format config file's data.

2. Log.py: 
- Provide the addtional log function to do the program execution log archiving feature.

3. c2Client.py:
- Provide the API to connect and communication to the c2 server to use the related function.

4. c2Constants.py:
- Define all the constants used in the c2 server and client. 

5. c2MwUtiles.py
- Utilities functions module used in the c2 clients to implememt the
basic attack actions.

6. keyEventActors.py
- Provide the API to handle and generate the keyboard event. 

7. mouseEventActors.py
- Provide the API to handle and genearte the mouse event.

8. nmapUtils.py
- Nmap untilities function to call the nmap API to do the network scan and service probe. 

9. SSHconnector.py
- Provide the API to connect and communication to the remote host via SSH protocol.

10. SCPconnector.py 
- Provide the API to connect and communication to the remote host via SSH to handle
file scp operation.

11. tsharkUtils.py
- Wireshark untilities function to call the tshark API to do the packet capture 
and analysis.

"""