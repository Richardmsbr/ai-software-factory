import Head from 'next/head';
import Link from 'next/link';
import { useQuery } from '@tanstack/react-query';
import Layout from '@/components/Layout';
import { projectsApi, agentsApi, healthApi } from '@/lib/api';
import { Project, Agent } from '@/types';

export default function Home() {
  const { data: projects } = useQuery<Project[]>({
    queryKey: ['projects'],
    queryFn: async () => {
      const response = await projectsApi.list({ limit: 5 });
      return response.data;
    },
  });

  const { data: agents } = useQuery<Agent[]>({
    queryKey: ['agents'],
    queryFn: async () => {
      const response = await agentsApi.list({ limit: 10 });
      return response.data;
    },
  });

  const { data: health } = useQuery({
    queryKey: ['health'],
    queryFn: async () => {
      const response = await healthApi.check();
      return response.data;
    },
    refetchInterval: 30000, // Refresh every 30s
  });

  const activeProjects = projects?.filter(p => 
    ['planning', 'in_progress', 'testing'].includes(p.status)
  ).length || 0;

  const busyAgents = agents?.filter(a => a.status === 'busy').length || 0;
  const idleAgents = agents?.filter(a => a.status === 'idle').length || 0;

  return (
    <>
      <Head>
        <title>AI Software Factory</title>
        <meta name="description" content="Enterprise software development factory" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </Head>
      <Layout>
        <div className="space-y-6">
          {/* Header */}
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
            <p className="mt-2 text-gray-600">
              Overview of your software factory operations
            </p>
          </div>

          {/* Stats Grid */}
          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
            <StatCard
              title="Active Projects"
              value={activeProjects}
              subtitle={`${projects?.length || 0} total`}
              color="blue"
            />
            <StatCard
              title="Working Agents"
              value={busyAgents}
              subtitle={`${idleAgents} available`}
              color="green"
            />
            <StatCard
              title="Total Agents"
              value={agents?.length || 0}
              subtitle="Specialized workers"
              color="purple"
            />
            <StatCard
              title="System Status"
              value={health?.status === 'healthy' ? 'Operational' : 'Degraded'}
              subtitle={health?.version || 'v1.0.0'}
              color={health?.status === 'healthy' ? 'green' : 'red'}
            />
          </div>

          {/* Recent Projects */}
          <div className="bg-white rounded-lg shadow">
            <div className="px-6 py-4 border-b border-gray-200">
              <div className="flex items-center justify-between">
                <h2 className="text-lg font-semibold text-gray-900">
                  Recent Projects
                </h2>
                <Link
                  href="/projects"
                  className="text-sm font-medium text-primary-600 hover:text-primary-700"
                >
                  View all
                </Link>
              </div>
            </div>
            <div className="divide-y divide-gray-200">
              {projects && projects.length > 0 ? (
                projects.slice(0, 5).map((project) => (
                  <Link
                    key={project.id}
                    href={`/projects/${project.id}`}
                    className="block px-6 py-4 hover:bg-gray-50 transition-colors"
                  >
                    <div className="flex items-center justify-between">
                      <div>
                        <h3 className="text-sm font-medium text-gray-900">
                          {project.name}
                        </h3>
                        <p className="mt-1 text-sm text-gray-500">
                          {project.description || 'No description'}
                        </p>
                      </div>
                      <StatusBadge status={project.status} />
                    </div>
                  </Link>
                ))
              ) : (
                <div className="px-6 py-8 text-center text-gray-500">
                  No projects yet. Create your first project to get started.
                </div>
              )}
            </div>
          </div>

          {/* Agents Status */}
          <div className="bg-white rounded-lg shadow">
            <div className="px-6 py-4 border-b border-gray-200">
              <div className="flex items-center justify-between">
                <h2 className="text-lg font-semibold text-gray-900">
                  Agent Status
                </h2>
                <Link
                  href="/agents"
                  className="text-sm font-medium text-primary-600 hover:text-primary-700"
                >
                  View all
                </Link>
              </div>
            </div>
            <div className="p-6">
              <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4">
                {agents?.slice(0, 10).map((agent) => (
                  <div
                    key={agent.id}
                    className="flex flex-col items-center p-4 bg-gray-50 rounded-lg"
                  >
                    <div className={`w-3 h-3 rounded-full mb-2 ${
                      agent.status === 'busy' ? 'bg-green-500' :
                      agent.status === 'idle' ? 'bg-gray-400' :
                      'bg-red-500'
                    }`} />
                    <p className="text-xs font-medium text-gray-900 text-center">
                      {agent.name}
                    </p>
                    <p className="text-xs text-gray-500 mt-1">
                      {agent.role}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </Layout>
    </>
  );
}

function StatCard({ 
  title, 
  value, 
  subtitle, 
  color 
}: { 
  title: string; 
  value: string | number; 
  subtitle: string; 
  color: string;
}) {
  const colorClasses = {
    blue: 'bg-blue-50 text-blue-700',
    green: 'bg-green-50 text-green-700',
    purple: 'bg-purple-50 text-purple-700',
    red: 'bg-red-50 text-red-700',
  }[color] || 'bg-gray-50 text-gray-700';

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <p className="text-sm font-medium text-gray-600">{title}</p>
      <p className={`mt-2 text-3xl font-semibold ${colorClasses.split(' ')[1]}`}>
        {value}
      </p>
      <p className="mt-1 text-sm text-gray-500">{subtitle}</p>
    </div>
  );
}

function StatusBadge({ status }: { status: string }) {
  const styles = {
    pending: 'bg-gray-100 text-gray-800',
    planning: 'bg-blue-100 text-blue-800',
    in_progress: 'bg-yellow-100 text-yellow-800',
    testing: 'bg-purple-100 text-purple-800',
    review: 'bg-indigo-100 text-indigo-800',
    completed: 'bg-green-100 text-green-800',
    cancelled: 'bg-red-100 text-red-800',
  }[status] || 'bg-gray-100 text-gray-800';

  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${styles}`}>
      {status.replace('_', ' ')}
    </span>
  );
}
