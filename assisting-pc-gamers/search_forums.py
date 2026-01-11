#!/usr/bin/env python3
"""
Forum Search Script for Gaming Help
Searches multiple gaming forums and scores results for quality
"""

import time
import re
from typing import Dict, List, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
import json

@dataclass
class ForumPost:
    """Represents a forum post/thread"""
    title: str
    content: str
    url: str
    author: str
    platform: str  # reddit, steam, gamefaqs
    score: int  # upvotes, kudos, etc.
    replies: int
    date: datetime
    is_solved: bool
    has_dev_response: bool
    quality_score: float = 0.0

class ForumSearcher:
    """Multi-platform forum searcher with quality scoring"""
    
    # Platform-specific search patterns
    SEARCH_PATTERNS = {
        'stuck': [
            '{game} stuck "{location}"',
            '{game} "can\'t progress" {location}',
            '{game} "where to go after" {location}',
            '{game} {location} walkthrough'
        ],
        'boss': [
            '{game} {boss} strategy',
            '{game} "how to beat" {boss}',
            '{game} {boss} tips guide',
            '{game} defeat {boss} help'
        ],
        'technical': [
            '{game} {error} fix',
            '{game} crash {error} solution',
            '{game} "won\'t start" {error}',
            '{game} bug {error} workaround'
        ],
        'item': [
            '{game} "where to find" {item}',
            '{game} {item} location',
            '{game} "how to get" {item}',
            '{game} {item} guide'
        ]
    }
    
    def __init__(self):
        self.rate_limits = {
            'reddit': {'calls': 0, 'reset_time': datetime.now()},
            'steam': {'calls': 0, 'reset_time': datetime.now()},
            'gamefaqs': {'calls': 0, 'reset_time': datetime.now()}
        }
    
    def search_all_platforms(self, game: str, problem_type: str, 
                            specific_term: str) -> List[ForumPost]:
        """
        Search all gaming platforms for solutions
        
        Args:
            game: Game name
            problem_type: Type of problem (stuck, boss, technical, item)
            specific_term: Specific location/boss/error/item
            
        Returns:
            List of ForumPost objects sorted by quality score
        """
        results = []
        
        # Get search queries for this problem type
        queries = self._build_queries(game, problem_type, specific_term)
        
        # Search each platform
        for query in queries:
            results.extend(self._search_reddit(query))
            results.extend(self._search_steam(query))
            results.extend(self._search_gamefaqs(query))
        
        # Score and sort results
        scored_results = [self._calculate_quality_score(post) for post in results]
        return sorted(scored_results, key=lambda x: x.quality_score, reverse=True)
    
    def _build_queries(self, game: str, problem_type: str, 
                      specific_term: str) -> List[str]:
        """Build search queries based on problem type"""
        if problem_type not in self.SEARCH_PATTERNS:
            # Generic search
            return [f'{game} {specific_term} help']
        
        queries = []
        for pattern in self.SEARCH_PATTERNS[problem_type]:
            # Handle different placeholder names
            query = pattern.format(
                game=game,
                location=specific_term,
                boss=specific_term,
                error=specific_term,
                item=specific_term
            )
            queries.append(query)
        
        return queries
    
    def _search_reddit(self, query: str) -> List[ForumPost]:
        """
        Search Reddit (simulated - would use PRAW in production)
        
        In production, this would:
        1. Use PRAW (Python Reddit API Wrapper)
        2. Search specific game subreddits first
        3. Fall back to general gaming subreddits
        """
        self._check_rate_limit('reddit', limit=60, window=60)
        
        # Simulated search results
        results = []
        
        # Build Reddit-specific query
        reddit_query = f'{query} (subreddit:gaming OR subreddit:pcgaming)'
        
        # Simulate finding posts
        # In production: reddit.subreddit('all').search(reddit_query, limit=10)
        
        example_post = ForumPost(
            title=f"Help with {query}",
            content="[This would be actual Reddit post content]",
            url="https://reddit.com/r/gaming/example",
            author="helpful_gamer",
            platform="reddit",
            score=156,
            replies=23,
            date=datetime.now() - timedelta(days=5),
            is_solved=True,
            has_dev_response=False
        )
        results.append(example_post)
        
        return results
    
    def _search_steam(self, query: str) -> List[ForumPost]:
        """
        Search Steam Forums (via web scraping)
        
        In production:
        1. Use requests + BeautifulSoup
        2. Search game-specific forums
        3. Look for [SOLVED] tags and dev responses
        """
        self._check_rate_limit('steam', limit=20, window=60)
        time.sleep(3)  # Respectful delay
        
        results = []
        
        # Simulate Steam forum search
        # URL would be: f'https://steamcommunity.com/app/{app_id}/discussions/search/?q={query}'
        
        example_post = ForumPost(
            title=f"[SOLVED] {query}",
            content="[Steam forum post content]",
            url="https://steamcommunity.com/app/12345/discussions/0/example",
            author="steam_user",
            platform="steam",
            score=45,
            replies=12,
            date=datetime.now() - timedelta(days=2),
            is_solved=True,
            has_dev_response=True  # Steam shows dev responses clearly
        )
        results.append(example_post)
        
        return results
    
    def _search_gamefaqs(self, query: str) -> List[ForumPost]:
        """
        Search GameFAQs Boards
        
        In production:
        1. Use requests + BeautifulSoup
        2. Search game-specific message boards
        3. Check for sticky topics and FAQ status
        """
        self._check_rate_limit('gamefaqs', limit=10, window=60)
        time.sleep(5)  # Extra careful with GameFAQs
        
        results = []
        
        # Simulate GameFAQs search
        # Would scrape: f'https://gamefaqs.gamespot.com/search?game={query}'
        
        example_post = ForumPost(
            title=f"Complete guide for {query}",
            content="[GameFAQs detailed walkthrough]",
            url="https://gamefaqs.gamespot.com/boards/12345-game/12345678",
            author="FAQ_Master",
            platform="gamefaqs",
            score=89,  # Karma on GameFAQs
            replies=45,
            date=datetime.now() - timedelta(days=30),
            is_solved=False,  # GameFAQs doesn't have solved tags
            has_dev_response=False
        )
        results.append(example_post)
        
        return results
    
    def _calculate_quality_score(self, post: ForumPost) -> ForumPost:
        """
        Calculate quality score for a forum post
        
        Scoring factors:
        - User reputation (score/karma)
        - Community validation (replies)
        - Solution confirmation (is_solved)
        - Official response (has_dev_response)
        - Recency (date)
        - Platform trust level
        """
        score = 0.0
        
        # User reputation (0-30 points)
        if post.score > 100:
            score += 30
        elif post.score > 50:
            score += 20
        elif post.score > 10:
            score += 10
        
        # Community validation (0-20 points)
        if post.replies > 20:
            score += 20
        elif post.replies > 10:
            score += 15
        elif post.replies > 5:
            score += 10
        
        # Solution confirmation (0-20 points)
        if post.is_solved:
            score += 20
        
        # Developer response (0-15 points)
        if post.has_dev_response:
            score += 15
        
        # Recency (0-15 points)
        days_old = (datetime.now() - post.date).days
        if days_old < 7:
            score += 15
        elif days_old < 30:
            score += 10
        elif days_old < 90:
            score += 5
        
        # Platform bonuses
        platform_trust = {
            'reddit': 1.0,  # Good for recent issues
            'steam': 1.1,   # Developer responses
            'gamefaqs': 0.9  # Good for detailed guides
        }
        score *= platform_trust.get(post.platform, 1.0)
        
        post.quality_score = min(score, 100.0)  # Cap at 100
        return post
    
    def _check_rate_limit(self, platform: str, limit: int, window: int):
        """Check and enforce rate limits"""
        now = datetime.now()
        rate_info = self.rate_limits[platform]
        
        # Reset window if needed
        if (now - rate_info['reset_time']).seconds >= window:
            rate_info['calls'] = 0
            rate_info['reset_time'] = now
        
        # Check if we're at limit
        if rate_info['calls'] >= limit:
            sleep_time = window - (now - rate_info['reset_time']).seconds
            if sleep_time > 0:
                print(f"Rate limit reached for {platform}, sleeping {sleep_time}s")
                time.sleep(sleep_time)
                rate_info['calls'] = 0
                rate_info['reset_time'] = datetime.now()
        
        rate_info['calls'] += 1

