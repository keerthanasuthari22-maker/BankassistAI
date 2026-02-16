"""
Banking Tools for Function Calling Agent
These tools can be called by the OpenAI function calling mechanism
"""
import json
from typing import Dict, Any, List
from pathlib import Path
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class BankingToolkit:
    """Set of tools for banking customer service agent"""
    
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self._load_data()
    
    def _load_data(self):
        """Load banking data"""
        # Load transactions
        transactions_path = self.data_dir / "transactions.json"
        self.transactions = []
        if transactions_path.exists():
            with open(transactions_path, 'r') as f:
                self.transactions = json.load(f)
        
        # Load branches
        branches_path = self.data_dir / "branch_data.json"
        self.branches = []
        if branches_path.exists():
            with open(branches_path, 'r') as f:
                data = json.load(f)
                self.branches = data.get("branches", [])
    
    def get_account_details(self, account_id: str) -> Dict[str, Any]:
        """
        Retrieve account details for a customer
        
        Args:
            account_id: Customer account ID (e.g., 'ACC001')
        
        Returns:
            Dictionary with account information
        """
        # Simulated account details
        accounts = {
            "ACC001": {
                "account_id": "ACC001",
                "customer_name": "Rajesh Kumar",
                "account_type": "Savings Account",
                "balance": 250000,
                "account_status": "Active",
                "opening_date": "2020-01-15",
                "account_number": "1234567890123456"
            },
            "ACC002": {
                "account_id": "ACC002",
                "customer_name": "Priya Sharma",
                "account_type": "Current Account",
                "balance": 500000,
                "account_status": "Active",
                "opening_date": "2019-06-22",
                "account_number": "2345678901234567"
            },
            "ACC003": {
                "account_id": "ACC003",
                "customer_name": "Amit Patel",
                "account_type": "Salary Account",
                "balance": 125000,
                "account_status": "Active",
                "opening_date": "2021-03-10",
                "account_number": "3456789012345678"
            }
        }
        
        if account_id in accounts:
            return {
                "success": True,
                "data": accounts[account_id]
            }
        else:
            return {
                "success": False,
                "error": f"Account {account_id} not found. Try ACC001, ACC002, or ACC003"
            }
    
    def get_transaction_history(
        self,
        account_id: str,
        days: int = 30
    ) -> Dict[str, Any]:
        """
        Retrieve transaction history for an account
        
        Args:
            account_id: Customer account ID
            days: Number of days to retrieve (default: 30)
        
        Returns:
            List of transactions
        """
        relevant_transactions = [
            t for t in self.transactions
            if t['account_id'] == account_id
        ]
        
        if relevant_transactions:
            # Sort by date descending
            relevant_transactions.sort(
                key=lambda x: x['date'],
                reverse=True
            )
            return {
                "success": True,
                "account_id": account_id,
                "transaction_count": len(relevant_transactions),
                "transactions": relevant_transactions[:10]  # Last 10 transactions
            }
        else:
            return {
                "success": False,
                "error": f"No transactions found for account {account_id}"
            }
    
    def find_nearest_branch(self, city: str) -> Dict[str, Any]:
        """
        Find branches in a specific city
        
        Args:
            city: City name to search for
        
        Returns:
            List of branches in the city
        """
        matching_branches = [
            b for b in self.branches
            if city.lower() in b['city'].lower()
        ]
        
        if matching_branches:
            return {
                "success": True,
                "city": city,
                "branch_count": len(matching_branches),
                "branches": matching_branches
            }
        else:
            return {
                "success": False,
                "error": f"No branches found in {city}. Available cities: Mumbai, Bangalore, Delhi"
            }
    
    def check_loan_eligibility(self, account_id: str, loan_type: str) -> Dict[str, Any]:
        """
        Check loan eligibility for a customer
        
        Args:
            account_id: Customer account ID
            loan_type: Type of loan (personal, home, business, auto)
        
        Returns:
            Eligibility status and details
        """
        account = self.get_account_details(account_id)
        if not account['success']:
            return account
        
        customer_data = account['data']
        loan_details = {
            "personal": {
                "max_amount": 5000000,
                "interest_rate": "9% - 12% p.a.",
                "tenure": "12 - 60 months",
                "min_balance_required": 50000
            },
            "home": {
                "max_amount": 10000000,
                "interest_rate": "8.5% - 9.5% p.a.",
                "tenure": "120 - 360 months",
                "min_balance_required": 100000
            },
            "business": {
                "max_amount": 1000000,
                "interest_rate": "12% - 15% p.a.",
                "tenure": "24 - 84 months",
                "min_balance_required": 200000
            },
            "auto": {
                "max_amount": 5000000,
                "interest_rate": "8% - 10% p.a.",
                "tenure": "24 - 84 months",
                "min_balance_required": 100000
            }
        }
        
        if loan_type.lower() not in loan_details:
            return {
                "success": False,
                "error": f"Unknown loan type. Available: personal, home, business, auto"
            }
        
        details = loan_details[loan_type.lower()]
        eligible = customer_data['balance'] >= details['min_balance_required']
        
        return {
            "success": True,
            "account_id": account_id,
            "customer_name": customer_data['customer_name'],
            "loan_type": loan_type,
            "eligible": eligible,
            "loan_details": details,
            "message": f"Eligible for {loan_type} loan" if eligible else f"Minimum balance of Rs. {details['min_balance_required']} required"
        }
    
    def escalate_to_human(self, account_id: str, reason: str) -> Dict[str, Any]:
        """
        Create escalation ticket for human agent
        
        Args:
            account_id: Customer account ID
            reason: Reason for escalation
        
        Returns:
            Ticket confirmation
        """
        ticket_id = f"TKT{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        return {
            "success": True,
            "ticket_id": ticket_id,
            "account_id": account_id,
            "reason": reason,
            "status": "Created",
            "message": f"Your request has been escalated. Ticket ID: {ticket_id}. A human agent will contact you within 2 hours.",
            "priority": "high"
        }
    
    def validate_account(self, account_id: str) -> Dict[str, Any]:
        """
        Validate if account exists
        
        Args:
            account_id: Account ID to validate
        
        Returns:
            Validation result
        """
        account = self.get_account_details(account_id)
        return {
            "success": account['success'],
            "account_id": account_id,
            "valid": account['success'],
            "message": f"Account {account_id} exists" if account['success'] else f"Account {account_id} not found"
        }


