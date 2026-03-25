# Cryptocurrency Price Tracker 
CPE-EC2-Final-Project by Ser Adriane Vincent B. Jugo

CPE-EC2-ETL-ELT/                <--  main GitHub Repository
│
├── README.md                   <-- Main instructions and overview of the project
├── requirements.txt            <-- List of Python packages (flask, requests, etc.)
│
├── Website-A-ETL/              <-- Folder for the ETL Application
│   ├── crypto_etl.py           <-- Your Python extraction & transformation script
│   ├── crypto_etl.db           <-- The SQLite database (created when script runs)
│   ├── app.py                  <-- (Optional) Flask script to run the web frontend
│   └── templates/              
│       └── index.html          <-- The HTML frontend for Website A
│
└── Website-B-ELT/              <-- Folder for the ELT Application
    ├── crypto_elt.py           <-- Your Python extraction script & SQL View setup
    ├── crypto_elt.db           <-- The SQLite database (created when script runs)
    ├── app.py                  <-- (Optional) Flask script to run the web frontend
    └── templates/              
        └── index.html          <-- The HTML frontend for Website B
