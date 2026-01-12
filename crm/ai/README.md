# CRM AI Module

AI-powered features for Frappe CRM including chat assistant, email composition, lead scoring, and deal analysis.

## 🚀 Features

### Core AI Capabilities
- **AI Chat Assistant**: Natural language queries about leads, deals, and contacts
- **Email Composer**: AI-powered email generation with tone customization
- **Lead Scoring**: Automatic lead qualification and quality assessment
- **Deal Analysis**: Win probability prediction and strategic recommendations
- **Activity Summarization**: Automatic summary of communications and tasks
- **Sentiment Analysis**: Analyze communication sentiment for better engagement

## 📦 Installation

1. **Install Python dependencies**:
```bash
bench --site your-site.local pip install -r apps/crm/pyproject.toml
```

2. **Migrate database** to create new DocTypes:
```bash
bench --site your-site.local migrate
```

3. **Build frontend**:
```bash
cd apps/crm/frontend && yarn install && yarn build
```

## ⚙️ Configuration

1. Navigate to **CRM AI Settings** in your CRM
2. Enable AI features
3. Choose your AI provider:
   - **OpenAI** (GPT-4o, GPT-4o-mini) - Recommended for production
   - **Anthropic** (Claude 3.5 Sonnet) - Great for long context
   - **Ollama** (Llama 3.1, etc.) - Free local deployment
   - **LiteLLM** - Multi-provider support

4. Enter your API key (not needed for Ollama)
5. Configure model settings:
   - **Model**: Choose the specific model (e.g., gpt-4o-mini, claude-3-5-sonnet-20240620)
   - **Temperature**: 0.0-1.0 (lower = more deterministic, higher = more creative)
   - **Max Tokens**: Maximum response length

## 🎯 Usage

### AI Chat Assistant

```javascript
// In Vue component
import { useAIStore } from '@/stores/ai'

const aiStore = useAIStore()

// Send a message
const response = await aiStore.sendMessage(
  "What deals are closing this month?",
  "CRM Deal",
  "DEAL-2024-001"
)
```

### Email Composition

```javascript
// Open email composer
<EmailComposer
  v-model="showComposer"
  reference-doctype="CRM Lead"
  reference-name="LEAD-2024-001"
  @email-generated="handleEmail"
/>
```

### Lead Scoring

```javascript
// Score a lead
const analysis = await aiStore.scoreLead("LEAD-2024-001")
```

### Deal Analysis

```javascript
// Analyze a deal
const insights = await aiStore.analyzeDeal("DEAL-2024-001")
```

## 🏗️ Architecture

```
crm/
├── ai/                          # Backend AI service layer
│   ├── ai_service.py           # Main orchestrator
│   ├── providers.py            # LLM provider implementations
│   ├── prompts.py              # Prompt templates
│   └── utils.py                # Helper functions
├── api/
│   └── ai.py                   # API endpoints
├── fcrm/doctype/
│   ├── crm_ai_settings/        # Configuration DocType
│   ├── crm_ai_conversation/    # Chat history storage
│   └── crm_ai_suggestion/      # AI suggestions storage
frontend/
├── src/
│   ├── components/AI/
│   │   ├── AIChat.vue          # Chat interface
│   │   ├── AISuggestions.vue   # Suggestions display
│   │   └── EmailComposer.vue   # Email generation UI
│   └── stores/
│       └── ai.js               # Pinia state management
```

## 🔌 API Reference

### Backend API Endpoints

All endpoints are prefixed with `crm.api.ai.*`

#### `chat(message, reference_doctype, reference_name)`
General chat with AI assistant.

**Parameters:**
- `message` (str): User's question or request
- `reference_doctype` (str, optional): Context doctype (CRM Lead, CRM Deal)
- `reference_name` (str, optional): Document name for context

**Returns:** `{type: "text", content: "...", timestamp: "..."}`

#### `compose_email(recipient_name, company, purpose, tone, reference_doctype, reference_name)`
AI-powered email composition.

