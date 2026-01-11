"""
INPUT WIZARD
Interactive input system for Termux
"""

import sys
import os
from typing import List, Dict, Any, Optional, Callable
import json

class Colors:
    """Terminal colors for Termux"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class InputWizard:
    """Interactive input wizard for Termux"""
    
    def __init__(self):
        self.current_section = None
        self.responses = {}
        
    def print_header(self, text: str):
        """Print section header"""
        width = 50
        print(f"\n{Colors.CYAN}{'=' * width}{Colors.END}")
        print(f"{Colors.BOLD}{text.center(width)}{Colors.END}")
        print(f"{Colors.CYAN}{'=' * width}{Colors.END}\n")
    
    def print_step(self, step: int, text: str):
        """Print step information"""
        print(f"{Colors.GREEN}[{step}] {Colors.YELLOW}{text}{Colors.END}")
    
    def print_success(self, text: str):
        """Print success message"""
        print(f"{Colors.GREEN}✅ {text}{Colors.END}")
    
    def print_error(self, text: str):
        """Print error message"""
        print(f"{Colors.RED}❌ {text}{Colors.END}")
    
    def print_info(self, text: str):
        """Print info message"""
        print(f"{Colors.BLUE}ℹ️  {text}{Colors.END}")
    
    def ask_yes_no(self, question: str, default: bool = True) -> bool:
        """Ask yes/no question"""
        options = "Y/n" if default else "y/N"
        
        while True:
            response = input(f"{Colors.YELLOW}👉 {question} [{options}]: {Colors.END}").strip().lower()
            
            if response == "":
                return default
            elif response in ["y", "yes"]:
                return True
            elif response in ["n", "no"]:
                return False
            else:
                self.print_error("Please enter 'y' or 'n'")
    
    def ask_text(self, question: str, default: str = None, password: bool = False) -> str:
        """Ask for text input"""
        prompt = f"{Colors.YELLOW}👉 {question}"
        
        if default:
            prompt += f" [{default}]"
        
        prompt += f": {Colors.END}"
        
        if password:
            import getpass
            response = getpass.getpass(prompt)
        else:
            response = input(prompt)
        
        if not response and default:
            return default
        
        return response
    
    def ask_number(self, question: str, min_val: int = None, max_val: int = None, default: int = None) -> int:
        """Ask for number input"""
        while True:
            prompt = f"{Colors.YELLOW}👉 {question}"
            
            if default is not None:
                prompt += f" [{default}]"
            
            prompt += f": {Colors.END}"
            
            response = input(prompt).strip()
            
            if not response and default is not None:
                return default
            
            if response.isdigit():
                num = int(response)
                
                if min_val is not None and num < min_val:
                    self.print_error(f"Number must be at least {min_val}")
                elif max_val is not None and num > max_val:
                    self.print_error(f"Number must be at most {max_val}")
                else:
                    return num
            else:
                self.print_error("Please enter a valid number")
    
    def ask_choice(self, question: str, choices: List[str], default: int = None) -> str:
        """Ask to choose from list"""
        print(f"{Colors.YELLOW}👉 {question}{Colors.END}")
        
        for i, choice in enumerate(choices, 1):
            print(f"  {Colors.CYAN}{i}.{Colors.END} {choice}")
        
        while True:
            prompt = f"{Colors.YELLOW}Enter choice"
            
            if default is not None:
                prompt += f" [{default}]"
            
            prompt += f": {Colors.END}"
            
            response = input(prompt).strip()
            
            if not response and default is not None:
                return choices[default - 1]
            
            if response.isdigit():
                choice_num = int(response)
                if 1 <= choice_num <= len(choices):
                    return choices[choice_num - 1]
            
            self.print_error(f"Please enter a number between 1 and {len(choices)}")
    
    def ask_multiple_choice(self, question: str, choices: List[str], defaults: List[int] = None) -> List[str]:
        """Ask for multiple choices"""
        print(f"{Colors.YELLOW}👉 {question} (Select multiple){Colors.END}")
        
        for i, choice in enumerate(choices, 1):
            default_mark = "✓" if defaults and i in defaults else " "
            print(f"  {Colors.CYAN}[{default_mark}] {i}.{Colors.END} {choice}")
        
        print(f"{Colors.YELLOW}Enter numbers separated by commas (e.g., 1,3,5){Colors.END}")
        
        while True:
            prompt = f"{Colors.YELLOW}Your choices: {Colors.END}"
            response = input(prompt).strip()
            
            if not response and defaults:
                return [choices[i-1] for i in defaults]
            
            try:
                selected_nums = [int(num.strip()) for num in response.split(",")]
                
                # Validate selections
                valid_selections = []
                for num in selected_nums:
                    if 1 <= num <= len(choices):
                        valid_selections.append(choices[num-1])
                    else:
                        self.print_error(f"Invalid choice: {num}")
                
                if valid_selections:
                    return valid_selections
                else:
                    self.print_error("No valid choices selected")
            
            except ValueError:
                self.print_error("Please enter numbers separated by commas")
    
    def ask_table(self, fields: List[Dict]) -> Dict:
        """Ask for multiple fields in a table"""
        results = {}
        
        print(f"{Colors.YELLOW}📋 Please fill the following:{Colors.END}")
        
        for field in fields:
            field_name = field["name"]
            field_type = field.get("type", "text")
            required = field.get("required", True)
            default = field.get("default")
            
            while True:
                if field_type == "text":
                    value = self.ask_text(field_name, default)
                elif field_type == "number":
                    value = self.ask_number(field_name, default=default)
                elif field_type == "choice":
                    value = self.ask_choice(field_name, field["choices"], default)
                elif field_type == "yes_no":
                    value = self.ask_yes_no(field_name, default)
                else:
                    value = self.ask_text(field_name, default)
                
                if required and not value:
                    self.print_error(f"{field_name} is required")
                    continue
                
                results[field["key"]] = value
                break
        
        return results
    
    def show_progress(self, current: int, total: int, message: str = ""):
        """Show progress bar"""
        bar_length = 30
        progress = current / total
        filled_length = int(bar_length * progress)
        
        bar = "█" * filled_length + "░" * (bar_length - filled_length)
        percent = progress * 100
        
        print(f"\r{Colors.CYAN}[{bar}] {percent:.1f}% {message}{Colors.END}", end="")
        
        if current == total:
            print()
    
    def confirm(self, message: str) -> bool:
        """Ask for confirmation"""
        return self.ask_yes_no(f"{message} Continue?", default=True)
    
    def save_responses(self, filename: str = "wizard_responses.json"):
        """Save wizard responses"""
        import json
        from pathlib import Path
        
        save_dir = Path(__file__).parent.parent / "data"
        save_dir.mkdir(exist_ok=True)
        
        save_path = save_dir / filename
        
        with open(save_path, 'w') as f:
            json.dump(self.responses, f, indent=2)
        
        self.print_success(f"Responses saved to {save_path}")
    
    def load_responses(self, filename: str = "wizard_responses.json") -> bool:
        """Load wizard responses"""
        from pathlib import Path
        
        load_path = Path(__file__).parent.parent / "data" / filename
        
        if load_path.exists():
            with open(load_path, 'r') as f:
                self.responses = json.load(f)
            
            self.print_success(f"Loaded responses from {load_path}")
            return True
        
        return False

# Global wizard instance
wizard = InputWizard()
