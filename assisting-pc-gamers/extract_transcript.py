#!/usr/bin/env python3
"""
YouTube Transcript Extraction for Gaming Videos
Extracts transcripts with timestamps for video tutorial analysis
"""

import re
import json
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from datetime import timedelta

@dataclass
class TranscriptSegment:
    """Represents a segment of video transcript"""
    start_time: float  # seconds
    end_time: float
    text: str
    timestamp_str: str  # human-readable format like "1:23"

@dataclass
class VideoTranscript:
    """Complete video transcript with metadata"""
    video_id: str
    title: str
    channel: str
    duration: float
    segments: List[TranscriptSegment]
    key_moments: List[Dict]  # Identified important timestamps

class TranscriptExtractor:
    """Extract and analyze YouTube video transcripts"""
    
    # Gaming-specific keywords for identifying key moments
    KEY_PHRASES = {
        'controls': [
            'press', 'hold', 'tap', 'click', 'button',
            'key', 'mouse', 'keyboard', 'controller'
        ],
        'timing': [
            'wait for', 'as soon as', 'right when', 'after the',
            'before', 'during', 'while', 'at the same time'
        ],
        'location': [
            'go to', 'head to', 'move to', 'jump to',
            'behind', 'in front of', 'next to', 'near the'
        ],
        'strategy': [
            'the trick is', 'the key is', 'make sure',
            'be careful', 'watch out', 'important', 'tip'
        ],
        'items': [
            'you need', 'equip', 'use the', 'switch to',
            'pick up', 'grab the', 'collect'
        ]
    }
    
    def extract_transcript(self, video_url: str) -> Optional[VideoTranscript]:
        """
        Extract transcript from YouTube video
        
        In production, this would use:
        - youtube-transcript-api library
        - YouTube Data API for metadata
        - Fallback to whisper for videos without captions
        """
        video_id = self._extract_video_id(video_url)
        if not video_id:
            return None
        
        # Simulate transcript extraction
        # In production: YouTubeTranscriptApi.get_transcript(video_id)
        
        segments = self._simulate_transcript_segments()
        
        transcript = VideoTranscript(
            video_id=video_id,
            title="Example Gaming Tutorial",
            channel="GamingChannel",
            duration=600.0,  # 10 minutes
            segments=segments,
            key_moments=[]
        )
        
        # Analyze transcript for key moments
        transcript.key_moments = self._identify_key_moments(segments)
        
        return transcript
    
    def _extract_video_id(self, url: str) -> Optional[str]:
        """Extract video ID from various YouTube URL formats"""
        patterns = [
            r'youtube\.com/watch\?v=([a-zA-Z0-9_-]+)',
            r'youtu\.be/([a-zA-Z0-9_-]+)',
            r'youtube\.com/embed/([a-zA-Z0-9_-]+)',
            r'youtube\.com/v/([a-zA-Z0-9_-]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        return None
    
    def _simulate_transcript_segments(self) -> List[TranscriptSegment]:
        """Simulate transcript segments for demonstration"""
        segments = [
            TranscriptSegment(
                start_time=0,
                end_time=5,
                text="Hey everyone, today I'll show you how to beat Malenia.",
                timestamp_str="0:00"
            ),
            TranscriptSegment(
                start_time=5,
                end_time=15,
                text="First, make sure you have the Bloodhound Step ash of war equipped.",
                timestamp_str="0:05"
            ),
            TranscriptSegment(
                start_time=15,
                end_time=25,
                text="When she starts her Waterfowl Dance, immediately press L2 to dash away.",
                timestamp_str="0:15"
            ),
            TranscriptSegment(
                start_time=25,
                end_time=35,
                text="The timing is crucial - wait for her to jump, then dash three times.",
                timestamp_str="0:25"
            ),
            TranscriptSegment(
                start_time=35,
                end_time=45,
                text="For the second phase, stay close to avoid her dive bomb attack.",
                timestamp_str="0:35"
            )
        ]
        return segments
    
    def _identify_key_moments(self, segments: List[TranscriptSegment]) -> List[Dict]:
        """Identify important moments in the transcript"""
        key_moments = []
        
        for segment in segments:
            text_lower = segment.text.lower()
            moment_types = []
            
            # Check for each type of key phrase
            for moment_type, phrases in self.KEY_PHRASES.items():
                if any(phrase in text_lower for phrase in phrases):
                    moment_types.append(moment_type)
            
            if moment_types:
                key_moments.append({
                    'timestamp': segment.timestamp_str,
                    'start_time': segment.start_time,
                    'types': moment_types,
                    'text': segment.text,
                    'importance': len(moment_types)  # More types = more important
                })
        
        # Sort by importance
        key_moments.sort(key=lambda x: x['importance'], reverse=True)
        return key_moments
    
    def format_transcript_for_response(self, transcript: VideoTranscript,
                                      focus_area: Optional[str] = None) -> str:
        """Format transcript for inclusion in response"""
        output = []
        
        output.append(f"**Video:** {transcript.title}")
        output.append(f"**Channel:** {transcript.channel}")
        output.append(f"**Duration:** {self._format_duration(transcript.duration)}\n")
        
        if transcript.key_moments:
            output.append("**Key Moments:**")
            for moment in transcript.key_moments[:5]:  # Top 5 moments
                types = ", ".join(moment['types'])
                output.append(f"[{moment['timestamp']}] ({types})")
                output.append(f"  \"{moment['text']}\"")
            output.append("")
        
        if focus_area:
            output.append(f"**Relevant sections for '{focus_area}':**")
            relevant = self._find_relevant_segments(transcript, focus_area)
            for segment in relevant:
                output.append(f"[{segment.timestamp_str}] {segment.text}")
        else:
            output.append("**Full Transcript:**")
            for segment in transcript.segments:
                output.append(f"[{segment.timestamp_str}] {segment.text}")
        
        return "\n".join(output)
    
    def _find_relevant_segments(self, transcript: VideoTranscript,
                                focus_area: str) -> List[TranscriptSegment]:
        """Find segments relevant to a specific topic"""
        relevant = []
        focus_lower = focus_area.lower()
        
        for segment in transcript.segments:
            if focus_lower in segment.text.lower():
                relevant.append(segment)
            # Also check for related terms
            elif any(word in segment.text.lower() 
                    for word in focus_lower.split()):
                relevant.append(segment)
        
        return relevant
    
    def _format_duration(self, seconds: float) -> str:
        """Format seconds into readable duration"""
        td = timedelta(seconds=seconds)
        hours = td.seconds // 3600
        minutes = (td.seconds % 3600) // 60
        secs = td.seconds % 60
        
        if hours > 0:
            return f"{hours}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes}:{secs:02d}"
    
    def extract_control_sequences(self, transcript: VideoTranscript) -> List[Dict]:
        """Extract control/button sequences from transcript"""
        sequences = []
        
        # Control patterns to look for
        control_patterns = [
            r'press (\w+)',
            r'hold (\w+)',
            r'tap (\w+)',
            r'hit (\w+)',
            r'click (\w+)',
            r'use (\w+) button',
            r'(\w+) \+ (\w+)',  # Combinations
        ]
        
        for segment in transcript.segments:
            for pattern in control_patterns:
                matches = re.findall(pattern, segment.text, re.IGNORECASE)
                if matches:
                    sequences.append({
                        'timestamp': segment.timestamp_str,
                        'controls': matches,
                        'context': segment.text
                    })
        
        return sequences
    
    def create_action_summary(self, transcript: VideoTranscript) -> str:
        """Create a concise action summary from transcript"""
        control_sequences = self.extract_control_sequences(transcript)
        
        if not control_sequences:
            return "No specific control instructions found in transcript."
        
        output = ["**Action Summary:**\n"]
        
        for i, seq in enumerate(control_sequences, 1):
            controls = ", ".join(str(c) for c in seq['controls'])
            output.append(f"{i}. [{seq['timestamp']}] {controls}")
            # Add context if it's not too long
            if len(seq['context']) < 100:
                output.append(f"   Context: {seq['context']}")
            output.append("")
        
        return "\n".join(output)

class VideoSearcher:
    """Search for gaming videos and their transcripts"""
    
    def search_video_solutions(self, game: str, problem: str) -> List[Dict]:
        """
        Search for video solutions to gaming problems
        
        In production would:
        1. Use YouTube Data API for search
        2. Filter by view count, likes, recency
        3. Check for captions availability
        """
        # Simulate video search results
        return [
            {
                'title': f"{game} - {problem} Solution Guide",
                'url': 'https://youtube.com/watch?v=example123',
                'channel': 'ProGamer',
                'views': 50000,
                'likes': 2000,
                'has_captions': True,
                'duration': '5:30'
            },
            {
                'title': f"Easy {problem} Strategy for {game}",
                'url': 'https://youtube.com/watch?v=example456',
                'channel': 'GameGuides',
                'views': 25000,
                'likes': 1500,
                'has_captions': True,
                'duration': '8:45'
            }
        ]
    
    def find_timestamp_for_topic(self, transcript: VideoTranscript,
                                 topic: str) -> Optional[Tuple[str, str]]:
        """Find the timestamp where a specific topic is discussed"""
        topic_lower = topic.lower()
        
        for segment in transcript.segments:
            if topic_lower in segment.text.lower():
                return (segment.timestamp_str, segment.text)
        
        return None

def main():
    """Example usage"""
    extractor = TranscriptExtractor()
    searcher = VideoSearcher()
    
    # Search for videos
    print("Searching for Elden Ring Malenia guides...")
    videos = searcher.search_video_solutions("Elden Ring", "Malenia boss fight")
    
    for video in videos[:2]:
        print(f"\nFound: {video['title']}")
        print(f"Channel: {video['channel']} | Views: {video['views']:,}")
        
        # Extract transcript
        transcript = extractor.extract_transcript(video['url'])
        
        if transcript:
            # Show key moments
            print("\nKey moments identified:")
            for moment in transcript.key_moments[:3]:
                print(f"  [{moment['timestamp']}] {', '.join(moment['types'])}")
            
            # Extract control sequences
            print("\nControl sequences found:")
            sequences = extractor.extract_control_sequences(transcript)
            for seq in sequences[:3]:
                print(f"  [{seq['timestamp']}] Controls: {seq['controls']}")
            
            # Save full analysis
            analysis = {
                'video_id': transcript.video_id,
                'title': transcript.title,
                'key_moments': transcript.key_moments,
                'control_sequences': sequences
            }
            
            with open(f'video_analysis_{transcript.video_id}.json', 'w') as f:
                json.dump(analysis, f, indent=2)
            
            print(f"\nFull analysis saved to video_analysis_{transcript.video_id}.json")

if __name__ == "__main__":
    main()