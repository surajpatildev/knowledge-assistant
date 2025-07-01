import React from 'react'

interface StatusBadgeProps {
  status: 'active' | 'inactive' | 'error' | 'testing' | 'healthy' | 'unhealthy'
  text?: string
}

export const StatusBadge: React.FC<StatusBadgeProps> = ({ status, text }) => {
  const getStatusStyles = (status: string) => {
    switch (status) {
      case 'active':
      case 'healthy':
        return 'bg-green-100 text-green-800'
      case 'inactive':
        return 'bg-gray-100 text-gray-800'
      case 'error':
      case 'unhealthy':
        return 'bg-red-100 text-red-800'
      case 'testing':
        return 'bg-yellow-100 text-yellow-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  return (
    <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusStyles(status)}`}>
      {text || status}
    </span>
  )
}