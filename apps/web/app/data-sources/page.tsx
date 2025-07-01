"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Plus, Database, FileText, Globe, TestTube } from "lucide-react";

interface DataSource {
  id: string;
  name: string;
  type: "postgresql" | "mysql" | "csv" | "api";
  status: "active" | "inactive" | "error";
  description: string;
  lastConnected: string;
}

const mockDataSources: DataSource[] = [
  {
    id: "1",
    name: "Main PostgreSQL DB",
    type: "postgresql",
    status: "active",
    description: "Primary application database",
    lastConnected: "2024-01-15T10:30:00Z",
  },
  {
    id: "2",
    name: "Sales Analytics",
    type: "mysql",
    status: "active",
    description: "Sales and revenue data",
    lastConnected: "2024-01-15T09:45:00Z",
  },
  {
    id: "3",
    name: "Customer Data Export",
    type: "csv",
    status: "inactive",
    description: "Monthly customer export",
    lastConnected: "2024-01-10T14:20:00Z",
  },
];

const getTypeIcon = (type: DataSource["type"]) => {
  switch (type) {
    case "postgresql":
    case "mysql":
      return <Database className="w-4 h-4" />;
    case "csv":
      return <FileText className="w-4 h-4" />;
    case "api":
      return <Globe className="w-4 h-4" />;
    default:
      return <Database className="w-4 h-4" />;
  }
};

const getStatusColor = (status: DataSource["status"]) => {
  switch (status) {
    case "active":
      return "bg-green-100 text-green-800";
    case "inactive":
      return "bg-gray-100 text-gray-800";
    case "error":
      return "bg-red-100 text-red-800";
    default:
      return "bg-gray-100 text-gray-800";
  }
};

export default function DataSourcesPage() {
  const [dataSources] = useState<DataSource[]>(mockDataSources);

  const handleTestConnection = (id: string) => {
    // TODO: Implement actual connection testing
    console.log("Testing connection for data source:", id);
  };

  const handleAddDataSource = () => {
    // TODO: Implement data source creation modal
    console.log("Add new data source");
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold tracking-tight">Data Sources</h1>
            <p className="text-gray-600 mt-2">
              Manage your database connections and data sources
            </p>
          </div>
          <Button onClick={handleAddDataSource}>
            <Plus className="w-4 h-4 mr-2" />
            Add Data Source
          </Button>
        </div>

        {/* Data Sources Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {dataSources.map((source) => (
            <Card key={source.id} className="hover:shadow-md transition-shadow">
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    {getTypeIcon(source.type)}
                    <CardTitle className="text-lg">{source.name}</CardTitle>
                  </div>
                  <Badge className={getStatusColor(source.status)}>
                    {source.status}
                  </Badge>
                </div>
                <CardDescription>{source.description}</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <div>
                    <p className="text-sm text-gray-600">Type</p>
                    <p className="font-medium capitalize">{source.type}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Last Connected</p>
                    <p className="font-medium">
                      {new Date(source.lastConnected).toLocaleDateString()}
                    </p>
                  </div>
                  <div className="pt-2">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => handleTestConnection(source.id)}
                      className="w-full"
                    >
                      <TestTube className="w-4 h-4 mr-2" />
                      Test Connection
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Empty State */}
        {dataSources.length === 0 && (
          <div className="text-center py-12">
            <Database className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              No data sources configured
            </h3>
            <p className="text-gray-600 mb-4">
              Get started by adding your first data source
            </p>
            <Button onClick={handleAddDataSource}>
              <Plus className="w-4 h-4 mr-2" />
              Add Data Source
            </Button>
          </div>
        )}
      </div>
    </div>
  );
}
