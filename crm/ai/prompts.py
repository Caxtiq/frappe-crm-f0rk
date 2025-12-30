"""Prompt templates for various AI tasks"""

# System prompts
SYSTEM_PROMPTS = {
	"email_composer": """You are an expert sales email writer. Write professional, engaging emails that:
- Are concise and to the point
- Have a clear call-to-action
- Match the specified tone
- Are personalized based on the context provided
- Follow email best practices""",
	
	"lead_scorer": """You are a lead qualification expert. Analyze the provided lead information and:
- Assess the lead quality (Hot, Warm, Cold)
- Provide a score from 0-100
- Explain your reasoning
- Suggest next best actions""",
	
	"deal_analyzer": """You are a sales strategy expert. Analyze deal information and:
- Estimate win probability
- Identify risks and opportunities
- Suggest next steps
- Provide strategic recommendations""",
	
	"activity_summarizer": """You are an expert at analyzing sales activities. Summarize the provided information:
- Extract key points and insights
- Identify action items
- Note important dates and commitments
- Highlight concerns or red flags""",
	
	"sentiment_analyzer": """You are a sentiment analysis expert. Analyze the text and:
- Determine overall sentiment (Positive, Neutral, Negative)
- Provide a confidence score
- Identify specific emotional indicators
- Suggest appropriate response tone""",
	
	"assistant": """You are a helpful CRM assistant. Help users with:
- Answering questions about their leads, deals, and contacts
- Performing quick actions
- Finding information
- Providing insights and recommendations
Be concise, accurate, and helpful.""",
}


# Prompt templates
def email_composer_prompt(
	recipient_name: str,
	company: str,
	purpose: str,
	tone: str = "professional",
	context: dict = None,
) -> str:
	"""Generate email composition prompt"""
	prompt = f"""Write a {tone} email to {recipient_name} at {company}.

Purpose: {purpose}"""
	
	if context:
		prompt += f"\n\nContext:\n"
		for key, value in context.items():
			prompt += f"- {key}: {value}\n"
	
	prompt += "\n\nWrite the email subject and body."
	return prompt


def lead_scoring_prompt(lead_data: dict) -> str:
	"""Generate lead scoring prompt"""
	prompt = "Analyze this lead and provide a quality score:\n\n"
	
	for key, value in lead_data.items():
		prompt += f"{key}: {value}\n"
	
	prompt += """\nProvide:
1. Quality rating (Hot/Warm/Cold)
2. Score (0-100)
3. Reasoning
4. Next best action"""
	
	return prompt


def deal_analysis_prompt(deal_data: dict) -> str:
	"""Generate deal analysis prompt"""
	prompt = "Analyze this sales deal:\n\n"
	
	for key, value in deal_data.items():
		prompt += f"{key}: {value}\n"
	
	prompt += """\nProvide:
1. Win probability (%)
2. Key risks
3. Opportunities
4. Recommended next steps
5. Suggested close date"""
	
	return prompt


def activity_summary_prompt(activities: list) -> str:
	"""Generate activity summary prompt"""
	prompt = "Summarize these recent activities:\n\n"
	
	for i, activity in enumerate(activities, 1):
		prompt += f"{i}. {activity.get('type', 'Activity')}: {activity.get('description', '')}\n"
		if activity.get('date'):
			prompt += f"   Date: {activity['date']}\n"
	
	prompt += "\nProvide a concise summary highlighting key points and action items."
	return prompt


def sentiment_analysis_prompt(text: str) -> str:
	"""Generate sentiment analysis prompt"""
	return f"""Analyze the sentiment of this communication:

"{text}"

Provide:
1. Overall sentiment (Positive/Neutral/Negative)
2. Confidence score (0-100)
3. Key emotional indicators
4. Recommended response tone"""


def chat_assistant_prompt(query: str, context: dict = None) -> str:
	"""Generate chat assistant prompt"""
	prompt = query
	
	if context:
		prompt = f"Context:\n"
		for key, value in context.items():
			prompt += f"{key}: {value}\n"
		prompt += f"\nUser question: {query}"
	
	return prompt
