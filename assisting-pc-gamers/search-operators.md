# Advanced Search Operators Guide

## Reddit Search Operators

### Field Operators
```
title:"exact phrase"        # Search only in post titles
selftext:"search term"      # Search in post body text
subreddit:gaming           # Limit to specific subreddit
author:username            # Posts by specific user
flair:Help                # Posts with specific flair
url:youtube.com           # Posts containing specific URL
self:yes                  # Text posts only (no links)
self:no                   # Link posts only
is_video:true             # Video posts only
over_18:no               # Exclude NSFW content
```

### Boolean Operators
```
AND                       # Both terms (default)
OR                        # Either term
NOT or -                  # Exclude term
"exact phrase"            # Exact phrase match
(grouping)               # Group terms
```

### Time Operators
```
after:2024               # Posts after year
after:2024-01-15        # Posts after specific date
before:2024-12-31       # Posts before date
timestamp:1609459200..1704067200  # Unix timestamp range
```

### Sorting
```
sort:top                 # Highest score
sort:new                # Most recent
sort:comments           # Most comments
sort:relevance          # Best match (default)
```

### Example Searches
```
# Find recent help threads for Elden Ring boss
subreddit:eldenring title:"help" OR title:"stuck" flair:Question after:2024 sort:top

# Technical issues with specific error
subreddit:pcgaming "crash" "error 0x80070057" -mod self:yes

# Find video guides
subreddit:gaming url:youtube.com title:"guide" OR title:"walkthrough" after:2024-06

# High-quality solutions
(title:"solved" OR flair:Solved) subreddit:darksouls3 self:yes sort:top
```

## Google Search Operators (for forums)

### Site-Specific
```
site:reddit.com                    # Search only Reddit
site:steamcommunity.com/app/       # Steam game forums
site:gamefaqs.gamespot.com         # GameFAQs
site:forums.nexusmods.com          # Nexus mod forums
-site:youtube.com                  # Exclude YouTube
```

### Text Operators
```
"exact phrase"                     # Exact match
+mandatory                        # Must include word
-exclude                          # Exclude word
word1 OR word2                    # Either word
word1..word2                      # Number range
*wildcard                         # Wildcard character
define:term                       # Definition
```

### Time Filters
```
after:2024                        # Content after year
after:2024-01-01                 # After specific date
before:2024-12-31                # Before date
daterange:2024-01-01..2024-12-31 # Date range
```

### File Type
```
filetype:pdf                      # PDF guides
filetype:txt                      # Text files
ext:pdf                          # Alternative syntax
```

### Advanced
```
intitle:"search term"             # In page title
inurl:walkthrough                # In URL
intext:"exact phrase"            # In body text
allintext:word1 word2            # All words in text
related:reddit.com/r/gaming      # Similar sites
cache:url                        # Cached version
```

### Example Searches
```
# Find Steam forum solutions for specific crash
site:steamcommunity.com/app/ "Cyberpunk 2077" "crash on startup" after:2024

# GameFAQs walkthrough for specific section
site:gamefaqs.gamespot.com "Final Fantasy XVI" "Chapter 5" walkthrough

# Exclude video results, find text guides
"Baldur's Gate 3" "build guide" -site:youtube.com -video

# Recent patch discussions
"Helldivers 2" "patch notes" OR "update" after:2024-10-01 site:reddit.com
```

## Steam Search Tips

### URL Patterns
```
steamcommunity.com/app/[APPID]/discussions/    # Game forums
steamcommunity.com/app/[APPID]/guides/        # Game guides
steamcommunity.com/id/[USER]/recommended/     # User reviews
store.steampowered.com/app/[APPID]/          # Store page
```

### Finding App IDs
```
# Search Google for:
"[Game Name]" site:steamcommunity.com/app/

# Or check store URL:
store.steampowered.com/app/1245620/  # 1245620 is Elden Ring
```

### Guide Filters
```
# Via Google:
site:steamcommunity.com/app/1245620/guides/ "boss guide"

# Categories to check:
/guides/?browsesort=toprated     # Highest rated
/guides/?browsesort=mostrecent   # Newest
/guides/?browsesort=trend        # Trending
```

### Discussion Search
```
# Pinned topics (common issues)
"[PINNED]" site:steamcommunity.com/app/[APPID]/discussions/

# Solved problems
"[SOLVED]" site:steamcommunity.com/app/[APPID]/discussions/

# Developer posts
"developer" site:steamcommunity.com/app/[APPID]/discussions/
```

