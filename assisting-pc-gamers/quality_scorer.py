#!/usr/bin/env python3
"""
Quality Scorer for Gaming Forum Solutions
Evaluates and ranks community solutions based on multiple factors
"""

from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, field
import re
import json

@dataclass
class SolutionMetrics:
    """Metrics for evaluating solution quality"""
    # User metrics
    author_reputation: int = 0  # Karma, reputation points
    author_post_count: int = 0  # Total posts by author
    author_badges: List[str] = field(default_factory=list)  # Special badges/roles
    
    # Post metrics
    upvotes: int = 0
    downvotes: int = 0
    reply_count: int = 0
    view_count: int = 0
    
    # Content metrics
    word_count: int = 0
    has_steps: bool = False
    has_screenshots: bool = False
    has_video: bool = False
    code_blocks: int = 0
    
    # Validation metrics
    confirmed_working: int = 0  # Number of "this worked" replies
    contradicted: bool = False  # Has corrections/disagreements
    is_solved: bool = False  # Marked as solution
    dev_response: bool = False  # Developer confirmed
    mod_endorsed: bool = False  # Moderator endorsed
    
    # Temporal metrics
    post_date: Optional[datetime] = None
    last_updated: Optional[datetime] = None
    game_version: Optional[str] = None
    
    # Platform
    platform: str = "unknown"  # reddit, steam, gamefaqs, etc.

