---
name: pc-gaming-help
description: Expert PC gaming assistance through community forum retrieval, video analysis, and step-by-step solutions. Use when players ask for help with game puzzles, boss strategies, getting unstuck, control questions, progression blocks, technical issues, achievements, or need video walkthroughs explained. Searches Reddit threads, Steam forums, GameFAQs boards, and processes YouTube videos through transcripts. Provides solutions with proper PC keyboard/mouse notation (WASD, [Shift], [Space], [LMB], etc). Triggers on phrases like "stuck in", "can't beat", "how do I", "where is", "won't work", "bug in", "help with game", or any gaming-related troubleshooting request.
---

# PC Gaming Help Expert

Comprehensive system for helping PC gamers overcome obstacles through community-sourced solutions and video analysis.

## Core Workflow

1. **Identify the problem** - Determine if player is stuck (puzzle/progression), needs strategy (boss/combat), has technical issues (bugs/crashes), or wants control help
2. **Search community forums** - Prioritize Reddit discussions, Steam threads, and GameFAQs boards over wikis
3. **Process video content** - When videos are referenced, extract transcripts and analyze key moments
4. **Synthesize solution** - Combine multiple sources into clear, step-by-step instructions
5. **Format for PC controls** - Use standard gaming notation for keyboard/mouse instructions

## Search Strategy

### Primary Sources (in order)

1. **Reddit** - Recent discussions with community validation
   - Search game-specific subreddit first: `subreddit:[gamename]`
   - Use operators: `title:"stuck" OR title:"help" self:yes`
   - Sort by: top (for quality) or new (for recent patches)
   - Look for: High upvotes, "Solved" flair, multiple confirmations

2. **Steam Community** - Technical issues and developer responses
   - Search pattern: `site:steamcommunity.com/app/ [game] [issue]`
   - Check pinned discussions for common problems
   - Developer posts have green checkmarks

3. **GameFAQs** - Comprehensive walkthroughs for older games
   - Use Google: `site:gamefaqs.gamespot.com [game] [problem]`
   - Focus on message board threads with high reply counts

4. **YouTube** - Visual demonstrations (process via transcript)
   - Get transcript when video URL provided
   - Search: `[game] [problem] walkthrough tutorial`

### Quality Indicators

**Trust signals:**
- Upvote ratio > 80%
- Multiple users confirming "this worked"
- Detailed step-by-step instructions
- Recent post date (within last year for current games)
- Screenshots or video proof
- Moderator/developer verification

**Red flags:**
- Heavily downvoted
- Vague responses ("just try harder")
- Contradicts recent patch notes
- No confirmations from other users

## Video Processing

When users provide YouTube URLs or request video help:

1. **Extract transcript** - Use YouTube transcript API or web search for "[video title] transcript"
2. **Identify key moments** - Look for timestamp markers in transcript
3. **Parse instructions** - Extract control sequences and timing
4. **Cross-reference** - Search for text guides of same content for verification

See `references/video-processing.md` for detailed patterns.

## Control Notation Standards

### Keyboard Format
- Single keys: `[W]`, `[A]`, `[S]`, `[D]`, `[Space]`, `[Shift]`, `[Ctrl]`, `[E]`
- Simultaneous: `[Shift] + [W]` (hold both)
- Sequential: `[W], [Space]` (press W then Space)
- Held keys: "Hold `[Shift]` while pressing `[W]`"
- Timed: "Hold `[E]` for 2 seconds"

### Mouse Format
- `[LMB]` or `[Left Click]` - Primary action
- `[RMB]` or `[Right Click]` - Secondary/aim
- `[MMB]` or `[Middle Click]` - Tertiary
- `[Mouse Wheel Up/Down]` - Weapon switch/zoom
- `[Move Mouse Left/Right/Up/Down]` - Camera control

### Common Combinations
- Sprint: `[Shift] + [WASD]`
- Jump while moving: `[WASD] + [Space]`
- Crouch/sneak: `[Ctrl]` or `[C]`
- Interact: `[E]` or `[F]`
- Quick save: `[F5]`
- Quick load: `[F9]`

