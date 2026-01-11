#!/usr/bin/env python3
"""
Control Notation Formatter for PC Gaming
Converts various control descriptions into standard notation
"""

import re
from typing import List, Dict, Optional, Tuple
from enum import Enum

class ControlType(Enum):
    """Types of gaming controls"""
    KEYBOARD = "keyboard"
    MOUSE = "mouse"
    COMBO = "combo"
    SEQUENCE = "sequence"

class ControlFormatter:
    """Format gaming controls into standard notation"""
    
    # Common control mappings
    CONTROL_ALIASES = {
        # Movement keys
        'forward': '[W]',
        'backward': '[S]',
        'back': '[S]',
        'left': '[A]',
        'right': '[D]',
        'strafe left': '[A]',
        'strafe right': '[D]',
        
        # Action keys
        'jump': '[Space]',
        'spacebar': '[Space]',
        'space bar': '[Space]',
        'sprint': '[Shift]',
        'run': '[Shift]',
        'crouch': '[Ctrl]',
        'sneak': '[Ctrl]',
        'interact': '[E]',
        'use': '[E]',
        'action': '[E]',
        'reload': '[R]',
        'melee': '[V]',
        'inventory': '[Tab]',
        'map': '[M]',
        
        # Mouse controls
        'shoot': '[LMB]',
        'fire': '[LMB]',
        'attack': '[LMB]',
        'primary': '[LMB]',
        'aim': '[RMB]',
        'ads': '[RMB]',
        'zoom': '[RMB]',
        'secondary': '[RMB]',
        'middle mouse': '[MMB]',
        'scroll up': '[Mouse Wheel Up]',
        'scroll down': '[Mouse Wheel Down]',
        
        # Special keys
        'escape': '[Esc]',
        'enter': '[Enter]',
        'return': '[Enter]',
        'tab': '[Tab]',
        'caps': '[Caps Lock]',
        'alt': '[Alt]',
        'control': '[Ctrl]',
        'shift': '[Shift]',
        
        # Function keys
        'quicksave': '[F5]',
        'quickload': '[F9]',
    }
    
    # Regex patterns for control detection
    PATTERNS = {
        'single_key': r'\b([A-Z0-9])\s+key\b',
        'function_key': r'\b(F\d{1,2})\b',
        'combo': r'(\w+)\s*\+\s*(\w+)',
        'hold': r'hold\s+(?:the\s+)?(\w+)',
        'press': r'press\s+(?:the\s+)?(\w+)',
        'tap': r'tap\s+(?:the\s+)?(\w+)',
        'sequence': r'(\w+)\s*,\s*then\s*(\w+)',
        'mouse_direction': r'move\s+mouse\s+(left|right|up|down)',
    }
    
    def format_instruction(self, instruction: str) -> str:
        """
        Convert natural language control instruction to standard notation
        
        Args:
            instruction: Natural language description
            
        Returns:
            Formatted instruction with standard notation
        """
        formatted = instruction
        
        # First pass: Replace common aliases
        formatted = self._replace_aliases(formatted)
        
        # Second pass: Format remaining controls
        formatted = self._format_controls(formatted)
        
        # Third pass: Format combinations and sequences
        formatted = self._format_combinations(formatted)
        
        # Fourth pass: Add timing indicators
        formatted = self._format_timing(formatted)
        
        return formatted
    
    def _replace_aliases(self, text: str) -> str:
        """Replace common control aliases with standard notation"""
        result = text
        
        # Sort by length to avoid partial replacements
        sorted_aliases = sorted(self.CONTROL_ALIASES.items(), 
                              key=lambda x: len(x[0]), reverse=True)
        
        for alias, notation in sorted_aliases:
            # Case-insensitive replacement
            pattern = re.compile(re.escape(alias), re.IGNORECASE)
            result = pattern.sub(notation, result)
        
        return result
    
    def _format_controls(self, text: str) -> str:
        """Format individual controls into notation"""
        result = text
        
        # Format single letter keys
        result = re.sub(r'\b([A-Z])\b(?!\])', r'[\1]', result)
        
        # Format function keys
        result = re.sub(r'\b(F\d{1,2})\b', r'[\1]', result)
        
        # Format number keys
        result = re.sub(r'\b([1-9]|0)\b(?!\])', r'[\1]', result)
        
        # Format arrow keys
        result = re.sub(r'\b(up|down|left|right)\s+arrow\b', 
                       r'[\1 Arrow]', result, flags=re.IGNORECASE)
        
        return result
    
    def _format_combinations(self, text: str) -> str:
        """Format control combinations and sequences"""
        result = text
        
        # Format "X + Y" combinations
        def format_combo(match):
            key1 = self._ensure_bracketed(match.group(1))
            key2 = self._ensure_bracketed(match.group(2))
            return f"{key1} + {key2}"
        
        # Look for combinations
        combo_pattern = r'(\[?\w+\]?)\s*\+\s*(\[?\w+\]?)'
        result = re.sub(combo_pattern, format_combo, result)
        
        # Format sequences "X then Y"
        def format_sequence(match):
            key1 = self._ensure_bracketed(match.group(1))
            key2 = self._ensure_bracketed(match.group(2))
            return f"{key1}, then {key2}"
        
        sequence_pattern = r'(\[?\w+\]?)\s*,?\s*then\s+(\[?\w+\]?)'
        result = re.sub(sequence_pattern, format_sequence, result)
        
        return result
    
    def _format_timing(self, text: str) -> str:
        """Add timing indicators to controls"""
        result = text
        
        # Format "hold X"
        hold_pattern = r'hold\s+(?:the\s+)?(\[?\w+\]?)'
        result = re.sub(hold_pattern, 
                       lambda m: f"Hold {self._ensure_bracketed(m.group(1))}", 
                       result, flags=re.IGNORECASE)
        
        # Format "tap X"
        tap_pattern = r'tap\s+(?:the\s+)?(\[?\w+\]?)'
        result = re.sub(tap_pattern,
                       lambda m: f"Tap {self._ensure_bracketed(m.group(1))}", 
                       result, flags=re.IGNORECASE)
        
        # Format timed holds
        timed_pattern = r'hold\s+(\[?\w+\]?)\s+for\s+(\d+)\s*(?:seconds?|sec)?'
        result = re.sub(timed_pattern,
                       lambda m: f"Hold {self._ensure_bracketed(m.group(1))} for {m.group(2)} seconds",
                       result, flags=re.IGNORECASE)
        
        return result
    
    def _ensure_bracketed(self, control: str) -> str:
        """Ensure a control is properly bracketed"""
        # If already bracketed, return as-is
        if control.startswith('[') and control.endswith(']'):
            return control
        
        # If it's a known multi-word control, handle specially
        multi_word = ['Mouse Wheel Up', 'Mouse Wheel Down', 'Left Click', 
                     'Right Click', 'Middle Click', 'Left Arrow', 'Right Arrow',
                     'Up Arrow', 'Down Arrow']
        
        for mw in multi_word:
            if mw.lower() in control.lower():
                return f'[{mw}]'
        
        # Single word control
        return f'[{control}]' if control else control
    
    def parse_combo_string(self, combo: str) -> List[str]:
        """Parse a combo string into individual controls"""
        # Remove brackets for parsing
        clean = combo.replace('[', '').replace(']', '')
        
        # Split on + for simultaneous
        if '+' in clean:
            parts = [part.strip() for part in clean.split('+')]
        # Split on , for sequential
        elif ',' in clean:
            parts = [part.strip() for part in clean.split(',')]
        else:
            parts = [clean.strip()]
        
        # Re-bracket each part
        return [f'[{part}]' for part in parts]
    
    def create_control_sequence(self, actions: List[Dict]) -> str:
        """
        Create a formatted control sequence from a list of actions
        
        Args:
            actions: List of dicts with 'control' and 'action' keys
            
        Returns:
            Formatted multi-step instruction
        """
        if not actions:
            return ""
        
        lines = []
        for i, action in enumerate(actions, 1):
            control = self._ensure_bracketed(action.get('control', ''))
            description = action.get('action', '')
            timing = action.get('timing', '')
            
            if timing:
                line = f"{i}. {timing.capitalize()} {control}: {description}"
            else:
                line = f"{i}. Press {control}: {description}"
            
            lines.append(line)
        
        return "\n".join(lines)
    
    def detect_control_type(self, text: str) -> ControlType:
        """Detect what type of control instruction this is"""
        text_lower = text.lower()
        
        if any(mouse in text_lower for mouse in ['mouse', 'click', 'lmb', 'rmb']):
            return ControlType.MOUSE
        elif '+' in text or 'and' in text_lower:
            return ControlType.COMBO
        elif 'then' in text_lower or ',' in text:
            return ControlType.SEQUENCE
        else:
            return ControlType.KEYBOARD