class QualityScorer:
    """Score gaming forum solutions for reliability and quality"""
    
    # Weight configuration for different factors
    WEIGHTS = {
        'author_credibility': 0.20,
        'community_validation': 0.25,
        'content_quality': 0.20,
        'official_endorsement': 0.15,
        'recency': 0.10,
        'detail_level': 0.10
    }
    
    # Platform trust multipliers
    PLATFORM_TRUST = {
        'steam': 1.1,      # Developer presence
        'reddit': 1.0,     # Good community validation
        'gamefaqs': 0.95,  # Detailed but sometimes outdated
        'discord': 1.05,   # Real-time verification
        'youtube': 0.9,    # Good for visual but less validated
        'wiki': 0.85,      # May be outdated
        'forum': 0.95      # Generic forums
    }
    
    def calculate_score(self, metrics: SolutionMetrics) -> float:
        """
        Calculate overall quality score (0-100)
        
        Args:
            metrics: Solution metrics to evaluate
            
        Returns:
            Quality score from 0 to 100
        """
        scores = {
            'author_credibility': self._score_author_credibility(metrics),
            'community_validation': self._score_community_validation(metrics),
            'content_quality': self._score_content_quality(metrics),
            'official_endorsement': self._score_official_endorsement(metrics),
            'recency': self._score_recency(metrics),
            'detail_level': self._score_detail_level(metrics)
        }
        
        # Calculate weighted score
        total_score = sum(scores[factor] * self.WEIGHTS[factor] 
                         for factor in scores)
        
        # Apply platform multiplier
        platform_mult = self.PLATFORM_TRUST.get(metrics.platform.lower(), 1.0)
        total_score *= platform_mult
        
        # Apply penalties
        if metrics.contradicted:
            total_score *= 0.8  # 20% penalty for contradicted solutions
        
        return min(max(total_score, 0), 100)  # Clamp to 0-100
    
    def _score_author_credibility(self, metrics: SolutionMetrics) -> float:
        """Score based on author's credibility (0-100)"""
        score = 0
        
        # Reputation/Karma
        if metrics.author_reputation > 10000:
            score += 40
        elif metrics.author_reputation > 5000:
            score += 35
        elif metrics.author_reputation > 1000:
            score += 30
        elif metrics.author_reputation > 500:
            score += 20
        elif metrics.author_reputation > 100:
            score += 10
        
        # Post count (experience)
        if metrics.author_post_count > 1000:
            score += 20
        elif metrics.author_post_count > 500:
            score += 15
        elif metrics.author_post_count > 100:
            score += 10
        elif metrics.author_post_count > 50:
            score += 5
        
        # Special badges/roles
        badge_scores = {
            'moderator': 20,
            'developer': 25,
            'verified': 15,
            'helper': 10,
            'veteran': 10,
            'expert': 15,
            'mvp': 20,
            'trusted': 15
        }
        
        for badge in metrics.author_badges:
            badge_lower = badge.lower()
            for key, points in badge_scores.items():
                if key in badge_lower:
                    score += points
                    break
        
        return min(score, 100)
    
    def _score_community_validation(self, metrics: SolutionMetrics) -> float:
        """Score based on community validation (0-100)"""
        score = 0
        
        # Upvote/downvote ratio
        if metrics.upvotes > 0:
            ratio = metrics.upvotes / max(1, metrics.upvotes + metrics.downvotes)
            if ratio > 0.95:
                score += 30
            elif ratio > 0.85:
                score += 25
            elif ratio > 0.75:
                score += 20
            elif ratio > 0.65:
                score += 15
            else:
                score += 10
        
        # Absolute upvotes
        if metrics.upvotes > 100:
            score += 20
        elif metrics.upvotes > 50:
            score += 15
        elif metrics.upvotes > 20:
            score += 10
        elif metrics.upvotes > 10:
            score += 5
        
        # Confirmations
        score += min(metrics.confirmed_working * 10, 30)
        
        # Engagement (replies)
        if metrics.reply_count > 20:
            score += 15
        elif metrics.reply_count > 10:
            score += 10
        elif metrics.reply_count > 5:
            score += 5
        
        # View count (if available)
        if metrics.view_count > 10000:
            score += 5
        elif metrics.view_count > 1000:
            score += 3
        
        return min(score, 100)
    
    def _score_content_quality(self, metrics: SolutionMetrics) -> float:
        """Score based on content quality (0-100)"""
        score = 0
        
        # Has structured steps
        if metrics.has_steps:
            score += 25
        
        # Visual aids
        if metrics.has_screenshots:
            score += 20
        if metrics.has_video:
            score += 15
        
        # Code/commands included
        if metrics.code_blocks > 0:
            score += min(metrics.code_blocks * 5, 15)
        
        # Appropriate length
        if 100 <= metrics.word_count <= 500:
            score += 15
        elif 50 <= metrics.word_count < 100:
            score += 10
        elif 500 < metrics.word_count <= 1000:
            score += 10
        elif metrics.word_count > 1000:
            score += 5
        
        # Solution marked
        if metrics.is_solved:
            score += 10
        
        return min(score, 100)
    
    def _score_official_endorsement(self, metrics: SolutionMetrics) -> float:
        """Score based on official endorsement (0-100)"""
        score = 0
        
        if metrics.dev_response:
            score += 50
        
        if metrics.mod_endorsed:
            score += 30
        
        if metrics.is_solved:
            score += 20
        
        return min(score, 100)
    
    def _score_recency(self, metrics: SolutionMetrics) -> float:
        """Score based on recency (0-100)"""
        if not metrics.post_date:
            return 50  # Neutral score if no date
        
        age = datetime.now() - metrics.post_date
        
        if age < timedelta(days=7):
            return 100
        elif age < timedelta(days=30):
            return 90
        elif age < timedelta(days=90):
            return 75
        elif age < timedelta(days=180):
            return 60
        elif age < timedelta(days=365):
            return 40
        else:
            return 20
    
    def _score_detail_level(self, metrics: SolutionMetrics) -> float:
        """Score based on detail level (0-100)"""
        score = 0
        
        # Word count indicates detail
        if metrics.word_count > 200:
            score += 30
        elif metrics.word_count > 100:
            score += 20
        elif metrics.word_count > 50:
            score += 10
        
        # Structured content
        if metrics.has_steps:
            score += 30
        
        # Supporting materials
        if metrics.has_screenshots or metrics.has_video:
            score += 20
        
        # Technical details (code blocks)
        if metrics.code_blocks > 0:
            score += 20
        
        return min(score, 100)
    
    def analyze_content(self, content: str) -> Dict[str, any]:
        """
        Analyze post content to extract quality indicators
        
        Args:
            content: Post text content
            
        Returns:
            Dictionary of extracted metrics
        """
        analysis = {
            'word_count': len(content.split()),
            'has_steps': False,
            'has_screenshots': False,
            'has_video': False,
            'code_blocks': 0,
            'confirmed_working': 0,
            'has_warnings': False
        }
        
        # Check for numbered steps
        step_patterns = [
            r'\d+\.',  # 1. 2. 3.
            r'Step \d+',  # Step 1, Step 2
            r'First.*Second.*Third',  # First, Second, Third
        ]
        for pattern in step_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                analysis['has_steps'] = True
                break
        
        # Check for images
        image_indicators = ['screenshot', 'image', '.png', '.jpg', '![']
        analysis['has_screenshots'] = any(ind in content.lower() 
                                         for ind in image_indicators)
        
        # Check for videos
        video_indicators = ['video', 'youtube', 'youtu.be', 'twitch']
        analysis['has_video'] = any(ind in content.lower() 
                                   for ind in video_indicators)
        
        # Count code blocks
        analysis['code_blocks'] = len(re.findall(r'```', content))
        
        # Check for confirmations
        confirmation_phrases = [
            'this worked', 'works for me', 'can confirm',
            'solved my problem', 'fixed it', 'thanks this helped'
        ]
        for phrase in confirmation_phrases:
            analysis['confirmed_working'] += len(re.findall(phrase, content, 
                                                           re.IGNORECASE))
        
        # Check for warnings
        warning_phrases = [
            'be careful', 'warning', 'caution', 'important',
            'make sure', 'don\'t forget', 'backup'
        ]
        analysis['has_warnings'] = any(phrase in content.lower() 
                                      for phrase in warning_phrases)
        
        return analysis
    
    def compare_solutions(self, solutions: List[Tuple[SolutionMetrics, str]]) -> List[Dict]:
        """
        Compare and rank multiple solutions
        
        Args:
            solutions: List of (metrics, content) tuples
            
        Returns:
            Ranked list with scores and analysis
        """
        ranked = []
        
        for metrics, content in solutions:
            # Analyze content
            content_analysis = self.analyze_content(content)
            
            # Update metrics with content analysis
            metrics.word_count = content_analysis['word_count']
            metrics.has_steps = content_analysis['has_steps']
            metrics.has_screenshots = content_analysis['has_screenshots']
            metrics.has_video = content_analysis['has_video']
            metrics.code_blocks = content_analysis['code_blocks']
            
            # Calculate score
            score = self.calculate_score(metrics)
            
            ranked.append({
                'score': score,
                'metrics': metrics,
                'content_preview': content[:200] + '...' if len(content) > 200 else content,
                'strengths': self._identify_strengths(metrics),
                'weaknesses': self._identify_weaknesses(metrics)
            })
        
        # Sort by score
        ranked.sort(key=lambda x: x['score'], reverse=True)
        
        return ranked
    
    def _identify_strengths(self, metrics: SolutionMetrics) -> List[str]:
        """Identify strengths of a solution"""
        strengths = []
        
        if metrics.dev_response:
            strengths.append("Developer confirmed")
        if metrics.is_solved:
            strengths.append("Marked as solution")
        if metrics.confirmed_working > 2:
            strengths.append(f"{metrics.confirmed_working} users confirmed working")
        if metrics.has_steps:
            strengths.append("Step-by-step instructions")
        if metrics.has_screenshots or metrics.has_video:
            strengths.append("Visual aids included")
        if metrics.upvotes > 50:
            strengths.append(f"Highly upvoted ({metrics.upvotes})")
        if metrics.author_reputation > 5000:
            strengths.append("Trusted author")
        
        return strengths
    
    def _identify_weaknesses(self, metrics: SolutionMetrics) -> List[str]:
        """Identify weaknesses of a solution"""
        weaknesses = []
        
        if metrics.contradicted:
            weaknesses.append("Has contradicting replies")
        if metrics.downvotes > metrics.upvotes * 0.3:
            weaknesses.append("Significant downvotes")
        if metrics.post_date and (datetime.now() - metrics.post_date) > timedelta(days=365):
            weaknesses.append("Over 1 year old")
        if metrics.word_count < 50:
            weaknesses.append("Very brief explanation")
        if not metrics.has_steps and metrics.word_count > 200:
            weaknesses.append("Lacks structure")
        
        return weaknesses

