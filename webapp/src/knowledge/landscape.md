# IT Landscape

This document describes the high level landscape for the lab in which this ServiceNow instance governs.

This technology ecosystem is a lab environment designed to support technical sales team efforts in
which innovative solutions are developed, customer demos are maintained and demonstrated, and IT 
operations platforms can be operated in order to simplify maintenance of the various systems involved.

The systems and solutions are in support of Red Hat teams and primarily consist of Red Hat products,
like Red Hat Enterprise Linux (RHEL), OpenShift Container Platform (OCP), and Ansible Automation 
Platform (AAP).

Most assetes in the lab are part of the shadowman.dev domain.

Monitoring and observability is performed by DataDog.  It is responsible for monitoring system 
resources, processes, and general health and then alerts when certain conditions are met.  These alerts
are then published to ServiceNow for actioning.

Ansible Automation Platform is configured to spawn automation playbooks for certain events.  It is
our objective to increase the number of events that AAP is capable of handling.

## Generic Assets

| Asset Name | Aliases | Description |
|---|---|--|
| Apache HTTP Server | HTTPD | Apache web server, hosting static web sites on RHEL |
|---|---|--|
