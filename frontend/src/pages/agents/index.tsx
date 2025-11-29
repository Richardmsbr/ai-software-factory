import Head from 'next/head';
import { useQuery } from '@tanstack/react-query';
import Layout from '@/components/Layout';
import { agentsApi } from '@/lib/api';
import { Agent } from '@/types';

export default function AgentsPage() {
  const { data: agents, isLoading } = useQuery<Agent[]>({
    queryKey: ['agents'],
    queryFn: async () => {
      const response = await agentsApi.list();
      return response.data;
    },
  });

  const groupedAgents = agents?.reduce((acc, agent) => {
    if (!acc[agent.role]) {
      acc[agent.role] = [];
    }
    acc[agent.role].push(agent);
    return acc;
  }, {} as Record<string, Agent[]>);

  return (
    <>
      <Head>
        <title>Agents - AI Software Factory</title>
      </Head>
      <Layout>
        <div className="space-y-6">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Agents</h1>
            <p className="mt-2 text-gray-600">
              Your specialized AI workforce
            </p>
          </div>

          {isLoading ? (
            <div className="text-center py-12">
              <p className="text-gray-500">Loading agents...</p>
            </div>
          ) : groupedAgents ? (
            <div className="space-y-6">
              {Object.entries(groupedAgents).map(([role, roleAgents]) => (
                <div key={role} className="bg-white rounded-lg shadow">
                  <div className="px-6 py-4 border-b border-gray-200">
                    <h2 className="text-lg font-semibold text-gray-900">
                      {role}
                    </h2>
                  </div>
                  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 p-6">
                    {roleAgents.map((agent) => (
                      <AgentCard key={agent.id} agent={agent} />
                    ))}
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-12 bg-white rounded-lg shadow">
              <p className="text-gray-500">No agents available</p>
            </div>
          )}
        </div>
      </Layout>
    </>
  );
}

function AgentCard({ agent }: { agent: Agent }) {
  const successRate = agent.total_tasks > 0
    ? ((agent.completed_tasks / agent.total_tasks) * 100).toFixed(0)
    : '0';

  return (
    <div className="border border-gray-200 rounded-lg p-4">
      <div className="flex items-start justify-between">
        <div>
          <h3 className="font-medium text-gray-900">{agent.name}</h3>
          <p className="text-sm text-gray-500 mt-1">{agent.role}</p>
        </div>
        <StatusIndicator status={agent.status} />
      </div>
      <div className="mt-4 space-y-2">
        <div className="flex justify-between text-sm">
          <span className="text-gray-600">Tasks</span>
          <span className="font-medium">{agent.total_tasks}</span>
        </div>
        <div className="flex justify-between text-sm">
          <span className="text-gray-600">Success Rate</span>
          <span className="font-medium">{successRate}%</span>
        </div>
      </div>
    </div>
  );
}

function StatusIndicator({ status }: { status: string }) {
  const colors = {
    idle: 'bg-gray-400',
    busy: 'bg-green-500',
    error: 'bg-red-500',
    offline: 'bg-gray-300',
  }[status] || 'bg-gray-400';

  return (
    <div className="flex items-center gap-2">
      <div className={`w-2 h-2 rounded-full ${colors}`} />
      <span className="text-xs text-gray-600 capitalize">{status}</span>
    </div>
  );
}
