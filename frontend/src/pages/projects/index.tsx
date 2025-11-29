import Head from 'next/head';
import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import Layout from '@/components/Layout';
import { projectsApi } from '@/lib/api';
import { Project } from '@/types';
import { formatDateTime } from '@/lib/utils';

export default function ProjectsPage() {
  const [showCreateModal, setShowCreateModal] = useState(false);

  const { data: projects, isLoading } = useQuery<Project[]>({
    queryKey: ['projects'],
    queryFn: async () => {
      const response = await projectsApi.list();
      return response.data;
    },
  });

  return (
    <>
      <Head>
        <title>Projects - AI Software Factory</title>
      </Head>
      <Layout>
        <div className="space-y-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Projects</h1>
              <p className="mt-2 text-gray-600">
                Manage your software development projects
              </p>
            </div>
            <button
              onClick={() => setShowCreateModal(true)}
              className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors font-medium"
            >
              New Project
            </button>
          </div>

          {isLoading ? (
            <div className="text-center py-12">
              <p className="text-gray-500">Loading projects...</p>
            </div>
          ) : projects && projects.length > 0 ? (
            <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
              {projects.map((project) => (
                <ProjectCard key={project.id} project={project} />
              ))}
            </div>
          ) : (
            <div className="text-center py-12 bg-white rounded-lg shadow">
              <p className="text-gray-500">No projects yet</p>
              <button
                onClick={() => setShowCreateModal(true)}
                className="mt-4 text-primary-600 hover:text-primary-700 font-medium"
              >
                Create your first project
              </button>
            </div>
          )}
        </div>
      </Layout>
    </>
  );
}

function ProjectCard({ project }: { project: Project }) {
  return (
    <div className="bg-white rounded-lg shadow p-6 hover:shadow-lg transition-shadow">
      <div className="flex items-start justify-between">
        <h3 className="text-lg font-semibold text-gray-900">{project.name}</h3>
        <StatusBadge status={project.status} />
      </div>
      <p className="mt-2 text-sm text-gray-600 line-clamp-2">
        {project.description || 'No description'}
      </p>
      <div className="mt-4 text-xs text-gray-500">
        Created {formatDateTime(project.created_at)}
      </div>
    </div>
  );
}

function StatusBadge({ status }: { status: string }) {
  const styles = {
    pending: 'bg-gray-100 text-gray-800',
    planning: 'bg-blue-100 text-blue-800',
    in_progress: 'bg-yellow-100 text-yellow-800',
    testing: 'bg-purple-100 text-purple-800',
    completed: 'bg-green-100 text-green-800',
  }[status] || 'bg-gray-100 text-gray-800';

  return (
    <span className={`px-2 py-1 rounded text-xs font-medium ${styles}`}>
      {status.replace('_', ' ')}
    </span>
  );
}