class GameControlLibrary:
    """Library of common game control patterns"""
    
    COMMON_COMBOS = {
        'sprint': '[Shift] + [W]',
        'sprint jump': '[Shift] + [W] + [Space]',
        'slide': '[Shift] + [Ctrl]',
        'dodge roll': '[Alt] + [Direction Key]',
        'quick melee': '[V]',
        'aim down sights': 'Hold [RMB]',
        'charged attack': 'Hold [LMB]',
        'crouch walk': '[Ctrl] + [WASD]',
        'tactical sprint': 'Double-tap [Shift]',
        'interact': 'Hold [E]',
    }
    
    GENRE_DEFAULTS = {
        'fps': {
            'move': '[WASD]',
            'look': '[Mouse Movement]',
            'shoot': '[LMB]',
            'aim': '[RMB]',
            'jump': '[Space]',
            'crouch': '[Ctrl]',
            'sprint': '[Shift]',
            'reload': '[R]',
            'interact': '[E]',
        },
        'rpg': {
            'move': '[WASD]',
            'attack': '[LMB]',
            'block': '[RMB]',
            'dodge': '[Space]',
            'ability1': '[Q]',
            'ability2': '[E]',
            'inventory': '[Tab]',
            'map': '[M]',
        },
        'strategy': {
            'camera': '[WASD] or Edge Scroll',
            'select': '[LMB]',
            'command': '[RMB]',
            'box_select': 'Drag [LMB]',
            'group': '[Ctrl] + [1-9]',
            'attack_move': '[A] + [Click]',
        }
    }
    
    @classmethod
    def get_genre_controls(cls, genre: str) -> Dict[str, str]:
        """Get default controls for a game genre"""
        return cls.GENRE_DEFAULTS.get(genre.lower(), {})
    
    @classmethod
    def get_combo(cls, action: str) -> Optional[str]:
        """Get a common combo notation"""
        return cls.COMMON_COMBOS.get(action.lower())

