# utils/csv_processor.py
import pandas as pd
import io
from typing import Dict, List, Tuple

class CSVProcessor:
    @staticmethod
    def find_column_by_keywords(columns: List[str], keywords: List[str]) -> str:
        """Find column name that matches any of the keywords"""
        columns_lower = [col.lower() for col in columns]
        for keyword in keywords:
            for i, col_lower in enumerate(columns_lower):
                if keyword.lower() in col_lower or col_lower in keyword.lower():
                    return columns[i]  # Return original case
        return None
    
    @staticmethod
    def smart_validate_csv(columns: List[str]) -> Tuple[bool, Dict[str, str]]:
        """Intelligently validate CSV and map columns"""
        column_mapping = {}
        
        # Smart detection of important columns
        name_col = CSVProcessor.find_column_by_keywords(columns, 
            ['name', 'person', 'contact', 'agent', 'caller'])
        company_col = CSVProcessor.find_column_by_keywords(columns, 
            ['company', 'business', 'organization', 'institution', 'hub'])
        industry_col = CSVProcessor.find_column_by_keywords(columns, 
            ['industry', 'sector', 'field', 'domain', 'vertical'])
        services_col = CSVProcessor.find_column_by_keywords(columns, 
            ['service', 'course', 'program', 'solution', 'offering'])
        phone_col = CSVProcessor.find_column_by_keywords(columns, 
            ['phone', 'mobile', 'contact'])
        email_col = CSVProcessor.find_column_by_keywords(columns, 
            ['email', 'mail'])
        
        # Store mappings
        if name_col:
            column_mapping['name'] = name_col
        if company_col:
            column_mapping['company'] = company_col
        if industry_col:
            column_mapping['industry'] = industry_col
        if services_col:
            column_mapping['services'] = services_col
        if phone_col:
            column_mapping['phone'] = phone_col
        if email_col:
            column_mapping['email'] = email_col
            
        # At minimum need name/company equivalent
        has_min_requirements = bool(name_col or company_col)
        
        return has_min_requirements, column_mapping
    
    @staticmethod
    def process_uploaded_csv(file_stream) -> Tuple[List[Dict], List[str], bool, Dict[str, str]]:
        """Process uploaded CSV file with smart column detection"""
        try:
            # Read CSV
            df = pd.read_csv(io.StringIO(file_stream.read().decode('utf-8', errors='ignore')))
            file_stream.seek(0)  # Reset stream
            
            # Convert to records
            records = df.to_dict('records')
            columns = list(df.columns)
            
            # Smart validation
            is_valid, column_mapping = CSVProcessor.smart_validate_csv(columns)
            
            return records, columns, is_valid, column_mapping
            
        except Exception as e:
            raise Exception(f"Error processing CSV: {str(e)}")
    
    @staticmethod
    def extract_smart_company_info(records: List[Dict], column_mapping: Dict[str, str]) -> Dict:
        """Extract company information using smart column mapping"""
        if not records:
            return {
                "name": "Your Company", 
                "industry": "business",
                "contact_person": "Representative"
            }
        
        first_record = records[0]
        
        # Use mapped columns or smart fallbacks
        company_name = (
            first_record.get(column_mapping.get('company', ''), '') or
            first_record.get('company', '') or 
            first_record.get('company_name', '') or 
            first_record.get('business', '') or 
            first_record.get('organization', '') or
            "Your Company"
        )
        
        contact_person = (
            first_record.get(column_mapping.get('name', ''), '') or
            first_record.get('name', '') or 
            first_record.get('contact_person', '') or 
            first_record.get('calling_agent_name', '') or
            "Representative"
        )
        
        industry = (
            first_record.get(column_mapping.get('industry', ''), '') or
            first_record.get('industry', '') or 
            first_record.get('sector', '') or 
            first_record.get('field', '') or 
            "business"
        )
        
        services = (
            first_record.get(column_mapping.get('services', ''), '') or
            first_record.get('services', '') or 
            first_record.get('courses', '') or 
            first_record.get('offerings', '') or
            "professional services"
        )
        
        return {
            "name": company_name,
            "industry": industry,
            "contact_person": contact_person,
            "services": services
        }
