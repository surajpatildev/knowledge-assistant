// Data source types

export type DataSourceType = 'postgresql' | 'mysql' | 'sqlite' | 'csv' | 'json' | 'api' | 'excel'

export type DataSourceStatus = 'active' | 'inactive' | 'error' | 'testing'

export interface DataSource {
  id: string
  name: string
  type: DataSourceType
  description: string
  connectionString: string
  status: DataSourceStatus
  createdAt: string
  updatedAt: string
  lastConnected?: string
  metadata?: Record<string, any>
}

export interface DataSourceCreate {
  name: string
  type: DataSourceType
  description?: string
  connectionString: string
  metadata?: Record<string, any>
}

export interface DataSourceUpdate {
  name?: string
  description?: string
  connectionString?: string
  metadata?: Record<string, any>
}

export interface ConnectionTest {
  dataSourceId: string
  status: 'success' | 'failure'
  message: string
  timestamp: string
  details?: Record<string, any>
}

export interface DatabaseSchema {
  dataSourceId: string
  tables: Record<string, TableSchema>
  views?: Record<string, ViewSchema>
}

export interface TableSchema {
  name: string
  columns: Record<string, ColumnSchema>
  primaryKey?: string[]
  foreignKeys?: ForeignKeySchema[]
  indexes?: IndexSchema[]
}

export interface ViewSchema {
  name: string
  columns: Record<string, ColumnSchema>
  definition: string
}

export interface ColumnSchema {
  name: string
  type: string
  nullable: boolean
  primaryKey?: boolean
  unique?: boolean
  defaultValue?: any
  comment?: string
}

export interface ForeignKeySchema {
  columnName: string
  referencedTable: string
  referencedColumn: string
}

export interface IndexSchema {
  name: string
  columns: string[]
  unique: boolean
}