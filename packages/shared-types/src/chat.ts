// Chat and messaging types

export interface Message {
  id: string
  content: string
  role: 'user' | 'assistant'
  timestamp: Date
  sessionId: string
  metadata?: Record<string, any>
}

export interface ChatQuery {
  query: string
  sessionId: string
  context?: Record<string, any>
  stream?: boolean
}

export interface ChatResponse {
  success: boolean
  message?: string
  data: Record<string, any>
  ui_components: UIComponent[]
  suggestions: string[]
  error?: string
}

export interface StreamEvent {
  type: 'thinking' | 'executing' | 'partial_result' | 'complete' | 'error'
  content?: string
  agent?: string
  action?: string
  data?: Record<string, any>
  ui?: UIComponent[]
  suggestions?: string[]
  message?: string
}

export interface UIComponent {
  type: 'chart' | 'table' | 'metric' | 'text' | 'layout'
  props: Record<string, any>
  id?: string
}