def format_control_table(controls: Dict[str, str]) -> str:
    """Format controls into a nice table"""
    if not controls:
        return ""
    
    lines = ["**Controls:**"]
    max_action = max(len(action) for action in controls.keys())
    
    for action, control in controls.items():
        action_padded = action.capitalize().ljust(max_action)
        lines.append(f"  {action_padded} : {control}")
    
    return "\n".join(lines)

def main():
    """Example usage"""
    formatter = ControlFormatter()
    
    # Test various input formats
    test_instructions = [
        "Press W to move forward",
        "Hold shift while pressing W to sprint",
        "Press space then ctrl to slide",
        "Use the E key to interact",
        "Click left mouse button to shoot",
        "Press F5 to quicksave",
        "Move mouse left to turn",
        "Press 1, 2, or 3 to switch weapons",
        "Hold E for 2 seconds to revive teammate",
        "Press shift + W + space to sprint jump"
    ]
    
    print("Control Formatting Examples:\n")
    print("-" * 50)
    
    for instruction in test_instructions:
        formatted = formatter.format_instruction(instruction)
        print(f"Input:  {instruction}")
        print(f"Output: {formatted}")
        print()
    
    # Show genre defaults
    print("\nFPS Default Controls:")
    print("-" * 50)
    fps_controls = GameControlLibrary.get_genre_controls('fps')
    print(format_control_table(fps_controls))
    
    # Create a complex sequence
    print("\n\nComplex Action Sequence:")
    print("-" * 50)
    
    sequence = [
        {'control': 'Shift', 'action': 'Start sprinting', 'timing': 'hold'},
        {'control': 'W', 'action': 'Move forward'},
        {'control': 'Space', 'action': 'Jump at the edge', 'timing': 'tap'},
        {'control': 'Ctrl', 'action': 'Air dash', 'timing': 'press'},
        {'control': 'LMB', 'action': 'Attack on landing', 'timing': 'press'}
    ]
    
    formatted_sequence = formatter.create_control_sequence(sequence)
    print(formatted_sequence)

if __name__ == "__main__":
    main()