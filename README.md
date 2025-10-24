# REAL-TIME-COLLABORATION-TOOL

*COMPANY NAME*: CODTECH IT SOLUTIONS PVT.LTD

*NAME*: SAIMON SHAIKH

*INTERN ID*: CT06DR437

*DOMAIN NAME*: SOFTWARE DEVELOPMENT

*DURATION*: 6 WEEKS

*MENTOR NAME*: NEELA SANTOSH

----------------
## Task 3: Real-Time Communication via WebSockets (CODTECH IT SOLUTIONS Internship)

This repository contains the source code for a fully functional, multi-user collaborative text editor. This project was developed as **Task 3** of the CODTECH IT SOLUTIONS Software Developer Internship program, demonstrating core skills in **real-time, bidirectional communication** using the WebSocket protocol.

## Project Overview
----------------

The primary goal was to move beyond the traditional HTTP request/response model to implement **instant data synchronization** across multiple clients. This was achieved by creating a simplified collaborative text editor (similar to Google Docs) where changes made by any user are immediately reflected in the document for all other connected participants.

The project proves proficiency in managing **persistent connections** and implementing server-side **broadcasting** logic, essential for modern interactive web applications.

### Key Features:

-   **Instant Synchronization:** Leverages **WebSockets** (via Flask-SocketIO) to ensure text updates occur instantly with near-zero latency.

-   **Multi-User Support:** The server accurately tracks, manages, and broadcasts the number of active users editing the document in real-time.

-   **Bidirectional Data Flow:** Clients send user input (`text_change` event), and the server immediately broadcasts the updated state back to all clients (`update_text` event).

-   **Initial State Loading:** New clients receive the current document history upon connecting, ensuring they start with the latest content.

-   **Aesthetic UI/UX:** Features a clean, attractive, and fully responsive light-theme interface for optimal user experience.

## Technical Implementation
------------------------

The architecture is built on a persistent, open communication layer managed by Flask-SocketIO.



## Technologies Used:
