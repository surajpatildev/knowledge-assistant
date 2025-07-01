import React from 'react'
import { DataSource } from '@data-lens/shared-types'

interface DataSourceCardProps {
  dataSource: DataSource
  onTest?: (id: string) => void
  onEdit?: (id: string) => void
  onDelete?: (id: string) => void
}

export const DataSourceCard: React.FC<DataSourceCardProps> = ({
  dataSource,
  onTest,
  onEdit,
  onDelete
}) => {
  return (
    <div className="border rounded-lg p-4 hover:shadow-md transition-shadow">
      <div className="flex items-center justify-between mb-2">
        <h3 className="text-lg font-semibold">{dataSource.name}</h3>
        <span className={`px-2 py-1 rounded text-xs ${
          dataSource.status === 'active' ? 'bg-green-100 text-green-800' :
          dataSource.status === 'error' ? 'bg-red-100 text-red-800' :
          'bg-gray-100 text-gray-800'
        }`}>
          {dataSource.status}
        </span>
      </div>
      <p className="text-gray-600 text-sm mb-3">{dataSource.description}</p>
      <div className="flex space-x-2">
        {onTest && (
          <button
            onClick={() => onTest(dataSource.id)}
            className="px-3 py-1 bg-blue-500 text-white rounded text-sm hover:bg-blue-600"
          >
            Test
          </button>
        )}
        {onEdit && (
          <button
            onClick={() => onEdit(dataSource.id)}
            className="px-3 py-1 bg-gray-500 text-white rounded text-sm hover:bg-gray-600"
          >
            Edit
          </button>
        )}
        {onDelete && (
          <button
            onClick={() => onDelete(dataSource.id)}
            className="px-3 py-1 bg-red-500 text-white rounded text-sm hover:bg-red-600"
          >
            Delete
          </button>
        )}
      </div>
    </div>
  )
}