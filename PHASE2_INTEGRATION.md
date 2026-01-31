"""
Phase 2 Integration Guide: Smart Features for Lead and Deal Pages

This document outlines where to integrate the new AI features into existing pages.
"""

## Frontend Integration Points:

### 1. Lead.vue / Deal.vue - Score Badge Integration

Add after line 19 (after AssignTo component):
```vue
<LeadScoreBadge
  v-if="aiStore.aiEnabled && doc.ai_score !== null"
  :score="doc.ai_score"
  :loading="scoringLead"
  :showScoreButton="!doc.ai_score"
  @score-lead="handleScoreLead"
  @show-breakdown="showScoreBreakdown = true"
/>
```

Add imports at top:
```javascript
import LeadScoreBadge from '@/components/AI/LeadScoreBadge.vue'
import ScoreBreakdownModal from '@/components/AI/ScoreBreakdownModal.vue'
import { aiStore } from '@/stores/ai'
```

Add state variables:
```javascript
const scoringLead = ref(false)
const showScoreBreakdown = ref(false)
const scoreData = ref(null)
```

Add methods:
```javascript
async function handleScoreLead() {
  scoringLead.value = true
  try {
    const result = await aiStore.scoreLead(leadId)
    doc.value.ai_score = result.score
    await loadScoreBreakdown()
  } catch (error) {
    console.error('Scoring failed:', error)
  } finally {
    scoringLead.value = false
  }
}

async function loadScoreBreakdown() {
  if (doc.value.ai_score) {
    scoreData.value = await aiStore.getScoreBreakdown(leadId)
  }
}
```

Add modal at bottom of template:
```vue
<ScoreBreakdownModal
  v-model="showScoreBreakdown"
  :scoreData="scoreData"
  :loading="!scoreData"
/>
```

### 2. Activities.vue - Email Reply Suggestions

In EmailArea component section, add after email content display:
```vue
<EmailReplySuggestion
  v-if="showAIReply"
  :emailContent="aiReplyContent"
  :loading="generatingReply"
  @use-reply="useAIReply"
  @regenerate="regenerateReply"
  @close="showAIReply = false"
/>
```

Add button to trigger AI reply (after Reply button):
```vue
<Button
  v-if="aiStore.aiEnabled"
  variant="ghost"
  :label="'AI Reply'"
  @click="generateAIReply(emailMessage)"
>
  <template #prefix>
    <svg>...</svg> <!-- AI icon -->
  </template>
</Button>
```

Add state and methods:
```javascript
const showAIReply = ref(false)
const aiReplyContent = ref(null)
const generatingReply = ref(false)

async function generateAIReply(emailMessage) {
  generatingReply.value = true
  try {
    const result = await aiStore.generateEmailReply(
      emailMessage.content,
      emailMessage.sender,
      props.doctype,
      props.docname
    )
    aiReplyContent.value = result.content
    showAIReply.value = true
  } catch (error) {
    console.error('Reply generation failed:', error)
  } finally {
    generatingReply.value = false
  }
}

function useAIReply(content) {
  newEmail.value = content
  showEmailBox.value = true
  showAIReply.value = false
}

async function regenerateReply() {
  await generateAIReply(currentEmailMessage.value)
}
```

### 3. LeadsListView.vue - Score Column Integration

Add to default columns configuration:
```javascript
{
  label: 'AI Score',
  key: 'ai_score',
  width: '100px',
}
```

Add custom renderer for score column:
```vue
<template #ai_score="{ row }">
  <div v-if="row.ai_score" class="flex items-center gap-2">
    <div
      :class="[
        'flex h-8 w-12 items-center justify-center rounded-md text-xs font-semibold',
        getScoreColorClass(row.ai_score)
      ]"
    >
      {{ row.ai_score }}
    </div>
  </div>
  <span v-else class="text-xs text-ink-gray-4">-</span>
</template>
```

Add helper method:
```javascript
function getScoreColorClass(score) {
  if (score >= 80) return 'bg-green-100 text-green-700'
  if (score >= 60) return 'bg-blue-100 text-blue-700'
  if (score >= 40) return 'bg-yellow-100 text-yellow-700'
  return 'bg-red-100 text-red-700'
}
```

### 4. Backend - Ensure Jobs Run

The auto-scoring happens via hooks now. To manually trigger batch scoring:

```python
# In Frappe console or background job
from crm.ai.jobs import batch_score_leads

# Score all unscored leads
batch_score_leads()

# Score leads with specific filters
batch_score_leads(filters={"status": "New"})
```

### 5. Installation Steps

1. Run migrations to add custom fields:
```bash
bench --site [site-name] migrate
```

2. Configure AI in CRM AI Settings:
- Enable AI
- Set provider (OpenAI, Anthropic, etc.)
- Enter API key
- Select model

3. Build frontend:
```bash
cd apps/crm/frontend
yarn build
```

4. Clear cache:
```bash
bench --site [site-name] clear-cache
```

### 6. Usage Examples

**Score a Lead Manually:**
```javascript
// From Lead page
await aiStore.scoreLead('LEAD-001')
```

**View Score Breakdown:**
```javascript
const breakdown = await aiStore.getScoreBreakdown('LEAD-001')
console.log(breakdown.factors) // Individual score factors
console.log(breakdown.recommendations) // AI recommendations
```

**Generate Email Reply:**
```javascript
const reply = await aiStore.generateEmailReply(
  emailContent,
  'John Doe',
  'CRM Lead',
  'LEAD-001',
  'professional'
)
```

**Compose New Email:**
```javascript
const email = await aiStore.composeEmail({
  recipient_name: 'Jane Smith',
  company: 'Acme Corp',
  purpose: 'Follow-up on demo',
  tone: 'friendly',
  reference_doctype: 'CRM Deal',
  reference_name: 'DEAL-001'
})
```

### 7. Troubleshooting

**Scores not appearing:**
- Check if AI is enabled in CRM AI Settings
- Verify API key is correct
- Check browser console for errors
- Check Frappe error logs

**Background jobs not running:**
- Ensure Redis is running
- Check queue status: `bench --site [site-name] doctor`
- Check worker logs

**API rate limits:**
- Consider using GPT-4o-mini instead of GPT-4o
- Implement caching for frequently accessed data
- Use batch operations when possible

