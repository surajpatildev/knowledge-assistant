import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'

export default function HomePage() {
  return (
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold tracking-tight text-gray-900 sm:text-6xl">
            Data Lens
          </h1>
          <p className="mt-6 text-lg leading-8 text-gray-600">
            Enterprise Knowledge Assistant - Interact with your data through natural language
          </p>
        </div>

        {/* Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
          <Card>
            <CardHeader>
              <CardTitle>Natural Language Queries</CardTitle>
              <CardDescription>
                Ask questions about your data in plain English
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-gray-600">
                No need to write SQL or learn complex query languages. Just ask what you want to know.
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Dynamic Visualizations</CardTitle>
              <CardDescription>
                Automatically generated charts and dashboards
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-gray-600">
                AI-powered visualizations that adapt to your data and query context.
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Multi-Source Integration</CardTitle>
              <CardDescription>
                Connect to databases, APIs, and files
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-gray-600">
                Seamlessly query across multiple data sources in a single conversation.
              </p>
            </CardContent>
          </Card>
        </div>

        {/* CTA Section */}
        <div className="text-center">
          <Link href="/chat">
            <Button size="lg" className="mr-4">
              Start Chatting
            </Button>
          </Link>
          <Link href="/data-sources">
            <Button variant="outline" size="lg">
              Manage Data Sources
            </Button>
          </Link>
        </div>

        {/* Status */}
        <div className="mt-12 text-center">
          <p className="text-sm text-gray-500">
            Status: Development Mode | Version 1.0.0
          </p>
        </div>
      </div>
    </div>
  )
}