class SolutionRanker:
    """Rank multiple solutions for the same problem"""
    
    def __init__(self):
        self.scorer = QualityScorer()
    
    def rank_solutions(self, solutions: List[Dict]) -> List[Dict]:
        """
        Rank solutions and provide recommendations
        
        Args:
            solutions: List of solution dictionaries
            
        Returns:
            Ranked and annotated solutions
        """
        # Convert to metrics objects
        metrics_list = []
        for solution in solutions:
            metrics = self._dict_to_metrics(solution)
            content = solution.get('content', '')
            metrics_list.append((metrics, content))
        
        # Score and rank
        ranked = self.scorer.compare_solutions(metrics_list)
        
        # Add recommendations
        for i, solution in enumerate(ranked):
            solution['recommendation'] = self._get_recommendation(
                solution, i, len(ranked)
            )
            solution['trust_level'] = self._get_trust_level(solution['score'])
        
        return ranked
    
    def _dict_to_metrics(self, solution_dict: Dict) -> SolutionMetrics:
        """Convert dictionary to SolutionMetrics object"""
        metrics = SolutionMetrics()
        
        # Map dictionary fields to metrics
        field_mapping = {
            'author_reputation': 'author_reputation',
            'upvotes': 'upvotes',
            'score': 'upvotes',  # Alternative name
            'downvotes': 'downvotes',
            'replies': 'reply_count',
            'is_solved': 'is_solved',
            'platform': 'platform',
            'has_dev_response': 'dev_response',
            'author_badges': 'author_badges'
        }
        
        for dict_key, metric_field in field_mapping.items():
            if dict_key in solution_dict:
                setattr(metrics, metric_field, solution_dict[dict_key])
        
        # Parse date if provided
        if 'date' in solution_dict:
            try:
                if isinstance(solution_dict['date'], str):
                    metrics.post_date = datetime.fromisoformat(solution_dict['date'])
                else:
                    metrics.post_date = solution_dict['date']
            except:
                pass
        
        return metrics
    
    def _get_recommendation(self, solution: Dict, rank: int, total: int) -> str:
        """Get recommendation for a solution based on rank and score"""
        score = solution['score']
        
        if rank == 0 and score > 80:
            return "⭐ Highly Recommended - Best solution available"
        elif rank == 0 and score > 60:
            return "✓ Recommended - Most reliable solution found"
        elif score > 70:
            return "✓ Good Alternative - Worth trying if primary fails"
        elif score > 50:
            return "⚠ Use with caution - Some validation needed"
        else:
            return "⚠ Last resort - Limited validation available"
    
    def _get_trust_level(self, score: float) -> str:
        """Get trust level description"""
        if score >= 80:
            return "Very High"
        elif score >= 65:
            return "High"
        elif score >= 50:
            return "Moderate"
        elif score >= 35:
            return "Low"
        else:
            return "Very Low"
    
    def generate_summary_report(self, ranked_solutions: List[Dict]) -> str:
        """Generate a summary report of ranked solutions"""
        if not ranked_solutions:
            return "No solutions found to evaluate."
        
        report = []
        report.append("📊 **Solution Quality Analysis**\n")
        
        # Best solution
        best = ranked_solutions[0]
        report.append(f"**Best Solution** (Score: {best['score']:.1f}/100)")
        report.append(f"Trust Level: {best['trust_level']}")
        report.append(f"Platform: {best['metrics'].platform.title()}")
        
        if best['strengths']:
            report.append(f"Strengths: {', '.join(best['strengths'])}")
        if best['weaknesses']:
            report.append(f"Cautions: {', '.join(best['weaknesses'])}")
        
        report.append(f"\n{best['recommendation']}\n")
        
        # Alternative solutions
        if len(ranked_solutions) > 1:
            report.append("**Alternative Solutions:**")
            for solution in ranked_solutions[1:4]:  # Show top 3 alternatives
                report.append(f"• Score {solution['score']:.1f}: {solution['recommendation']}")
        
        # Overall confidence
        avg_score = sum(s['score'] for s in ranked_solutions) / len(ranked_solutions)
        report.append(f"\n**Overall Confidence:** {self._get_confidence_level(avg_score)}")
        
        return "\n".join(report)
    
    def _get_confidence_level(self, avg_score: float) -> str:
        """Get overall confidence level"""
        if avg_score >= 70:
            return "✅ High - Multiple validated solutions available"
        elif avg_score >= 50:
            return "⚠️ Moderate - Solutions available but need verification"
        else:
            return "⚠️ Low - Limited or unverified solutions"

