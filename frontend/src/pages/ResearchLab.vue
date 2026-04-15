<template>
  <div class="research-shell px-3 pb-3 sm:px-5 sm:pb-5">
    <LayoutHeader>
      <template #left-header>
        <ViewBreadcrumbs routeName="Research Lab" />
      </template>
    </LayoutHeader>

    <div class="mt-3 grid gap-4 lg:grid-cols-2">
      <section class="research-card rounded-2xl p-4">
        <h2 class="text-lg font-semibold text-[var(--crm-text)]">1. Causal Next-Best-Action</h2>
        <p class="mt-1 text-sm text-[var(--crm-text-soft)]">
          Estimate which action is likely to create the highest incremental conversion uplift.
        </p>

        <div class="mt-4 grid gap-3 sm:grid-cols-2">
          <label class="field">
            <span>Reference DocType (optional)</span>
            <select v-model="causal.referenceDoctype" class="field-input">
              <option value="">None</option>
              <option value="CRM Lead">CRM Lead</option>
              <option value="CRM Deal">CRM Deal</option>
            </select>
          </label>
          <label class="field" v-if="causal.referenceDoctype === 'CRM Lead'">
            <span>Select Lead</span>
            <select v-model="causal.referenceName" class="field-input text-ellipsis">
              <option value="">-- Choose Lead --</option>
              <option v-for="lead in leadsList.data" :key="lead.name" :value="lead.name">
                {{ lead.lead_name || lead.name }}
              </option>
            </select>
          </label>
          <label class="field" v-else-if="causal.referenceDoctype === 'CRM Deal'">
            <span>Select Deal</span>
            <select v-model="causal.referenceName" class="field-input text-ellipsis">
              <option value="">-- Choose Deal --</option>
              <option v-for="deal in dealsList.data" :key="deal.name" :value="deal.name">
                {{ deal.deal_name || deal.organization || deal.name }}
              </option>
            </select>
          </label>
          <label class="field" v-else>
            <span>Reference Name</span>
            <input v-model="causal.referenceName" class="field-input" placeholder="Select a DocType first..." disabled />
          </label>
          <label class="field">
            <span>Lead Intent Score</span>
            <input v-model.number="causal.intent" type="range" min="0" max="100" />
            <strong>{{ causal.intent }}</strong>
          </label>
          <label class="field">
            <span>Response Delay (hours)</span>
            <input v-model.number="causal.delay" type="range" min="0" max="72" />
            <strong>{{ causal.delay }}</strong>
          </label>
        </div>

        <div class="mt-3 flex flex-wrap gap-2">
          <Button :label="__('Run Recommendation')" @click="runNextBestAction" />
          <Button :label="__('Log Positive Outcome')" @click="logOutcome(true)" />
          <Button :label="__('Log Negative Outcome')" @click="logOutcome(false)" />
        </div>

        <div class="mt-3 grid gap-3 sm:grid-cols-2">
          <label class="field">
            <span>Observed Outcome</span>
            <input v-model="outcome.observedOutcome" class="field-input" placeholder="Meeting booked, no-response, won" />
          </label>
          <label class="field">
            <span>Conversion Delta (%)</span>
            <input v-model.number="outcome.conversionDelta" type="number" class="field-input" />
          </label>
        </div>

        <div class="result-box mt-4">
          <p class="text-sm text-[var(--crm-text-soft)]">Recommended Action</p>
          <p class="text-base font-semibold">{{ causalResult.recommended_action }}</p>
          <p class="text-sm text-[var(--crm-text-soft)] mt-1">
            Expected uplift: <strong>{{ causalResult.expected_uplift }}%</strong>
          </p>
          <p class="text-xs text-[var(--crm-text-soft)] mt-1">Run ID: {{ causalResult.run_name || 'N/A' }}</p>
        </div>
      </section>

      <section class="research-card rounded-2xl p-4">
        <h2 class="text-lg font-semibold text-[var(--crm-text)]">2. Adaptive SLA Prioritization (Bandit)</h2>
        <p class="mt-1 text-sm text-[var(--crm-text-soft)]">
          Simulate online allocation between lead queues using an exploration-exploitation policy.
        </p>

        <div class="mt-4 flex flex-wrap items-center gap-2">
          <Button :label="__('Run 1 Iteration')" @click="runBanditIteration(1)" />
          <Button :label="__('Run 10 Iterations')" @click="runBanditIteration(10)" />
          <Button :label="__('Save Run')" @click="saveBanditRun" />
          <Button :label="__('Reset')" @click="resetBandit" />
        </div>

        <div class="mt-4 grid grid-cols-3 gap-2 text-sm">
          <div class="metric-box">
            <p class="label">Iterations</p>
            <p class="value">{{ bandit.iterations }}</p>
          </div>
          <div class="metric-box">
            <p class="label">Avg. FRT</p>
            <p class="value">{{ bandit.avgFrt.toFixed(2) }}h</p>
          </div>
          <div class="metric-box">
            <p class="label">Cumulative Regret</p>
            <p class="value">{{ bandit.regret.toFixed(2) }}</p>
          </div>
        </div>
      </section>

      <section class="research-card rounded-2xl p-4">
        <h2 class="text-lg font-semibold text-[var(--crm-text)]">3. Explainable Lead Scoring</h2>
        <p class="mt-1 text-sm text-[var(--crm-text-soft)]">
          Generate a score with interpretable feature contributions and confidence estimate.
        </p>

        <div class="mt-4 grid gap-3 sm:grid-cols-2">
          <label class="field sm:col-span-2">
            <span>Select Lead to Analyze</span>
            <select v-model="explainable.leadName" class="field-input text-ellipsis">
              <option value="">-- Choose Lead --</option>
              <option v-for="lead in leadsList.data" :key="lead.name" :value="lead.name">
                {{ lead.lead_name || lead.name }}
              </option>
            </select>
          </label>
          <label class="field">
            <span>Email Engagement Focus</span>
            <input v-model.number="explainable.emailEngagement" type="range" min="0" max="100" />
            <strong>{{ explainable.emailEngagement }}</strong>
          </label>
          <label class="field">
            <span>Deal Value Fit Emphasis</span>
            <input v-model.number="explainable.valueFit" type="range" min="0" max="100" />
            <strong>{{ explainable.valueFit }}</strong>
          </label>
        </div>

        <div class="mt-4 result-box">
          <p class="text-sm text-[var(--crm-text-soft)]">Predicted Conversion Score</p>
          <p class="text-base font-semibold">{{ explainableResult.score }}/100</p>
          <p class="mt-1 text-sm text-[var(--crm-text-soft)]">Confidence: {{ explainableResult.confidence }}%</p>
          <ul class="mt-2 list-disc pl-5 text-sm text-[var(--crm-text)]">
            <li v-for="reason in explainableResult.reasons" :key="reason">{{ reason }}</li>
          </ul>
          <div class="mt-3">
            <Button :label="__('Save Run')" @click="saveExplainableRun" />
          </div>
        </div>
      </section>

      <section class="research-card rounded-2xl p-4">
        <h2 class="text-lg font-semibold text-[var(--crm-text)]">4. Outcome-Aware Activity Summarization</h2>
        <p class="mt-1 text-sm text-[var(--crm-text-soft)]">
          Convert activity logs into concise summary, risk flags, and recommended next steps.
        </p>

        <label class="field mt-4">
          <span>Target Note / Call Log</span>
          <select 
            v-model="selectedNote"
            class="field-input text-ellipsis"
            @change="syncNoteContent"
          >
            <option :value="null">-- Custom text --</option>
            <option v-for="note in notesList.data" :key="note.name" :value="note">
              {{ note.title || note.name }} ({{ note.reference_doctype }})
            </option>
          </select>
        </label>
        <textarea
          v-model="summaryInput"
          class="mt-3 h-28 w-full rounded-xl border border-[var(--crm-border)] bg-transparent p-3 text-sm outline-none"
          placeholder="Paste call/email activity notes in English or select a real Note above"
        />

        <div class="mt-3 flex gap-2">
          <Button :label="__('Generate Summary')" @click="generateSummary" />
          <Button :label="__('Save Run')" @click="saveSummaryRun" />
        </div>

        <div class="result-box mt-4">
          <p class="text-sm text-[var(--crm-text-soft)]">Summary</p>
          <p class="mt-1 text-sm">{{ summaryOutput.summary }}</p>
          <p class="mt-2 text-sm text-[var(--crm-text-soft)]">Risk Flags</p>
          <ul class="mt-1 list-disc pl-5 text-sm">
            <li v-for="risk in summaryOutput.risks" :key="risk">{{ risk }}</li>
          </ul>
          <p class="mt-2 text-sm text-[var(--crm-text-soft)]">Next Actions</p>
          <ul class="mt-1 list-disc pl-5 text-sm">
            <li v-for="action in summaryOutput.actions" :key="action">{{ action }}</li>
          </ul>
        </div>
      </section>

      <section class="research-card rounded-2xl p-4 lg:col-span-2">
        <h2 class="text-lg font-semibold text-[var(--crm-text)]">5. Fairness and Bias Audit Dashboard</h2>
        <p class="mt-1 text-sm text-[var(--crm-text-soft)]">
          Compare quality metrics across groups and track parity gaps over time.
        </p>

        <div class="mt-4 overflow-auto">
          <table class="w-full min-w-[620px] text-sm">
            <thead>
              <tr class="text-left text-[var(--crm-text-soft)]">
                <th class="pb-2">Group</th>
                <th class="pb-2">Precision</th>
                <th class="pb-2">Recall</th>
                <th class="pb-2">Approval Rate</th>
                <th class="pb-2">Parity Gap</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="row in fairnessRows"
                :key="row.group"
                class="border-t border-[var(--crm-border)]"
              >
                <td class="py-2">{{ row.group }}</td>
                <td class="py-2">{{ row.precision.toFixed(2) }}</td>
                <td class="py-2">{{ row.recall.toFixed(2) }}</td>
                <td class="py-2">{{ row.approvalRate.toFixed(2) }}</td>
                <td class="py-2" :class="row.parityGap > 0.12 ? 'text-rose-300' : 'text-emerald-300'">
                  {{ row.parityGap.toFixed(2) }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="mt-3 flex gap-2">
          <Button :label="__('Save Fairness Audit')" @click="saveFairnessRun" />
          <Button :label="__('Reload Snapshot')" @click="loadFairnessSnapshot" />
        </div>
      </section>

      <section class="research-card rounded-2xl p-4 lg:col-span-2">
        <h2 class="text-lg font-semibold text-[var(--crm-text)]">A/B Periodic Report</h2>
        <p class="mt-1 text-sm text-[var(--crm-text-soft)]">
          Aggregated experiment performance by variant over a rolling period.
        </p>

        <div class="mt-3 flex items-end gap-3">
          <label class="field">
            <span>Period (days)</span>
            <input v-model.number="abPeriodDays" type="number" min="1" class="field-input w-28" />
          </label>
          <Button :label="__('Refresh Report')" @click="loadABReport" />
        </div>

        <div class="mt-4 overflow-auto">
          <table class="w-full min-w-[820px] text-sm">
            <thead>
              <tr class="text-left text-[var(--crm-text-soft)]">
                <th class="pb-2">Experiment</th>
                <th class="pb-2">Variant</th>
                <th class="pb-2">Runs</th>
                <th class="pb-2">Success Rate</th>
                <th class="pb-2">Avg Conversion Delta</th>
                <th class="pb-2">Avg Response Time</th>
                <th class="pb-2">Avg Regret</th>
                <th class="pb-2">Avg Fairness Gap</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="row in abReportRows"
                :key="row.experiment_type + row.variant"
                class="border-t border-[var(--crm-border)]"
              >
                <td class="py-2">{{ row.experiment_type }}</td>
                <td class="py-2">{{ row.variant }}</td>
                <td class="py-2">{{ row.runs }}</td>
                <td class="py-2">{{ row.success_rate }}%</td>
                <td class="py-2">{{ formatNumber(row.avg_conversion_delta_percent) }}</td>
                <td class="py-2">{{ formatNumber(row.avg_response_time_hours) }}</td>
                <td class="py-2">{{ formatNumber(row.avg_regret) }}</td>
                <td class="py-2">{{ formatNumber(row.avg_fairness_gap) }}</td>
              </tr>
              <tr v-if="!abReportRows.length" class="border-t border-[var(--crm-border)]">
                <td class="py-2 text-[var(--crm-text-soft)]" colspan="8">No runs available in selected period.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>
    </div>
    <p v-if="statusMessage" class="mt-4 text-sm text-[var(--crm-text-soft)]">{{ statusMessage }}</p>
  </div>
</template>

<script setup>
import LayoutHeader from '@/components/LayoutHeader.vue'
import ViewBreadcrumbs from '@/components/ViewBreadcrumbs.vue'
import { Button, call, createListResource } from 'frappe-ui'
import { computed, onMounted, ref } from 'vue'

const leadsList = createListResource({
  doctype: 'CRM Lead',
  fields: ['name', 'lead_name'],
  limit: 100,
  auto: true,
})

const dealsList = createListResource({
  doctype: 'CRM Deal',
  fields: ['name', 'deal_name', 'organization'],
  limit: 100,
  auto: true,
})

const notesList = createListResource({
  doctype: 'CRM Note',
  fields: ['name', 'title', 'content', 'reference_doctype', 'reference_name'],
  limit: 100,
  auto: true,
})

const selectedNote = ref(null)

function stripHtml(html) {
  let tmp = document.createElement('DIV');
  tmp.innerHTML = html;
  return tmp.textContent || tmp.innerText || '';
}

function syncNoteContent() {
  if (selectedNote.value && selectedNote.value.content) {
    summaryInput.value = stripHtml(selectedNote.value.content)
  }
}

const statusMessage = ref('')

const causal = ref({
  intent: 62,
  delay: 18,
  referenceDoctype: '',
  referenceName: '',
})

const outcome = ref({
  observedOutcome: 'Follow-up meeting booked',
  conversionDelta: 4.2,
})

const causalResult = ref({
  run_name: '',
  recommended_action: 'Schedule a discovery call',
  expected_uplift: 0,
})

async function runNextBestAction() {
  const data = await call('crm.api.research_lab.recommend_next_best_action', {
    reference_doctype: causal.value.referenceDoctype || undefined,
    reference_name: causal.value.referenceName || undefined,
    intent_score: causal.value.intent,
    response_delay_hours: causal.value.delay,
  })

  causalResult.value = {
    run_name: data.run_name,
    recommended_action: data.recommended_action,
    expected_uplift: data.expected_uplift,
  }
  statusMessage.value = `Next-Best-Action run saved as ${data.run_name}`
}

async function logOutcome(isSuccess) {
  if (!causalResult.value.run_name) {
    statusMessage.value = 'Run recommendation first before logging outcome.'
    return
  }

  await call('crm.api.research_lab.log_next_best_action_outcome', {
    run_name: causalResult.value.run_name,
    is_success: isSuccess ? 1 : 0,
    observed_outcome: outcome.value.observedOutcome,
    conversion_delta_percent: outcome.value.conversionDelta,
    response_time_hours: causal.value.delay,
  })

  statusMessage.value = `Outcome logged for ${causalResult.value.run_name}`
  await loadABReport()
}

const bandit = ref({
  iterations: 0,
  avgFrt: 3.8,
  regret: 0,
})

function runBanditIteration(count) {
  call('crm.api.research_lab.get_real_bandit_metrics', { iterations: bandit.value.iterations + count })
    .then(res => {
      bandit.value.iterations += count
      bandit.value.avgFrt = res.avgFrt
      bandit.value.regret = res.regret
    })
}

function resetBandit() {
  bandit.value = { iterations: 0, avgFrt: 3.8, regret: 0 }
}

async function saveBanditRun() {
  await call('crm.api.research_lab.log_research_run', {
    experiment_type: 'Adaptive SLA Bandit',
    variant: 'ucb-v1',
    input_payload: {
      iterations: bandit.value.iterations,
    },
    result_payload: {
      avg_frt: bandit.value.avgFrt,
      regret: bandit.value.regret,
    },
    metrics_payload: {
      avg_frt: bandit.value.avgFrt,
      regret: bandit.value.regret,
      conversion_delta_percent: Math.max(0, 4.2 - bandit.value.regret * 1.1),
    },
    is_success: bandit.value.regret < 0.2 ? 1 : 0,
  })
  statusMessage.value = 'Bandit run saved.'
  await loadABReport()
}

const explainable = ref({
  leadName: '',
  emailEngagement: 55,
  valueFit: 68,
})

import { watch } from 'vue'

const explainableResult = ref({
  score: 50,
  confidence: 0,
  reasons: []
})

watch(() => explainable.value.leadName, async (newVal) => {
  if (newVal) {
    const res = await call('crm.api.research_lab.calculate_explainable_score', { lead_name: newVal })
    explainableResult.value = res
  } else {
    explainableResult.value = { score: 50, confidence: 0, reasons: [] }
  }
})

async function saveExplainableRun() {
  await call('crm.api.research_lab.log_research_run', {
    experiment_type: 'Explainable Scoring',
    variant: 'explainable-v1',
    input_payload: {
      email_engagement: explainable.value.emailEngagement,
      value_fit: explainable.value.valueFit,
    },
    result_payload: explainableResult.value,
    metrics_payload: {
      conversion_delta_percent: Math.max(0, (explainableResult.value.score - 50) / 10),
    },
    is_success: explainableResult.value.score >= 70 ? 1 : 0,
  })
  statusMessage.value = 'Explainable scoring run saved.'
  await loadABReport()
}

const summaryInput = ref('')
const summaryOutput = ref({
  summary: '',
  risks: [],
  actions: [],
})

async function generateSummary() {
  const text = summaryInput.value.trim()
  if (!text) return

  const res = await call('crm.api.research_lab.generate_summary_for_note', { note_content: text })
  summaryOutput.value = res
}

async function saveSummaryRun() {
  const riskCount = summaryOutput.value.risks.length
  await call('crm.api.research_lab.log_research_run', {
    experiment_type: 'Outcome Summary',
    variant: 'summary-v1',
    input_payload: { text: summaryInput.value },
    result_payload: summaryOutput.value,
    metrics_payload: {
      conversion_delta_percent: Math.max(0, 2.5 - riskCount * 0.4),
    },
    is_success: riskCount <= 2 ? 1 : 0,
  })
  statusMessage.value = 'Activity summary run saved.'
  await loadABReport()
}

const fairnessRows = ref([])

onMounted(async () => {
  await runNextBestAction()
  await loadABReport()
  
  // Fetch real fairness audit layout
  const res = await call('crm.api.research_lab.get_real_fairness_audit')
  fairnessRows.value = res || []
})

async function saveFairnessRun() {
  const fairnessGap = Math.max(...fairnessRows.value.map((row) => row.parityGap || 0))
  await call('crm.api.research_lab.log_research_run', {
    experiment_type: 'Fairness Audit',
    variant: 'fairness-v1',
    result_payload: { rows: fairnessRows.value },
    metrics_payload: {
      fairness_gap: fairnessGap,
    },
    is_success: fairnessGap <= 0.12 ? 1 : 0,
  })
  statusMessage.value = 'Fairness audit run saved.'
  await loadABReport()
}

async function loadFairnessSnapshot() {
  const data = await call('crm.api.research_lab.get_fairness_snapshot', {
    period_days: abPeriodDays.value,
  })
  if (data.rows?.length) {
    fairnessRows.value = data.rows
    statusMessage.value = `Loaded fairness snapshot from ${data.last_run}`
  } else {
    statusMessage.value = 'No fairness snapshot found in selected period.'
  }
}

const abPeriodDays = ref(30)
const abReportRows = ref([])

async function loadABReport() {
  const report = await call('crm.api.research_lab.get_ab_report', {
    period_days: abPeriodDays.value,
  })
  abReportRows.value = report.rows || []
}

function formatNumber(v) {
  return v === null || v === undefined ? 'N/A' : Number(v).toFixed(2)
}


</script>

<style scoped>
.research-shell {
  min-height: 100%;
}

.research-card {
  border: 1px solid var(--crm-border);
  background:
    linear-gradient(170deg, rgba(116, 97, 255, 0.14), rgba(12, 14, 24, 0.72));
  box-shadow: 0 14px 28px rgba(3, 6, 20, 0.28);
}

.field {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  font-size: 0.9rem;
  color: var(--crm-text-soft);
}

.field strong {
  color: var(--crm-text);
  font-weight: 600;
}

.field-input {
  border: 1px solid var(--crm-border);
  border-radius: 0.7rem;
  background: rgba(9, 12, 22, 0.3);
  color: var(--crm-text);
  padding: 0.42rem 0.55rem;
  outline: none;
}

.result-box {
  border: 1px solid var(--crm-border);
  border-radius: 0.85rem;
  padding: 0.75rem;
  background: rgba(9, 12, 22, 0.45);
}

.metric-box {
  border: 1px solid var(--crm-border);
  border-radius: 0.75rem;
  padding: 0.55rem 0.65rem;
  background: rgba(9, 12, 22, 0.45);
}

.metric-box .label {
  font-size: 0.75rem;
  color: var(--crm-text-soft);
}

.metric-box .value {
  font-size: 0.98rem;
  font-weight: 600;
  color: var(--crm-text);
  margin-top: 0.15rem;
}
</style>