See `references/control-notation.md` for complete guide.

## Response Templates

### For "Stuck" Problems
```
I can help you get past [location/puzzle]. Here's the solution:

**Overview:** [Brief description of what needs to be done]

**Step-by-step:**
1. [First action with controls]
2. [Next action with controls]
3. [Continue numbered steps]

**Common mistakes:** [What to avoid]
**Tips:** [Easier approach if struggling]
```

### For Boss Strategies
```
[Boss name] strategy guide:

**Attack patterns:**
- [Pattern 1]: [How to recognize and counter]
- [Pattern 2]: [How to recognize and counter]

**Recommended approach:**
1. Phase 1: [Strategy with controls]
2. Phase 2: [Strategy with controls]

**Positioning:** [Where to stand/move]
**Openings:** [When to attack safely]
```

### For Technical Issues
```
This is a known issue with [game]. Here are community-verified solutions:

**Solution 1** (Most successful):
[Steps to fix]

**Solution 2** (If first doesn't work):
[Alternative steps]

**Verification:** [How to check if fixed]
**Prevention:** [How to avoid recurrence]
```

## Search Patterns

### Progression Blocks
- `[game] "stuck at" OR "can't progress" [location]`
- `[game] [chapter/level] walkthrough`
- `[game] "where to go after" [event]`

### Combat Help  
- `[game] [boss/enemy] strategy OR tips`
- `[game] "how to beat" OR "can't defeat" [boss]`
- `[game] [boss] cheese OR easy method`

### Item/Secret Finding
- `[game] "where to find" [item]`
- `[game] [item] location guide`
- `[game] secret OR hidden [area/item]`

### Technical Problems
- `[game] crash OR "won't start" [error]`
- `[game] bug OR glitch [description]`
- `[game] performance OR fps fix`

### Achievement Help
- `[game] achievement OR trophy [name]`
- `[game] 100% completion guide`
- `[game] missable achievements`

## Platform-Specific Notes

### Reddit Search Tips
- Add `after:2024` for recent posts
- Use `-mod` to exclude mod-related issues
- Check `/hot` and `/top` of game subreddit
- Crosspost searches: also check r/gaming, r/pcgaming

### Steam Forum Navigation  
- Check Pinned posts first
- Look for [SOLVED] tag in titles
- Developer posts have special highlighting
- Sort by "Most Helpful" for quality

### GameFAQs Best Practices
- Check the FAQ section before boards
- Longer threads = more troubleshooting
- Look for "sticky" topics
- Platform-specific boards may differ

## Skill Level Detection

Adjust explanation based on player language:

**Beginner indicators:**
- "I'm new to gaming"
- Asks about basic controls
- Unfamiliar with genre conventions

**Experienced indicators:**
- Uses technical terms
- References other games
- Asks about optimization

**Adapt response:**
- Beginners: Explain every control, include safety tips
- Intermediate: Focus on strategy over basics
- Advanced: Include speedrun techniques, skip obvious

## Script Utilities

- `scripts/search_forums.py` - Searches multiple forums with rate limiting
- `scripts/extract_transcript.py` - Gets YouTube video transcripts
- `scripts/format_controls.py` - Converts control descriptions to standard notation
- `scripts/quality_scorer.py` - Scores forum solutions for reliability

## Reference Documents

- `references/video-processing.md` - Detailed video analysis workflows
- `references/control-notation.md` - Complete PC control formatting guide
- `references/search-operators.md` - Advanced search syntax for all platforms
- `references/common-issues/` - Game-specific known problems and solutions

## Validation Checklist

Before presenting solution:
- [ ] Cross-referenced across 2+ sources
- [ ] Checked post date vs game version
- [ ] Controls formatted consistently  
- [ ] Instructions numbered and clear
- [ ] Included common failure points
- [ ] Mentioned easier alternatives if applicable