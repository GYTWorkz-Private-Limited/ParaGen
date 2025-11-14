"""
Prompts for section identification and generation
"""

SECTION_IDENTIFICATION_PROMPT = """
Analyze the following question and break it down into logical sections that would make up a comprehensive answer.

Question: "{question}"

Return your response as CSV format with exactly 2 columns: section heading and estimated word count.

Guidelines:
- Create 3-6 sections for a comprehensive answer
- Each section should be substantial (100-300 words)
- Sections should be logically ordered
- Headings should be descriptive and specific
- Word counts should be realistic estimates

Return only the CSV data with NO headers, NO explanations, NO other text:
"""

SECTION_CONTENT_FOCUSED_PROMPT = """
Write content for this specific section. Be direct and focused - do not include introductory phrases or section headings in your response.

Main Question: "{main_question}"
Section Focus: "{section_heading}"
Target Length: {target_words} words

Requirements:
- Write ONLY the content for this section
- Start directly with the main points
- No "In this section..." or "Let me explain..." introductions
- No section titles or headings
- Be comprehensive but concise
- Focus purely on the section topic

Content:
"""

SEQUENTIAL_GENERATION_PROMPT = """
Provide a comprehensive and detailed answer to the following question. Write a well-structured, informative response that thoroughly addresses all aspects of the question.

Question: "{question}"

Instructions:
- Provide a complete, detailed answer
- Use clear structure and organization
- Include relevant examples and explanations
- Write in a professional, informative style
- Make the response comprehensive and valuable

Your response:
"""