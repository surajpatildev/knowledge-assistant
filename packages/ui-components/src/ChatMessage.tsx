import React from 'react'
import { Message } from '@data-lens/shared-types'

interface ChatMessageProps {
  message: Message
  showTimestamp?: boolean
}

export const ChatMessage: React.FC<ChatMessageProps> = ({
  message,
  showTimestamp = true
}) => {
  const isUser = message.role === 'user'
  
  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}>
      <div className={`max-w-[80%] rounded-lg px-3 py-2 ${
        isUser 
          ? 'bg-blue-600 text-white' 
          : 'bg-gray-100 text-gray-900'
      }`}>
        <p className="text-sm">{message.content}</p>
        {showTimestamp && (
          <p className="text-xs opacity-70 mt-1">
            {message.timestamp.toLocaleTimeString()}
          </p>
        )}
      </div>
    </div>
  )
}