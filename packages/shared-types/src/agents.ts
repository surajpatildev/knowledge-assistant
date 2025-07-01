// Agent system types

export type AgentType = 'orchestrator' | 'router' | 'sql' | 'analysis' | 'ui' | 'memory'

export type TaskStatus = 'pending' | 'running' | 'completed' | 'failed'

export interface AgentTask {
  id: string
  agent: AgentType
  action: string
  params: Record<string, any>
  dependencies: string[]
  parallel?: boolean
  stream_result?: boolean
  status?: TaskStatus
}

export interface ExecutionPlan {
  steps: AgentTask[]
  estimated_time?: number
  complexity?: 'simple' | 'medium' | 'complex'
}

export interface AgentResult {
  success: boolean
  data?: any
  metadata?: Record<string, any>
  error?: string
  execution_time?: number
  viz_hint?: string
}

export interface IntentClassification {
  primary_intent: string
  secondary_intents: string[]
  complexity: 'simple' | 'medium' | 'complex'
  data_sources: string[]
  confidence: number
  reasoning: string
}

export interface QueryAnalysis {
  sql?: string
  explanation?: string
  estimated_cost?: Record<string, any>
  data_source?: string
  row_count?: number
  execution_time?: number
}

export interface AnalysisResult {
  analysis_type: string
  results: Record<string, any>
  insights: string[]
  recommendations: string[]
}