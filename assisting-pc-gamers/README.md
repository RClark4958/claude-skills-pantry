# PC Gaming Help Expert Skill

A comprehensive Claude skill for helping PC gamers overcome obstacles through community-sourced solutions, video analysis, and clear control instructions.

## Features

- 🔍 **Multi-platform Forum Search**: Searches Reddit, Steam, GameFAQs for validated community solutions
- 📺 **Video Tutorial Analysis**: Processes YouTube transcripts to extract strategies and control sequences
- 🎮 **Standard Control Notation**: Formats all instructions with proper PC gaming notation (`[WASD]`, `[Shift]`, `[LMB]`, etc.)
- ⭐ **Quality Scoring**: Evaluates solutions based on community validation, author credibility, and content quality
- 📚 **Game-Specific Knowledge**: Includes common issues and solutions for popular games
- 🎯 **Smart Problem Detection**: Identifies whether player needs puzzle help, boss strategies, technical fixes, or control guidance

## Installation

1. Download the skill package
2. In Claude.ai, Claude Code, or via API:
   - Add the skill to your skills directory
   - The skill will auto-trigger on gaming-related queries

## Usage Examples

### Basic Help Request
```
"I'm stuck in Portal 2, chamber 15"
```
Claude will search for community solutions and provide step-by-step instructions.

### Boss Strategy
```
"How do I beat Malenia in Elden Ring?"
```
Returns top strategies from Reddit/Steam with quality scores and control notation.

### Video Tutorial Analysis
```
"Can you explain this speedrun technique? [YouTube URL]"
```
Extracts transcript, identifies key moments, and formats control sequences.

### Technical Issues
```
"Cyberpunk 2077 keeps crashing on startup"
```
Searches recent threads for verified fixes across multiple platforms.

## Skill Structure

```
pc-gaming-help/
├── SKILL.md                    # Main skill file with workflows
├── README.md                    # This file
├── scripts/
│   ├── search_forums.py       # Multi-platform forum searcher
│   ├── extract_transcript.py  # YouTube transcript processor
│   ├── format_controls.py     # Control notation formatter
│   └── quality_scorer.py      # Solution quality evaluator
└── references/
    ├── video-processing.md     # Video analysis guide
    ├── control-notation.md     # Complete control formatting
    ├── search-operators.md     # Advanced search syntax
    └── common-issues/
        ├── elden-ring.md       # Game-specific issues
        └── baldurs-gate-3.md   # Game-specific issues
```

## Key Components

### Forum Search Strategy
1. **Reddit First**: Recent discussions with community validation
2. **Steam Second**: Technical issues and developer responses  
3. **GameFAQs Third**: Comprehensive guides for older games
4. **YouTube Transcripts**: Visual demonstrations when needed

### Quality Scoring Factors
- **Author Credibility** (20%): Reputation, post count, badges
- **Community Validation** (25%): Upvotes, confirmations, replies
- **Content Quality** (20%): Structure, visual aids, detail level
- **Official Endorsement** (15%): Developer/moderator confirmation
- **Recency** (10%): How current the solution is
- **Detail Level** (10%): Comprehensiveness of explanation

### Control Notation Standards

| Action | Notation | Example |
|--------|----------|---------|
| Single Key | `[Key]` | `[W]`, `[Space]`, `[E]` |
| Simultaneous | `+` | `[Shift] + [W]` (sprint) |
| Sequential | `,` | `[W], [Space]` (move then jump) |
| Hold | "Hold" | "Hold `[E]` for 2 seconds" |
| Mouse | `[LMB/RMB]` | `[LMB]` (shoot), `[RMB]` (aim) |

## Response Templates

### Stuck/Progression Problems
```
Overview → Step-by-step solution → Common mistakes → Tips for struggling
```

### Boss Strategies  
```
Attack patterns → Positioning → Timing windows → Equipment recommendations
```

### Technical Issues
```
Verified solutions (ranked) → Troubleshooting steps → Prevention tips
```

## Advanced Features

### Video Processing Pipeline
1. Extract video ID from URL
2. Retrieve transcript via API/search
3. Identify key moments (controls, timing, strategy)
4. Parse control sequences
5. Format with timestamps

### Search Optimization
- Uses platform-specific operators
- Filters by date for patch-relevant info
- Cross-references multiple sources
- Prioritizes solved/verified posts

### Skill Level Adaptation
- **Beginners**: Detailed control explanations, safety tips
- **Intermediate**: Focus on strategy, assume basic knowledge
- **Advanced**: Include speedrun tech, optimization tips

## Best Practices

### When to Trigger
- "stuck in [game]"
- "can't beat [boss]"
- "how do I [action]"
- "[game] won't work"
- "help with [puzzle]"
- Video URLs with gaming content

### Quality Validation
- Always cross-reference 2+ sources
- Check post dates vs game patches
- Verify control notation consistency
- Include common failure points

## Customization

### Adding Game-Specific Knowledge
Create new files in `references/common-issues/` following the template:
```markdown
# [Game Name] - Common Issues & Solutions

## Technical Issues
[Common technical problems and fixes]

## Progression Blocks
[Where players commonly get stuck]

## Boss Strategies
[Quick tips for difficult bosses]
```

### Updating Search Patterns
Edit `references/search-operators.md` to add new search patterns for specific scenarios.

### Adjusting Quality Weights
Modify `WEIGHTS` dictionary in `scripts/quality_scorer.py` to prioritize different factors.

## Performance Considerations

- **Rate Limiting**: Respects platform API limits
- **Caching**: Solutions cached for 24-48 hours
- **Efficiency**: Searches stop after finding high-quality solutions
- **Fallbacks**: Multiple search strategies if primary fails

## Limitations

- Cannot directly watch videos (uses transcripts instead)
- Requires recent community activity for best results
- Platform-specific solutions may not apply to all versions
- Some solutions may be outdated despite high scores

## Support

This skill is designed to be self-improving through user interaction. Claude learns which solutions work best through conversation feedback.

## License

This skill is provided as-is for helping gamers overcome challenges. Respect platform ToS when searching forums.

---

**Version**: 1.0.0  
**Last Updated**: November 2024  
**Compatible With**: Claude.ai, Claude Code, Claude API