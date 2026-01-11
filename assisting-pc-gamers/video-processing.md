# Video Processing Guide for Gaming Help

## Overview

Since Claude cannot directly process video files, we use transcript-based analysis combined with contextual search to understand video game tutorials and walkthroughs.

## Primary Method: YouTube Transcript Extraction

### When User Provides YouTube URL

1. **Extract Video ID**
   - From URL: `youtube.com/watch?v=VIDEO_ID` or `youtu.be/VIDEO_ID`
   - Clean any additional parameters

2. **Get Transcript**
   - Search for: "[video title] transcript" if direct API unavailable
   - YouTube often auto-generates captions available via search
   - Look for timestamps in transcript: `[0:23]`, `(1:45)`, or `@ 2:30`

3. **Parse Key Sections**
   ```
   Example transcript analysis:
   [0:00-0:30] - Introduction/problem setup
   [0:30-2:00] - Preparation/equipment needed  
   [2:00-5:00] - Main strategy explanation
   [5:00-end] - Execution and tips
   ```

### When User Describes Video

1. **Search for Video**
   - Query: `[game] [problem description] video walkthrough`
   - Look for videos with transcripts available
   - Prefer videos with high view counts and good like ratios

2. **Find Text Companions**
   - Search: `[video creator] [game] written guide`
   - Many YouTubers post text versions
   - IGN, GameSpot often have both video and text

## Transcript Analysis Patterns

### Identifying Key Moments

**Control Instructions**
Look for phrases indicating controls:
- "Press [button]"
- "Hold down"
- "Click on"
- "Jump at"
- "When you see"

**Timing Cues**
Critical timing information:
- "Wait for"
- "As soon as"
- "Right when"
- "After the"
- "Count to"

**Spatial Directions**
Movement instructions:
- "Go to the left"
- "Behind the"
- "Jump across"
- "Turn around"
- "Face the"

### Common Video Tutorial Structures

**Speedrun Videos**
- Quick execution, minimal explanation
- Extract: Route, glitch usage, frame-perfect timing
- Cross-reference with speedrun wikis

**Casual Walkthroughs**
- Detailed explanation, multiple attempts shown
- Extract: Strategy options, common mistakes, tips
- Good for beginners

**Boss Fight Guides**
- Pattern recognition focus
- Extract: Attack telegraphs, dodge timing, damage windows
- Note equipment recommendations

**100% Completion**
- Comprehensive coverage
- Extract: Missable items, point of no return warnings
- Timeline-critical information

## Timestamp Navigation

### Standard Formats
```
[MM:SS] - Common in transcripts
Chapter: X (MM:SS) - YouTube chapters
@MM:SS - Social media style
Part 3 starts at MM:SS - Natural language
```

### Using Timestamps in Responses
```
"According to the walkthrough:
- At [2:30] - Position yourself behind the pillar
- At [2:45] - Wait for the laser sweep
- At [3:00] - Sprint using [Shift] + [W] to the switch"
```

## Alternative Video Sources

### Twitch Clips
- Search: `site:clips.twitch.tv [game] [achievement/boss]`
- Usually short, specific solutions
- Check clip title for context

### Reddit Video Posts
- Search: `site:reddit.com/r/[game] url:v.redd.it`
- Often includes text explanation in comments
- Community validates in replies

### Steam Community Videos
- Found in Steam Guides section
- Often paired with written guides
- Check comments for corrections

## Cross-Reference Strategies

### Verify Video Content
Always cross-check video information with:
1. Written guides for same content
2. Multiple videos showing same strategy
3. Recent patch notes (strategies may be outdated)
4. Community feedback on the video

### Common Discrepancies
- **Version differences**: Video from older game version
- **Platform differences**: PC vs console controls
- **Difficulty settings**: Strategy may be difficulty-specific
- **Mod usage**: Video might use mods not mentioned

## Transcript Quality Issues

### Auto-Generated Captions
Problems to watch for:
- Game terms misheard ("Souls" → "Soles")
- Character names wrong
- Button callouts unclear
- Numbers confused (15 vs 50)

Mitigation:
- Cross-reference with written guides
- Use context to correct obvious errors
- Search for community-corrected transcripts

### Missing Information
When transcript lacks detail:
- Search for: "[YouTuber name] [video title] breakdown"
- Check video comments for timestamps
- Find reaction/analysis videos

## Response Format for Video-Based Help

```markdown
Based on the [video title] walkthrough by [creator]:

**Setup** (0:00-1:00)
- [Preparation steps from video]

**Execution** (1:00-5:00)
1. [Step with timestamp]: [Instruction with controls]
2. [Step with timestamp]: [Instruction with controls]

**Key moment** (3:45): [Critical timing/positioning]

**Common mistakes shown**:
- [What the video showed going wrong]

**Alternative approach** (if mentioned):
- [Other strategy from video]

Note: Video is from [date], verify for current patch.
```

## Special Considerations

### Spoiler Sensitivity
- Warn if video solution contains story spoilers
- Offer spoiler-free alternative if available
- Mark spoiler sections clearly

### Accessibility
- Note if strategy requires quick reflexes
- Mention easier alternatives from video
- Include accessibility options if discussed

### Equipment Dependencies
- List required items/level from video
- Note if strategy needs specific build
- Mention alternatives for different loadouts

## Quick Reference Patterns

**Get any YouTube transcript:**
Search: "[exact video title]" transcript OR captions

**Find video for specific problem:**
Search: [game] [problem] video tutorial walkthrough

**Verify video currency:**
Search: [game] [strategy from video] "after patch" OR "still works"

**Find text version of video:**
Search: [creator] [game] [topic] written guide OR text

**Check if strategy patched:**
Search: [game] [exploit/strategy] patched OR nerfed [current year]