**Parameters:**
- `recipient_name` (str): Email recipient
- `company` (str): Company name
- `purpose` (str): Email purpose/goal
- `tone` (str): professional | friendly | urgent | casual | formal
- `reference_doctype` (str, optional): Context doctype
- `reference_name` (str, optional): Document name

**Returns:** `{type: "email", content: "...", timestamp: "..."}`

#### `score_lead(lead_name)`
Analyze and score a lead.

**Parameters:**
- `lead_name` (str): CRM Lead document name

**Returns:** Analysis with quality rating, score, and recommendations

#### `analyze_deal(deal_name)`
Analyze deal and predict win probability.

**Parameters:**
- `deal_name` (str): CRM Deal document name

**Returns:** Analysis with win probability, risks, and next steps

#### `summarize_activities(reference_doctype, reference_name, limit)`
Summarize recent activities.

**Parameters:**
- `reference_doctype` (str): CRM Lead | CRM Deal
- `reference_name` (str): Document name
- `limit` (int): Number of activities to summarize (default: 10)

**Returns:** Concise summary with key points and action items

#### `analyze_sentiment(text, reference_doctype, reference_name)`
Analyze sentiment of communication.

**Parameters:**
- `text` (str): Text to analyze
- `reference_doctype` (str, optional): Context doctype
- `reference_name` (str, optional): Document name

**Returns:** Sentiment analysis with score and recommendations

## 💡 Best Practices

### Cost Optimization
1. **Use appropriate models**: GPT-4o-mini for simple tasks, GPT-4o for complex analysis
2. **Cache results**: Leverage conversation history to avoid redundant calls
3. **Batch operations**: Process multiple items together when possible
4. **Set reasonable max_tokens**: Limit response length based on needs

### Performance
1. **Async operations**: AI calls should be non-blocking
2. **Background jobs**: Use Celery for batch processing (future implementation)
3. **Progressive disclosure**: Load AI features on-demand, not by default

### Security
1. **API key protection**: Store in Password field, never expose to frontend
2. **Rate limiting**: Implement per-user limits to prevent abuse
3. **Data privacy**: Be mindful of what context is sent to external APIs
4. **User permissions**: Respect CRM permissions when accessing data

## 🔮 Future Enhancements (Roadmap)

### Phase 2 Features
- [ ] Real-time call transcription and analysis
- [ ] Automated lead enrichment from web sources
- [ ] Smart notification prioritization
- [ ] Meeting preparation briefs

### Phase 3 Features
- [ ] Revenue forecasting with Prophet
- [ ] Churn prediction models
- [ ] A/B testing for email templates
- [ ] Voice-to-text for notes

### Phase 4 Features
- [ ] Custom model fine-tuning on your data
- [ ] Semantic search across all CRM data
- [ ] WhatsApp AI auto-responder
- [ ] Integration with ERPNext for full pipeline

## 🐛 Troubleshooting

### AI features not working
1. Check if AI is enabled in CRM AI Settings
2. Verify API key is correctly set
3. Check browser console for errors
4. Review backend logs: `bench --site your-site.local console`

### "AI is not enabled" error
- Navigate to CRM AI Settings and enable the checkbox
- Save the settings
- Reload your browser

### OpenAI API errors
- Verify API key is valid
- Check OpenAI account has sufficient credits
- Ensure network connectivity to api.openai.com

### Slow response times
- Consider using a faster model (gpt-4o-mini vs gpt-4o)
- Reduce max_tokens setting
- Check network latency to API provider

## 📊 Monitoring

View AI usage and costs in the backend:
```python
# In Frappe console
frappe.get_all('Error Log', filters={'title': ('like', '%AI Usage%')}, limit=20)
```

## 🤝 Contributing

1. Backend changes: Update files in `crm/ai/` and `crm/api/ai.py`
2. Frontend changes: Update components in `frontend/src/components/AI/`
3. New features: Add to both backend API and frontend store
4. DocTypes: Create new doctypes as needed for data persistence

## 📝 License

Same as Frappe CRM - GPL v3.0
