import { defineStore } from 'pinia'
import { createResource } from 'frappe-ui'
import { ref, computed } from 'vue'

export const useAIStore = defineStore('ai', () => {
  // State
  const settings = ref(null)
  const isEnabled = ref(false)
  const conversations = ref({})
  const suggestions = ref({})
  const loading = ref(false)

  // Load AI settings
  const settingsResource = createResource({
    url: 'frappe.client.get_single',
    params: {
      doctype: 'CRM AI Settings',
    },
    auto: true,
    onSuccess(data) {
      settings.value = data
      isEnabled.value = data.enabled || false
    },
  })

  // Getters
  const aiEnabled = computed(() => isEnabled.value)
  const aiProvider = computed(() => settings.value?.provider || 'openai')
  const aiModel = computed(() => settings.value?.model || 'gpt-4o-mini')

  // Actions
  const sendMessage = async (message, referenceDoctype, referenceName) => {
    if (!isEnabled.value) {
      throw new Error('AI is not enabled')
    }

    const resource = createResource({
      url: 'crm.api.ai.chat',
      params: {
        message,
        reference_doctype: referenceDoctype,
        reference_name: referenceName,
      },
    })

    const response = await resource.submit()
    
    // Update local conversations cache
    const key = `${referenceDoctype}:${referenceName}`
    if (!conversations.value[key]) {
      conversations.value[key] = []
    }
    conversations.value[key].push({
      user_message: message,
      ai_response: response.content,
      timestamp: response.timestamp,
    })

    return response
  }

  const composeEmail = async (params) => {
    if (!isEnabled.value) {
      throw new Error('AI is not enabled')
    }

    const resource = createResource({
      url: 'crm.api.ai.compose_email',
      params,
    })

    return await resource.submit()
  }

  const scoreLead = async (leadName) => {
    if (!isEnabled.value) {
      throw new Error('AI is not enabled')
    }

    const resource = createResource({
      url: 'crm.api.ai.score_lead',
      params: { lead_name: leadName },
    })

    const response = await resource.submit()
    
    // Update suggestions cache
    const key = `CRM Lead:${leadName}`
    if (!suggestions.value[key]) {
      suggestions.value[key] = []
    }
    suggestions.value[key].unshift(response)

    return response
  }

  const analyzeDeal = async (dealName) => {
    if (!isEnabled.value) {
      throw new Error('AI is not enabled')
    }

    const resource = createResource({
      url: 'crm.api.ai.analyze_deal',
      params: { deal_name: dealName },
    })

    const response = await resource.submit()
    
    // Update suggestions cache
    const key = `CRM Deal:${dealName}`
    if (!suggestions.value[key]) {
      suggestions.value[key] = []
    }
    suggestions.value[key].unshift(response)

    return response
  }

  const summarizeActivities = async (referenceDoctype, referenceName) => {
    if (!isEnabled.value) {
      throw new Error('AI is not enabled')
    }

    const resource = createResource({
      url: 'crm.api.ai.summarize_activities',
      params: {
        reference_doctype: referenceDoctype,
        reference_name: referenceName,
      },
    })

    return await resource.submit()
  }

  const analyzeSentiment = async (text, referenceDoctype, referenceName) => {
    if (!isEnabled.value) {
      throw new Error('AI is not enabled')
    }

    const resource = createResource({
      url: 'crm.api.ai.analyze_sentiment',
      params: {
        text,
        reference_doctype: referenceDoctype,
        reference_name: referenceName,
      },
    })

    return await resource.submit()
  }

  const getConversationHistory = async (referenceDoctype, referenceName, limit = 20) => {
    const resource = createResource({
      url: 'crm.api.ai.get_conversation_history',
      params: {
        reference_doctype: referenceDoctype,
        reference_name: referenceName,
        limit,
      },
    })

    const data = await resource.submit()
    
    // Cache the conversations
    const key = `${referenceDoctype}:${referenceName}`
    conversations.value[key] = data

    return data
  }

  const getSuggestions = async (referenceDoctype, referenceName, suggestionType = null) => {
    const resource = createResource({
      url: 'crm.api.ai.get_suggestions',
      params: {
        reference_doctype: referenceDoctype,
        reference_name: referenceName,
        suggestion_type: suggestionType,
      },
    })

    const data = await resource.submit()
    
    // Cache the suggestions
    const key = `${referenceDoctype}:${referenceName}`
    suggestions.value[key] = data

    return data
  }

  const acceptSuggestion = async (suggestionName) => {
    const resource = createResource({
      url: 'crm.api.ai.accept_suggestion',
      params: { suggestion_name: suggestionName },
    })

    return await resource.submit()
  }

  const rejectSuggestion = async (suggestionName, reason = null) => {
    const resource = createResource({
      url: 'crm.api.ai.reject_suggestion',
      params: {
        suggestion_name: suggestionName,
        reason,
      },
    })

    return await resource.submit()
  }

  const updateSettings = async (newSettings) => {
    const resource = createResource({
      url: 'frappe.client.set_value',
      params: {
        doctype: 'CRM AI Settings',
        name: 'CRM AI Settings',
        fieldname: newSettings,
      },
    })

    const response = await resource.submit()
    settings.value = { ...settings.value, ...newSettings }
    isEnabled.value = newSettings.enabled ?? isEnabled.value
    
    return response
  }

  const reloadSettings = () => {
    settingsResource.reload()
  }

  // Clear cache for a specific reference
  const clearCache = (referenceDoctype, referenceName) => {
    const key = `${referenceDoctype}:${referenceName}`
    delete conversations.value[key]
    delete suggestions.value[key]
  }

  return {
    // State
    settings,
    isEnabled,
    conversations,
    suggestions,
    loading,
    
    // Getters
    aiEnabled,
    aiProvider,
    aiModel,
    
    // Actions
    sendMessage,
    composeEmail,
    scoreLead,
    analyzeDeal,
    summarizeActivities,
    analyzeSentiment,
    getConversationHistory,
    getSuggestions,
    acceptSuggestion,
    rejectSuggestion,
    updateSettings,
    reloadSettings,
    clearCache,
  }
})
