"""
Data initialization and utilities for Banking AI Agent
"""
import json
from pathlib import Path
from datetime import datetime, timedelta
import random


def create_sample_data():
    """Create realistic sample banking data"""
    
    data_dir = Path(__file__).parent / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    
    # Create banking FAQs and policies
    banking_docs = """
# BANKING CUSTOMER SERVICE DOCUMENTATION

## Account Management
### How do I open a new account?
To open a new account, visit your nearest branch with valid ID proof, PAN card, and address proof. 
You can also apply online through our mobile app or website. The process takes 2-3 business days.

### What are the minimum balance requirements?
- Savings Account: Rs. 5,000
- Current Account: Rs. 50,000
- Salary Account: No minimum balance required

### Can I change my account type?
Yes, you can convert your Savings Account to Current Account or vice versa at zero cost. 
Visit your branch or call our customer service at 1800-BANK-123.

## Transaction Services
### What is the daily transaction limit?
- ATM Withdrawals: Rs. 50,000 per day
- NEFT/RTGS Transfer: Rs. 10,00,000 per transaction
- Mobile Banking: Rs. 2,00,000 per day

### How long do transfers take?
- NEFT: 1-2 hours (during banking hours)
- RTGS: 30 minutes (urgent transfers, fee Rs. 25)
- IMPS: Instant (24/7 available)
- Cheque Clearing: 3-5 business days

### What are the charges for international transfers?
International transfers (SWIFT): Rs. 500 + applicable bank charges
Exchange rate: Current market rate + 0.5% markup

## Loan Services
### What loan options are available?
1. Personal Loan: Up to Rs. 50 lakhs, 9% - 12% interest rate
2. Home Loan: Up to Rs. 1 crore, 8.5% - 9.5% interest rate
3. Business Loan: Up to Rs. 10 lakhs, 12% - 15% interest rate
4. Auto Loan: Up to Rs. 50 lakhs, 8% - 10% interest rate

### How do I apply for a loan?
Submit your application online or visit the nearest branch with:
- Last 6 months salary slips
- Last 2 years income tax returns
- Bank statements
- Identity and address proof

Approval typically takes 3-5 business days.

### What is the prepayment policy?
You can prepay any loan amount without penalty. Full loan closure: No exit charges.

## Digital Banking
### How do I register for mobile banking?
Visit any branch or call 1800-BANK-456. You'll receive an OTP-based login setup.
No additional charges for registration.

### Is mobile banking secure?
Yes, all transactions are encrypted with 256-bit SSL encryption.
Enable 2FA in security settings for additional protection.

### What should I do if I forget my password?
Use 'Forgot Password' on login screen for automatic recovery via registered mobile number.
If unavailable, visit nearest branch with ID proof.

## Complaints & Grievances
### How do I file a complaint?
1. Online: Visit grievance.bankassist.com
2. Call: 1800-BANK-789 (24/7)
3. Visit: Nearest branch during business hours

Resolution time: 30 days for standard complaints, 7 days for urgent issues.

### Who can I escalate to if unsatisfied?
Contact our Ombudsman at: ombudsman@bankassist.com or write to regulatory body within 60 days.

## Branch & ATM Services
### What are branch timings?
Standard timings: 9:00 AM - 5:00 PM (Monday - Friday)
9:00 AM - 2:00 PM (Saturday)
Closed on Sundays and national holidays

### How do I find the nearest branch?
Use our mobile app, visit bankassist.com, or call 1800-BANK-100.
You can search by location, city, or service type.

## Fees & Charges
### What are the annual account maintenance charges?
- Savings Account: Rs. 0 (No charges)
- Current Account: Rs. 500 per quarter (Rs. 2,000/year)
- Salary Account: Rs. 0 (No charges)

### Are there charges for digital transactions?
NEFT/RTGS: Rs. 25-50 per transaction
Mobile Banking/Internet Banking: Completely free
SMS Alerts: Rs. 0 (Complimentary)
"""
    
    with open(data_dir / "banking_docs.txt", "w") as f:
        f.write(banking_docs)
    
    # Create branch data
    branches = {
        "branches": [
            {
                "id": "BR001",
                "name": "Downtown Branch",
                "city": "Mumbai",
                "address": "123 Financial Plaza, Mumbai - 400001",
                "phone": "022-1234-5678",
                "email": "downtown@bankassist.com",
                "timings": "9:00 AM - 5:00 PM",
                "services": ["Account Opening", "Loan Application", "Safe Deposit Lockers"],
                "atm_available": True
            },
            {
                "id": "BR002",
                "name": "Airport Branch",
                "city": "Mumbai",
                "address": "Terminal 2, Mumbai Airport",
                "phone": "022-9876-5432",
                "email": "airport@bankassist.com",
                "timings": "24/7",
                "services": ["International Transfers", "Forex", "Travel Cards"],
                "atm_available": True
            },
            {
                "id": "BR003",
                "name": "IT Hub Branch",
                "city": "Bangalore",
                "address": "Tech Park, Whitefield, Bangalore - 560066",
                "phone": "080-4456-7890",
                "email": "ithub@bankassist.com",
                "timings": "9:00 AM - 6:00 PM",
                "services": ["Account Opening", "Credit Cards", "Digital Services"],
                "atm_available": True
            },
            {
                "id": "BR004",
                "name": "Central Branch",
                "city": "Delhi",
                "address": "456 Business Central, New Delhi - 110001",
                "phone": "011-2345-6789",
                "email": "central@bankassist.com",
                "timings": "9:00 AM - 5:00 PM",
                "services": ["Bulk Services", "Corporate Accounts", "Investment"],
                "atm_available": True
            }
        ]
    }
    
    with open(data_dir / "branch_data.json", "w") as f:
        json.dump(branches, f, indent=2)
    
    # Create sample transactions
    customers = {
        "ACC001": {"name": "Rajesh Kumar", "balance": 250000, "account_type": "Savings"},
        "ACC002": {"name": "Priya Sharma", "balance": 500000, "account_type": "Current"},
        "ACC003": {"name": "Amit Patel", "balance": 125000, "account_type": "Salary"},
    }
    
    transactions = []
    base_date = datetime.now()
    
    for acc_id, customer in customers.items():
        for i in range(10):
            trans_date = base_date - timedelta(days=random.randint(1, 30))
            transactions.append({
                "transaction_id": f"TXN{acc_id}{i:03d}",
                "account_id": acc_id,
                "customer_name": customer["name"],
                "date": trans_date.isoformat(),
                "type": random.choice(["Credit", "Debit"]),
                "amount": round(random.uniform(1000, 50000), 2),
                "description": random.choice([
                    "Salary Deposit",
                    "Grocery Purchase",
                    "Electricity Bill",
                    "ATM Withdrawal",
                    "Online Shopping",
                    "Transfer to Friend"
                ]),
                "status": "Completed"
            })
    
    with open(data_dir / "transactions.json", "w") as f:
        json.dump(transactions, f, indent=2)
    
    print("✅ Sample data created successfully!")
    return True


if __name__ == "__main__":
    create_sample_data()
