# **FastAPI ZKP Protocol Implementation**
A FastAPI-based **Zero-Knowledge Proof (ZKP) Communication Protocol** for securely exchanging encrypted messages while verifying decryption correctness using Schnorr’s protocol.

## **📌 Overview**
This project implements a **secure communication system** where police patrols exchange encrypted messages over HTTP. To ensure message integrity and authenticity:
1. Messages are **encrypted** before transmission.
2. The **Schnorr Zero-Knowledge Proof** is used to verify the correct decryption of messages.
3. A **distributed model** allows each patrol unit to act as both a **sender** and **verifier**.
4. A **centralized database** stores encryption metadata such as **public keys** and **message history**.

---

## **📌 Features**
✔ **Key Exchange**: Each sender shares their **public key** with others.  
✔ **Message Encryption**: Messages are **encrypted** before being sent.  
✔ **Zero-Knowledge Proof (Schnorr Protocol)**: Ensures the message was correctly decrypted.  
✔ **Message Storage**: Encrypted and decrypted messages are stored in **SQLite**.  
✔ **Multi-Role Nodes**: Each node acts as both a **client (sender)** and **server (verifier)**.  
✔ **Dockerized Deployment**: Uses **Docker Compose** for scalability.  
✔ **TDD Approach**: Fully tested using **pytest**.  

---

## **📌 API Endpoints**
### **1️⃣ Initial Configuration (`/initial_configuration`)**
Stores and retrieves the **prime number** and **generator** for ZKP verification.
- **`POST /initial_configuration`** → Stores the prime and generator.
- **`GET /initial_configuration`** → Retrieves the stored prime and generator.

### **2️⃣ Public Key Exchange (`/public_keys`)**
Handles **public key storage and exchange** for identity verification.
- **`POST /public_keys`** → Stores a user’s public key.
- **`GET /public_keys/{user_id}`** → Retrieves the public key of a specific user.

### **3️⃣ Secure Messaging (`/messages`)**
Manages **encrypted message exchange** and **decryption verification**.
- **`POST /messages/send`** → Sends an encrypted message with a ZKP proof.
- **`POST /messages/verify`** → Verifies decryption correctness using Schnorr's proof.
- **`GET /messages/{message_id}`** → Retrieves message details.

---

## **📌 Project Structure**
```
zkp_protocol/
├── app/
│   ├── core/
│   │   ├── config.py        # App settings (DB URL, app name, etc.)
│   │   ├── database.py      # Database setup (SQLite, SQLAlchemy)
│   ├── main.py              # FastAPI entry point
│   ├── resources/
│   │   ├── init_config/     # Initial ZKP configuration (prime & generator)
│   │   │   ├── model.py
│   │   │   ├── schemas.py
│   │   │   ├── crud.py
│   │   │   ├── routes.py
│   │   │   ├── utils.py
│   │   ├── public_keys/     # Public key management
│   │   ├── messages/        # Secure messaging with ZKP verification
├── docker/
│   ├── Dockerfile
│   ├── docker-compose.yml
├── tests/                   # Unit tests
│   ├── test_init_config.py
│   ├── test_public_keys.py
│   ├── test_messages.py
├── scripts/                 # Utility scripts (prime generation, testing automation)
├── .env                     # Environment variables
├── .gitignore
├── README.md                 # This file
├── requirements.txt          # Dependencies
```

---

## **📌 Installation & Setup**
### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/LeweLotki/police_protocol_zkp.git
cd zkp_protocol
```

### **2️⃣ Install Dependencies**
If using **Poetry**:
```bash
poetry install
```
If using **pip**:
```bash
pip install -r requirements.txt
```

### **3️⃣ Run the Application**
```bash
uvicorn app.main:app --reload
```
Access the API at:  
📌 **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)  
📌 **Redoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## **📌 Running Tests**
Run all tests:
```bash
pytest tests/
```
Run a specific test:
```bash
pytest tests/test_init_config.py
```

---

## **📌 Running with Docker**
Build and start the containers:
```bash
docker compose up -d --build
```
Stop the containers:
```bash
docker compose down
```

---

## **📌 How It Works**
1. **Nodes start up** and exchange **public keys**.
2. A **sender encrypts a message** and sends it along with a **ZKP proof**.
3. The **verifier decrypts the message** and verifies it using Schnorr’s protocol.
4. The **verifier confirms** if the decryption was **successful or not**.
5. Messages and cryptographic metadata are **stored in the database**.

---

## **📌 Future Improvements**
🔹 **End-to-End Encryption**: Implement **AES-256** for message encryption.  
🔹 **Distributed Key Management**: Use **DID (Decentralized Identity)** for public key sharing.  
🔹 **Scalability**: Migrate from **SQLite** to **PostgreSQL** for high availability.  
🔹 **Logging & Monitoring**: Add **ELK Stack** or **Prometheus + Grafana**.  

---

## **📌 License**
📜 MIT License - Free to use and modify.  

---

Now the **README** is **comprehensive and structured**, covering:
✅ **Project Purpose & Features**  
✅ **API Endpoints**  
✅ **Project Structure**  
✅ **Setup Instructions**  
✅ **How It Works**  
✅ **Future Enhancements**  

