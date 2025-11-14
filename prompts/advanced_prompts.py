"""
Advanced prompts for different content types and styles
"""

# For technical/detailed sections
TECHNICAL_SECTION_PROMPT = """
Write detailed technical content for this section. Focus on specifics, implementations, and practical details.

Main Topic: "{main_question}"
Section Focus: "{section_heading}"
Target Length: {target_words} words

Requirements:
- Start directly with technical details
- No section titles, headings, or introductions
- No "In this section..." or "Let me explain..." phrases
- Focus purely on technical implementation and specifics
- Be comprehensive but concise

Content:
"""

# For conceptual/explanatory sections  
CONCEPTUAL_SECTION_PROMPT = """
Explain the key concepts and principles for this section. Focus on understanding and clarity.

Main Topic: "{main_question}"
Section Focus: "{section_heading}"  
Target Length: {target_words} words

Requirements:
- Start directly with conceptual explanations
- No section titles, headings, or introductions
- No "In this section..." or "Let me explain..." phrases
- Focus purely on concepts and principles
- Make complex ideas clear and understandable

Content:
"""

# For practical/implementation sections
PRACTICAL_SECTION_PROMPT = """
Provide practical guidance and actionable information for this section.

Main Topic: "{main_question}"
Section Focus: "{section_heading}"
Target Length: {target_words} words

Requirements:
- Start directly with practical guidance
- No section titles, headings, or introductions
- No "In this section..." or "Here's how..." phrases
- Focus purely on actionable information and best practices
- Provide concrete steps and recommendations

Content:
"""

# Dynamic prompt selector based on section type
SECTION_TYPE_KEYWORDS = {
    "technical": ["implementation", "architecture", "system", "technology", "technical", "infrastructure", "code", "development"],
    "conceptual": ["principles", "concepts", "theory", "understanding", "fundamentals", "overview", "introduction"],
    "practical": ["practices", "steps", "guide", "how to", "process", "workflow", "best practices", "challenges"]
}

def get_section_prompt(section_heading: str, question: str, target_words: int) -> str:
    """
    Select the most appropriate prompt based on section content
    """
    section_lower = section_heading.lower()
    
    # Check for technical keywords
    if any(keyword in section_lower for keyword in SECTION_TYPE_KEYWORDS["technical"]):
        return TECHNICAL_SECTION_PROMPT.format(
            main_question=question,
            section_heading=section_heading,
            target_words=target_words
        )
    
    # Check for practical keywords
    elif any(keyword in section_lower for keyword in SECTION_TYPE_KEYWORDS["practical"]):
        return PRACTICAL_SECTION_PROMPT.format(
            main_question=question,
            section_heading=section_heading,
            target_words=target_words
        )
    
    # Default to conceptual
    else:
        return CONCEPTUAL_SECTION_PROMPT.format(
            main_question=question,
            section_heading=section_heading,
            target_words=target_words
        )