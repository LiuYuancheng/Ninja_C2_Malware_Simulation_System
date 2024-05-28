# Malicious Activities Module Repository 

**Project Design Purpose** : Our goal is to create a comprehensive library repository containing various cyber attack activity modules designed to disrupt computer systems, network devices, and services. The modules in the repository can be imported into other modules to build more complex attack paths or run individually as standalone malware to target and attack specific systems.

```
# Created:     2024/05/28
# version:     v0.2.3
# Copyright:   Copyright (c) 2024 LiuYuancheng
# License:     MIT License
```

**Table of Contents**

[TOC]

------

### Introduction

The Malicious Activities Module Repository is a Python library containing various plugins for generating attack activities aimed at disrupting computer system, network device, or service. All plugin modules can be executed individually as a small attack malware or imported as functions to run within the [ Ninja Agent ] module, enabling the construction of more complex attack paths. 

The malicious modules will cover 28 different activities under five attack field:  `Credentials Compromise`, `Phishing and Scam`, `Scan and Record`, `Denial of Service(DoS)` and `System Destruction`. 



#### Introduction of Credentials Compromise Module

These modules are used to compromise the target's security information by stealing files or scanning user traces.

##### File/Data Stolen Module

The File/Data Stolen module is designed to extract sensitive information from target systems. Its functions include: File Extraction, Directory Scanning, Data Compression, Stealth Transfer and Log Cleanup. 

##### Command History Scanning Module

Retrieve and analyze Linux OS user's commands history to uncover executed commands and potentially sensitive information.

