// Common API types

export interface ApiResponse<T = any> {
  success: boolean
  data?: T
  error?: string
  message?: string
}

export interface PaginatedResponse<T> extends ApiResponse<T[]> {
  pagination: {
    page: number
    limit: number
    total: number
    totalPages: number
  }
}

export interface HealthCheck {
  status: 'healthy' | 'unhealthy'
  service: string
  version?: string
  timestamp: string
}

export interface DetailedHealthCheck extends HealthCheck {
  services: Record<string, 'healthy' | 'unhealthy' | 'unknown'>
}