# 📦 Pub/Sub Event Planning System

This project simulates a real-world event coordination system using a **Publisher/Subscriber (Pub/Sub)** model in Python, powered by **Redis Streams**. The architecture is designed to demonstrate decoupled, asynchronous communication between multiple independent actors.

---

## 🚀 System Overview

### Roles Involved:

- **🎤 Host**  
  Publishes an event invitation to the system.

- **☁️ Coordinator**  
  Acts as the central broker. It:
  - Receives invitations from the Host
  - Forwards them to all registered Guests
  - Collects guest responses
  - Sends back a compiled summary to the Host

- **🎉 Guest**  
  Subscribes to invitations, decides whether to attend (`Yes`, `No`, or `Maybe`), and sends their response back to the Coordinator.

---

## 🧩 Tech Stack

- **Python**
- **Redis Streams** for Pub/Sub messaging
- **Threading** for concurrent listening
- **Environment Variables / Config** for independent processes