def main():
    """Example usage of quality scorer"""
    ranker = SolutionRanker()
    
    # Example solutions to evaluate
    solutions = [
        {
            'platform': 'reddit',
            'content': """
            Here's how to beat Malenia:
            
            1. First, equip the Bloodhound Step ash of war
            2. Use a bleed weapon like Rivers of Blood
            3. When she does Waterfowl Dance, immediately dash away
            4. Stay close in phase 2 to avoid her dive bomb
            
            This worked perfectly for me and 5 others in this thread!
            """,
            'upvotes': 156,
            'downvotes': 3,
            'replies': 23,
            'is_solved': True,
            'author_reputation': 8500,
            'date': datetime.now() - timedelta(days=10),
            'author_badges': ['trusted']
        },
        {
            'platform': 'steam',
            'content': "Just use mimic tear and spam magic. Easy.",
            'upvotes': 45,
            'downvotes': 20,
            'replies': 8,
            'has_dev_response': False,
            'author_reputation': 200,
            'date': datetime.now() - timedelta(days=60)
        },
        {
            'platform': 'gamefaqs',
            'content': """
            Complete Malenia Strategy Guide
            
            Phase 1:
            - Stay at medium range
            - Dodge into her attacks
            - Punish after her combos
            
            Phase 2:
            - Similar strategy but watch for rot
            - Her opening is always the flower dive
            
            Equipment recommendations:
            - 60+ Vigor
            - Heavy armor
            - Greatshield helps
            
            [Screenshot of positioning]
            [Video guide linked]
            
            This has been confirmed by dozens of users.
            """,
            'upvotes': 89,
            'replies': 45,
            'author_reputation': 15000,
            'author_badges': ['expert', 'veteran'],
            'date': datetime.now() - timedelta(days=30)
        }
    ]
    
    # Rank solutions
    ranked = ranker.rank_solutions(solutions)
    
    # Display individual scores
    print("Individual Solution Scores:\n")
    print("-" * 60)
    
    for i, solution in enumerate(ranked, 1):
        print(f"\nSolution #{i}")
        print(f"Score: {solution['score']:.1f}/100")
        print(f"Platform: {solution['metrics'].platform}")
        print(f"Trust Level: {solution['trust_level']}")
        print(f"Recommendation: {solution['recommendation']}")
        
        if solution['strengths']:
            print(f"Strengths: {', '.join(solution['strengths'])}")
        if solution['weaknesses']:
            print(f"Weaknesses: {', '.join(solution['weaknesses'])}")
        
        print(f"Preview: {solution['content_preview']}")
    
    # Generate summary report
    print("\n" + "=" * 60)
    print("\nSummary Report:")
    print("-" * 60)
    summary = ranker.generate_summary_report(ranked)
    print(summary)
    
    # Export to JSON
    export_data = []
    for solution in ranked:
        export_data.append({
            'score': solution['score'],
            'trust_level': solution['trust_level'],
            'platform': solution['metrics'].platform,
            'recommendation': solution['recommendation'],
            'strengths': solution['strengths'],
            'weaknesses': solution['weaknesses']
        })
    
    with open('solution_rankings.json', 'w') as f:
        json.dump(export_data, f, indent=2)
    
    print("\n✅ Rankings exported to solution_rankings.json")

if __name__ == "__main__":
    main()