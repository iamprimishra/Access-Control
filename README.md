# Access-Control
Scalable RFID-Based Secure Access Management

## Introduction
The Access Control project is a comprehensive system designed to ensure secure and reliable access management to controlled areas. Leveraging RFID Card credentials, this project enables the granting or denying of access based on authorized user identification. It comes equipped with features such as time tracking and remote administration for enhanced control and monitoring.

## Features
**RFID-Based Access Control**: The system grants or denies access based on RFID card credentials, allowing only authorized personnel to enter controlled areas.

**Time Tracking**: With the integration of the DS1307 RTC module, the system accurately tracks time, enabling administrators to set time-based access rules and monitor user activity.

**Remote Administration**: The web interface offers remote administration capabilities, allowing administrators to manage access settings and user data from any connected device.

**Scalability**: The project is designed to be scalable, capable of managing access to a single door or multiple access points across a complex facility.

**Security**: By using RFID cards, this access control system provides a higher level of security compared to traditional key-based access control systems, reducing the risk of unauthorized access.

## Hardware Components
**Rugged Board-A5D2x**: This powerful embedded board serves as the main processing unit, managing data processing and access control logic.

**EM18 RFID Reader Module**: The RFID reader module allows the system to read RFID card credentials and authenticate users.

**DS1307 RTC Module**: The Real-Time Clock (RTC) module ensures accurate timekeeping, enabling precise tracking and control of user access based on time parameters.

## Software Components
**User-Friendly Web Interface**: The system features a well-designed web interface created using HTML, CSS, and JavaScript. This interface provides administrators with intuitive tools to efficiently manage access settings and user information.

**Python Server**: A locally hosted Python Server handles data storage and manages the access control logic. It processes the requests from the RFID reader, authenticates users, and grants or denies access based on predefined rules.

**Multithreading and Parallel Processing in Python**: The implementation of multithreading and parallel processing in Python optimizes system performance, ensuring swift response times even during peak usage.

**MRAA Embedded Library**: The MRAA library offers an efficient interface to interact with the hardware components, allowing seamless integration of software and hardware functionalities.

**I2C and UART Protocols**: These communication protocols facilitate seamless and efficient data exchange between components.

## Operating System
Linux is chosen as the operating system for this project due to its inherent stability and robust security features. Linux ensures a reliable and secure platform for hosting the access control system.

## Conclusion
Project Access Control offers a robust and scalable solution for secure access management. By combining RFID technology with sophisticated software components, the system ensures reliable authentication, time tracking, and remote administration. Its user-friendly web interface and optimized performance through multithreading and parallel processing make it an efficient and reliable choice for controlling access to controlled areas. With Linux as the operating system, the Access Control project guarantees stability and security in access management, providing peace of mind to facility administrators and ensuring a safe environment for authorized personnel.