def format_solution(posts: List[ForumPost], max_results: int = 5) -> str:
    """Format the top forum posts into a solution response"""
    if not posts:
        return "No solutions found. Try broadening your search terms."
    
    output = []
    output.append("Found solutions from the community:\n")
    
    for i, post in enumerate(posts[:max_results], 1):
        quality_indicator = "✓" if post.is_solved else ""
        dev_indicator = "👨‍💻" if post.has_dev_response else ""
        
        output.append(f"\n**Solution {i}** {quality_indicator}{dev_indicator}")
        output.append(f"Source: {post.platform.title()} | Score: {post.quality_score:.1f}")
        output.append(f"Title: {post.title}")
        output.append(f"Upvotes: {post.score} | Replies: {post.replies}")
        output.append(f"Posted: {post.date.strftime('%Y-%m-%d')}")
        output.append(f"URL: {post.url}")
        output.append(f"Preview: {post.content[:200]}...")
        output.append("-" * 40)
    
    # Add legend
    output.append("\n✓ = Marked as solved")
    output.append("👨‍💻 = Developer responded")
    output.append("\nHighest quality score indicates most reliable solution.")
    
    return "\n".join(output)

def main():
    """Example usage of the forum searcher"""
    searcher = ForumSearcher()
    
    # Example search
    print("Searching for Elden Ring boss help...")
    results = searcher.search_all_platforms(
        game="Elden Ring",
        problem_type="boss",
        specific_term="Malenia"
    )
    
    # Display formatted results
    print(format_solution(results))
    
    # Export results as JSON for further processing
    results_dict = [
        {
            'title': post.title,
            'url': post.url,
            'platform': post.platform,
            'quality_score': post.quality_score,
            'is_solved': post.is_solved
        }
        for post in results[:10]
    ]
    
    with open('search_results.json', 'w') as f:
        json.dump(results_dict, f, indent=2)
    
    print(f"\nExported top {len(results_dict)} results to search_results.json")

if __name__ == "__main__":
    main()