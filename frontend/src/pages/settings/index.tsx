import Head from 'next/head';
import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import Layout from '@/components/Layout';
import { settingsApi } from '@/lib/api';
import { APIKey, SystemConfig } from '@/types';

export default function SettingsPage() {
  return (
    <>
      <Head>
        <title>Settings - AI Software Factory</title>
      </Head>
      <Layout>
        <div className="space-y-6">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Settings</h1>
            <p className="mt-2 text-gray-600">
              Configure your factory settings and API keys
            </p>
          </div>

          <SystemConfiguration />
          <APIKeysManagement />
        </div>
      </Layout>
    </>
  );
}

function SystemConfiguration() {
  const { data: config } = useQuery<SystemConfig>({
    queryKey: ['config'],
    queryFn: async () => {
      const response = await settingsApi.getConfig();
      return response.data;
    },
  });

  if (!config) return null;

  return (
    <div className="bg-white rounded-lg shadow">
      <div className="px-6 py-4 border-b border-gray-200">
        <h2 className="text-lg font-semibold text-gray-900">
          System Configuration
        </h2>
      </div>
      <div className="p-6 space-y-4">
        <ConfigRow label="Application" value={config.app_name} />
        <ConfigRow label="Version" value={config.version} />
        <ConfigRow label="Default LLM Provider" value={config.default_llm_provider} />
        <ConfigRow label="Default Model" value={config.default_model} />
        <ConfigRow label="Max Agents" value={config.max_agents.toString()} />
        <ConfigRow label="Max Concurrent Projects" value={config.max_concurrent_projects.toString()} />
        <ConfigRow label="Memory Backend" value={config.memory_backend} />
        <ConfigRow 
          label="Ollama Available" 
          value={config.ollama_available ? 'Yes' : 'No'} 
        />
      </div>
    </div>
  );
}

function ConfigRow({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex justify-between py-2">
      <span className="text-sm font-medium text-gray-700">{label}</span>
      <span className="text-sm text-gray-900">{value}</span>
    </div>
  );
}

function APIKeysManagement() {
  const [showAddForm, setShowAddForm] = useState(false);
  const queryClient = useQueryClient();

  const { data: apiKeys } = useQuery<APIKey[]>({
    queryKey: ['apiKeys'],
    queryFn: async () => {
      const response = await settingsApi.listApiKeys();
      return response.data;
    },
  });

  const deleteMutation = useMutation({
    mutationFn: (provider: string) => settingsApi.deleteApiKey(provider),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['apiKeys'] });
    },
  });

  return (
    <div className="bg-white rounded-lg shadow">
      <div className="px-6 py-4 border-b border-gray-200">
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-semibold text-gray-900">
            API Keys
          </h2>
          <button
            onClick={() => setShowAddForm(!showAddForm)}
            className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors text-sm font-medium"
          >
            {showAddForm ? 'Cancel' : 'Add API Key'}
          </button>
        </div>
      </div>

      {showAddForm && (
        <AddAPIKeyForm 
          onSuccess={() => {
            setShowAddForm(false);
            queryClient.invalidateQueries({ queryKey: ['apiKeys'] });
          }}
        />
      )}

      <div className="divide-y divide-gray-200">
        {apiKeys && apiKeys.length > 0 ? (
          apiKeys.map((key) => (
            <div key={key.id} className="px-6 py-4">
              <div className="flex items-center justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-3">
                    <h3 className="text-sm font-medium text-gray-900">
                      {key.provider}
                    </h3>
                    {key.is_active ? (
                      <span className="px-2 py-0.5 bg-green-100 text-green-800 text-xs rounded">
                        Active
                      </span>
                    ) : (
                      <span className="px-2 py-0.5 bg-gray-100 text-gray-800 text-xs rounded">
                        Inactive
                      </span>
                    )}
                  </div>
                  <p className="mt-1 text-sm text-gray-500 font-mono">
                    {key.api_key_masked}
                  </p>
                  {key.base_url && (
                    <p className="mt-1 text-xs text-gray-400">
                      {key.base_url}
                    </p>
                  )}
                </div>
                <button
                  onClick={() => deleteMutation.mutate(key.provider)}
                  className="ml-4 text-sm text-red-600 hover:text-red-700 font-medium"
                >
                  Delete
                </button>
              </div>
            </div>
          ))
        ) : (
          <div className="px-6 py-8 text-center text-gray-500">
            No API keys configured. Add your first API key to get started.
          </div>
        )}
      </div>
    </div>
  );
}

function AddAPIKeyForm({ onSuccess }: { onSuccess: () => void }) {
  const [provider, setProvider] = useState('');
  const [apiKey, setApiKey] = useState('');
  const [baseUrl, setBaseUrl] = useState('');

  const mutation = useMutation({
    mutationFn: (data: any) => settingsApi.createApiKey(data),
    onSuccess,
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    mutation.mutate({
      provider,
      api_key: apiKey,
      base_url: baseUrl || undefined,
      is_active: true,
    });
  };

  return (
    <form onSubmit={handleSubmit} className="px-6 py-4 bg-gray-50 border-b border-gray-200">
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Provider
          </label>
          <input
            type="text"
            value={provider}
            onChange={(e) => setProvider(e.target.value)}
            placeholder="openrouter"
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            required
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            API Key
          </label>
          <input
            type="password"
            value={apiKey}
            onChange={(e) => setApiKey(e.target.value)}
            placeholder="sk-..."
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            required
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Base URL (optional)
          </label>
          <input
            type="url"
            value={baseUrl}
            onChange={(e) => setBaseUrl(e.target.value)}
            placeholder="https://api.provider.com"
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          />
        </div>
      </div>
      <div className="mt-4 flex justify-end">
        <button
          type="submit"
          disabled={mutation.isPending}
          className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors text-sm font-medium disabled:opacity-50"
        >
          {mutation.isPending ? 'Adding...' : 'Add API Key'}
        </button>
      </div>
    </form>
  );
}
