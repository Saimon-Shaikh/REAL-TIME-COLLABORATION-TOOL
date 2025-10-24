# REAL-TIME-COLLABORATION-TOOL

*COMPANY NAME*: CODTECH IT SOLUTIONS PVT.LTD

*NAME*: SAIMON SHAIKH

*INTERN ID*: CT06DR437

*DOMAIN NAME*: SOFTWARE DEVELOPMENT

*DURATION*: 6 WEEKS

*MENTOR NAME*: NEELA SANTOSH

---
# TASK/PROJECT DESCRIPTION
## Task 3: Real-Time Communication via WebSockets (CODTECH IT SOLUTIONS Internship)

This repository contains the source code for a fully functional, multi-user collaborative text editor. This project was developed as **Task 3** of the CODTECH IT SOLUTIONS Software Developer Internship program, demonstrating core skills in **real-time, bidirectional communication** using the WebSocket protocol.

---

## Project Overview

The primary goal was to move beyond the traditional HTTP request/response model to implement **instant data synchronization** across multiple clients. This was achieved by creating a simplified collaborative text editor (similar to Google Docs) where changes made by any user are immediately reflected in the document for all other connected participants.

The project proves proficiency in managing **persistent connections** and implementing server-side **broadcasting** logic, essential for modern interactive web applications.

### Key Features:

* **Instant Synchronization:** Leverages **WebSockets** (via Flask-SocketIO) to ensure text updates occur instantly with near-zero latency.
* **Multi-User Support:** The server accurately tracks, manages, and broadcasts the number of active users editing the document in real-time.
* **Bidirectional Data Flow:** Clients send user input (`text_change` event), and the server immediately broadcasts the updated state back to all clients (`update_text` event).
* **Live Collaborator List:** The server maintains a dictionary of all currently connected users. A list of currently online usernames is broadcast to all clients whenever a user connects, disconnects, or changes their name.
*  **Custom Identity & Registration:** Users are initially assigned a unique, temporary "Guest" name. A dedicated input field and button allow users to register a custom display name (username). This name is then used in the live collaborator list.
* **Initial State Loading:** New clients receive the current document history upon connecting, ensuring they start with the latest content.
* **Aesthetic UI/UX:** Features a clean, attractive, and fully responsive light-theme interface for optimal user experience.

---

## Technical Implementation

The architecture is built on a persistent, open communication layer managed by Flask-SocketIO.

### Real-Time Communication Layer:

The core system uses **Flask-SocketIO** to handle all connection handshakes and data broadcasting, replacing standard Flask routing for real-time events.

| Event Name | Direction | Triggered By | Server Action (Brief) |
| :--- | :--- | :--- | :--- |
| `connect` | Client → Server | Client loads page. | Initial handshake; sends current document state. |
| `disconnect` | Client → Server | Client closes tab. | Logs exit; updates and broadcasts new user count. |
| `text_change` | Client → Server | User types in editor. | **Core Logic:** Updates the document state (currently in-memory) and broadcasts `update_text` to all other users. |

### Technologies Used:

| Component | Technology | Role |
| :--- | :--- | :--- |
| **Backend Framework** | Python / Flask | Core application framework and routing |
| **Real-Time Protocol** | Flask-SocketIO (WebSockets) | Manages persistent connections and broadcasting |
| **Frontend** | HTML5, Vanilla JavaScript | Client-side logic for connecting and UI updates |
| **Styling** | Tailwind CSS (CDN) | Rapid, responsive UI design and theming |
| **Typography** | Jost / Inter Fonts | Enhanced visual appeal and readability |