## GameFAQs Search Patterns

### Board Types
```
/boards/[PLATFORM]-[GAMEID]      # Platform-specific board
/boards/[GAMEID]                 # General board
/boards/[GENRE]                  # Genre board
```

### Google Search for GameFAQs
```
site:gamefaqs.gamespot.com "[Game]" "[Problem]" answers
site:gamefaqs.gamespot.com/boards "[Game]" FAQ
site:gamefaqs.gamespot.com "[Game]" "sticky" OR "pinned"
```

### Quality Indicators
```
# High-quality threads
"[STICKY]" OR "[PINNED]"         # Official important topics
"karma given"                     # Helpful responses
"accepted answer"                 # Solution confirmed
```

## YouTube Search (for transcripts)

### Direct Searches
```
"[video title]" transcript
"[video title]" subtitles
"[video title]" closed captions
"[channel name]" "[game]" transcript
```

### Finding Videos with Good Transcripts
```
"[game]" walkthrough "cc" OR "subtitles"
"[game]" guide "full transcript"
"[game]" tutorial "English captions"
```

### Cross-Reference Text Guides
```
"[YouTuber name]" "[game]" written guide
"[YouTuber name]" "[game]" blog post
"[YouTuber name]" "[game]" text version
```

## Discord Search (via Google)

### Public Discord Servers
```
site:discord.com "[game]" server invite
site:discord.gg "[game]" community
site:top.gg "[game]" discord
```

### Discord FAQ Channels
```
"[game]" discord FAQ OR pinned
"[game]" discord resources
"[game]" discord guides
```

## Search Query Templates

### Stuck/Progression
```
"[game]" stuck "can't progress" "[location]" -walkthrough
"[game]" "where to go after" "[event]" site:reddit.com
"[game]" "[area]" "won't open" OR "locked" solution
```

### Boss/Combat
```
"[game]" "[boss name]" strategy -wiki -ign after:2024
"[game]" "[boss]" "cheese" OR "easy" site:reddit.com
"[game]" beat "[boss]" "first try" tips
```

### Technical Issues
```
"[game]" "[error code]" fix after:2024
"[game]" crash "on startup" OR "launch" solution
"[game]" "black screen" OR "won't start" "[GPU brand]"
```

### Achievements/Collectibles
```
"[game]" "[achievement name]" guide -youtube
"[game]" missable achievements OR trophies list
"[game]" "100%" OR "completion" guide after:2024
```

### Puzzle Solutions
```
"[game]" "[puzzle name]" solution -video
"[game]" "[area]" puzzle "code" OR "combination"
"[game]" "[item]" "how to use" OR "where to use"
```

## Platform-Specific Quality Signals

### Reddit Quality
```
score:>100               # High upvotes
num_comments:>20        # Good discussion
flair:Solved            # Confirmed solution
author:AutoModerator    # Official threads
```

### Steam Quality
```
[SOLVED] in title       # Fixed issue
Developer response      # Official answer
Pinned by moderator    # Important info
High award count       # Community validated
```

### GameFAQs Quality
```
Karma: 100+            # Trusted user
Sticky topic           # Essential info
FAQ status            # Comprehensive guide
Board veteran         # Experienced helper
```

## Rate Limiting Considerations

### Safe Search Intervals
```
Reddit API: 60 requests/minute
Google Search: 100-150/hour (vary to avoid detection)
Steam: No official API, 3-5 second delays
GameFAQs: 5-10 second delays
```

### Distributed Searching
```
1. Start with Reddit (API-friendly)
2. Then Google site-specific (moderate)
3. Finally direct site access (careful)
4. Cache results for 24-48 hours
```

## Query Optimization Tips

### Start Broad, Then Narrow
```
Initial: "[game]" boss help
Narrow: "[game]" "[specific boss]" phase 2
Specific: "[game]" "[boss]" "one shot attack" dodge
```

### Use Error Messages
```
Include exact error text in quotes
Add system specs if technical
Include patch version if known
```

### Version Awareness
```
Add "after:[recent-patch-date]"
Include "current patch" or "[version]"
Exclude outdated: -"old patch" -"outdated"
```

### Multi-Platform Searches
```
Search all major platforms in order:
1. Reddit (community solutions)
2. Steam (technical + official)
3. GameFAQs (detailed guides)
4. YouTube (visual guides)
5. Discord (real-time help)
```