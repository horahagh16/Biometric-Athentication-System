# Biometric Authentication System for Deterministic Digital Wallets

This project aims to provide a robust biometric authentication system designed to enhance the security of deterministic digital wallets, reducing the reliance on mnemonic phrases. This repository includes the source code, analysis, and resources required to understand and implement the biometric authentication system.

## Table of Contents

1. [Introduction](#introduction)
2. [Features](#features)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Project Structure](#project-structure)
6. [Contributing](#contributing)
7. [Contact](#contact)

## Introduction

The Biometric Authentication System leverages biometric data, such as facial recognition and fingerprint analysis, to authenticate users securely. This project is particularly focused on integrating these biometric methods with digital wallets, offering a more secure alternative to traditional password and mnemonic-based authentication mechanisms.

## Features

- **Biometric Authentication**: Uses facial recognition and fingerprint analysis to authenticate users.
- **Frontend and Backend Integration**: A full-stack solution with both frontend and backend components for seamless user experience.
- **User Registration and Authentication**: Supports user sign-up and login processes using biometric data.
- **Digital Wallet Security**: Potentially integrates with deterministic digital wallets to enhance security.

## Installation

To set up the Biometric Authentication System locally, follow these steps:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/horahagh16/Biometric-Athentication-System.git
   cd Biometric-Athentication-System
   ```

2. **Run the application:**

   ```bash
   python app.py
   ```

3. **Access the application:**

   Open your web browser and go to `http://127.0.0.1:5000` to use the Biometric Authentication System.

## Usage

1. **Launching the System:**
   - Run the application using the command above.
   - Use the web interface to sign up or log in using your biometric data.

2. **Frontend Interaction:**
   - The frontend consists of an HTML form where users can upload their facial image, fingerprint image, and passphrase.
   - Depending on the chosen process (signup or login), additional fields like mnemonic words may be required.

3. **Testing and Validation:**
   - You can use test data to verify the functionality of the biometric authentication system by following the process outlined in the `analysis/Biometric_Authentication_System.ipynb` notebook.
   - Here is my [dataset](https://drive.google.com/drive/folders/1_QXhFUDC0lltlQL6hpTlnkFc_vlDmFvb?usp=drive_link)

## Project Structure

```
Biometric-Athentication-System/
│
├── analysis/                            # Analysis and exploratory data
│   ├── Biometric_Authentication_System.ipynb  # Jupyter notebook with analysis
│   ├── emotion result/                          # Facial analysis test result
│   └── fingerprint result/                   # Fingerprint analysis test result
│
├── modules/                             # Modules for biometric processing
│   ├── encryption.py                    # Encryption utilities
│   ├── face.py                          # Facial analysis processing
│   └── fingerprint.py                   # Fingerprint analysis processing
│
├── process/                             # Process handling for authentication
│   ├── sign_in.py                       # Sign-in logic
│   └── sign_up.py                       # Sign-up logic
│
├── static/                              # Static files for frontend
│   ├── styles.css                       # CSS styles
│   └── script.js                        # JavaScript logic
│
├── templates/                           # HTML templates
│   └── index.html                       # Main user interface
│
├── app.py                               # Main application file to connect backend and frontend
├── english.txt                          # BIP39 english word list
└── README.md                            # Project documentation
```

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit the changes (`git commit -m 'Add feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Open a pull request.

## Contact

For more information or questions, feel free to contact the project maintainer:

- Name: Hora Haghighatkhah
- Email: haghighatkhah.hora@gmail.com
- GitHub: [horahagh16](https://github.com/horahagh16)

---
