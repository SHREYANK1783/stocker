# Stocker Web Application

A cloud-based stock trading web application built with Python Flask and AWS DynamoDB.

## Features
- **User Authentication:** Secure registration and login with hashed passwords.
- **Stock Dashboard:** View a list of stocks, search by symbol, and view current prices.
- **Trading:** Buy and sell stocks seamlessly to manage your portfolio.
- **Portfolio Tracking:** View your current holdings, average prices, and current total value.
- **Transaction History:** Keep track of all your buy and sell orders.

## Local Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/stocker.git
   cd stocker
   ```

2. **Set up a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables**
   Copy `.env.example` to `.env` and fill in your AWS credentials.
   ```bash
   cp .env.example .env
   ```

5. **Set up DynamoDB Tables**
   Run the database setup script to create the required tables in AWS DynamoDB:
   ```bash
   python setup_db.py
   ```

6. **Run the Application**
   ```bash
   python run.py
   ```
   Navigate to `http://localhost:5000` in your browser.

## Deployment on AWS EC2

### Prerequisites
- An AWS account
- An EC2 Instance (Amazon Linux 2 or Ubuntu recommended)
- DynamoDB access (ensure your EC2 IAM role or `.env` has permissions)

### Step-by-Step Guide
1. **Connect to your EC2 instance** via SSH:
   ```bash
   ssh -i your-key.pem ec2-user@your-ec2-ip-address
   ```
2. **Install Python and Git**:
   ```bash
   sudo yum update -y
   sudo yum install git python3 pip -y
   ```
3. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/stocker.git
   cd stocker
   ```
4. **Setup Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   cp .env.example .env
   # Edit .env and add your SECRET_KEY and AWS credentials
   nano .env 
   ```
5. **Run the server** (For production, use gunicorn + Nginx instead of `run.py`):
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:80 "app:create_app()"
   ```
6. **Access your app** via the EC2 instance's Public IPv4 DNS in a browser. Make sure port 80 is open in your Security Group.

## Testing
To run the automated basic route tests:
```bash
pytest
```
For manual UI testing, follow the steps inside the implementation plan or register an account and test the flow (Buy/Sell/Portfolio/Logout) via `http://localhost:5000`.