def get_tool_definitions() -> List[Dict]:
    """
    Get OpenAI function calling tool definitions
    These are provided to the API to enable function calling
    """
    return [
        {
            "type": "function",
            "function": {
                "name": "get_account_details",
                "description": "Retrieve account details including balance, account type, and status for a customer",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "account_id": {
                            "type": "string",
                            "description": "The customer's account ID (e.g., 'ACC001')"
                        }
                    },
                    "required": ["account_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_transaction_history",
                "description": "Get recent transactions for a customer account",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "account_id": {
                            "type": "string",
                            "description": "The customer's account ID"
                        },
                        "days": {
                            "type": "integer",
                            "description": "Number of days of history to retrieve (default: 30)"
                        }
                    },
                    "required": ["account_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "find_nearest_branch",
                "description": "Find bank branches in a specific city with their details and services",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "city": {
                            "type": "string",
                            "description": "City name to search for branches"
                        }
                    },
                    "required": ["city"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "check_loan_eligibility",
                "description": "Check customer eligibility for different types of loans",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "account_id": {
                            "type": "string",
                            "description": "The customer's account ID"
                        },
                        "loan_type": {
                            "type": "string",
                            "description": "Type of loan: personal, home, business, or auto"
                        }
                    },
                    "required": ["account_id", "loan_type"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "escalate_to_human",
                "description": "Escalate a customer query to a human agent when automated resolution is not possible",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "account_id": {
                            "type": "string",
                            "description": "The customer's account ID"
                        },
                        "reason": {
                            "type": "string",
                            "description": "Reason for escalation"
                        }
                    },
                    "required": ["account_id", "reason"]
                }
            }
        }
    ]
