# dynamic_ai_model.py
import random
from datetime import datetime
import json
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import numpy as np
from typing import Dict, List, Optional

class DynamicVoiceAgent:
    def __init__(self):
        self.company_data = []
        self.columns = []
        self.column_mapping = {}
        self.conversation_history = {}
        self.patterns = []  # For clustering
        self.vectorizer = TfidfVectorizer(max_features=100, stop_words='english')
        self.kmeans = None
        self.company_info = {
            "name": "Your Company", 
            "industry": "business",
            "contact_person": "Representative",
            "services": "professional services"
        }
        
        # Create data directory
        os.makedirs('data/patterns', exist_ok=True)
        
        # Load saved patterns on startup
        self.load_patterns_from_disk()
        
        print("🤖 Dynamic Voice Agent Initialized")
    
    def load_company_data(self, company_data: List[Dict], columns: List[str], column_mapping: Dict[str, str] = None):
        """Load company data from uploaded CSV"""
        self.company_data = company_data
        self.columns = columns
        self.column_mapping = column_mapping or {}
        
        # Extract company info from the actual data
        self.company_info = self._extract_company_info_from_data()
        print(f"✅ Loaded company data: {self.company_info}")
    
    def _extract_company_info_from_data(self) -> Dict:
        """Extract company information from the actual loaded data"""
        if not self.company_data:
            return {
                "name": "Your Company", 
                "industry": "business",
                "contact_person": "Representative",
                "services": "professional services"
            }
        
        first_record = self.company_data[0]
        
        # Extract actual values from your CSV columns
        company_name = self._get_value_from_record(first_record, ['company_name', 'company', 'business', 'organization'], 'Your Company')
        contact_person = self._get_value_from_record(first_record, ['calling_agent_name', 'name', 'contact_person'], 'Representative')
        industry = self._get_value_from_record(first_record, ['industry', 'sector', 'field'], 'business')
        services = self._get_value_from_record(first_record, ['services', 'courses', 'offerings'], 'professional services')
        
        return {
            "name": company_name,
            "industry": industry,
            "contact_person": contact_person,
            "services": services
        }
    
    def _get_value_from_record(self, record: Dict, possible_keys: List[str], default: str) -> str:
        """Get value from record trying different possible keys"""
        for key in possible_keys:
            if key in record and record[key]:
                return str(record[key]).strip()
        return default
    
    def load_patterns_from_disk(self):
        """Load saved patterns from disk"""
        try:
            if os.path.exists('data/patterns/conversation_patterns.json'):
                with open('data/patterns/conversation_patterns.json', 'r') as f:
                    self.patterns = json.load(f)
                print(f"✅ Loaded {len(self.patterns)} saved conversation patterns")
            else:
                print("ℹ️ No saved patterns found, starting fresh")
        except Exception as e:
            print(f"⚠️ Error loading patterns: {e}")
            self.patterns = []
    
    def save_patterns_to_disk(self):
        """Save learned patterns to disk"""
        try:
            # Keep only recent patterns (last 1000)
            if len(self.patterns) > 1000:
                self.patterns = self.patterns[-1000:]
            
            with open('data/patterns/conversation_patterns.json', 'w') as f:
                json.dump(self.patterns, f, default=str, indent=2)
            print(f"💾 Saved {len(self.patterns)} conversation patterns to disk")
        except Exception as e:
            print(f"⚠️ Error saving patterns: {e}")
    
    def add_conversation_pattern(self, user_input: str, response: str):
        """Add conversation to learning pool and save persistently"""
        self.patterns.append({
            'input': user_input.lower().strip(),
            'response': response,
            'timestamp': datetime.now().isoformat()
        })
        
        # Save immediately
        self.save_patterns_to_disk()
    
    def generate_short_response(self, user_input: str, customer_data: Dict = None) -> str:
        """Generate short response using ACTUAL company data"""
        user_input = user_input.lower().strip()
        
        # Use your actual company data
        company_name = self.company_info['name']
        industry = self.company_info['industry']
        contact_person = self.company_info['contact_person']
        services = self.company_info['services']
        
        print(f"Generating response for: {user_input}")
        print(f"Using company data: {self.company_info}")
        
        # Generate responses using YOUR actual data
        if any(word in user_input for word in ['hello', 'hi', 'hey']):
            return f"Hello! This is {contact_person} from {company_name}. How can I help you today?"
        
        elif any(word in user_input for word in ['company', 'about', 'who']):
            return f"{company_name} specializes in {industry} and {services}."
        
        elif any(word in user_input for word in ['service', 'help', 'offer', 'course']):
            return f"We offer {services} for {industry} companies. What interests you most?"
        
        elif any(word in user_input for word in ['contact', 'phone', 'email']):
            return f"You can reach {company_name} directly. at the phone no. of company or at the email"
        
        elif any(word in user_input for word in ['busy', 'later']):
            return f"I understand, {contact_person} from {company_name}. When would be better?"
        
        elif any(word in user_input for word in ['thank', 'thanks']):
            return f"You're welcome from {company_name}! Anything else I can help with?"
        
        elif any(word in user_input for word in ['ai', 'robotic', 'automation']):
            return f"At {company_name}, we specialize in {services} for {industry}. How can we help?"
        
        else:
            # Default response with your actual company data
            return f"Thanks from {contact_person} at {company_name}. How can we help with your {industry} needs?"

    def get_learning_insights(self) -> Dict:
        """Get insights from learned patterns"""
        return {
            'pattern_count': len(self.patterns),
            'company_info': self.company_info,
            'storage_location': 'data/patterns/conversation_patterns.json'
        }
