export interface Project {
  id: number;
  name: string;
  description?: string;
  status: ProjectStatus;
  requirements?: any;
  tech_stack?: any;
  created_at: string;
  updated_at: string;
}

export enum ProjectStatus {
  PENDING = 'pending',
  PLANNING = 'planning',
  IN_PROGRESS = 'in_progress',
  TESTING = 'testing',
  REVIEW = 'review',
  COMPLETED = 'completed',
  CANCELLED = 'cancelled',
}

export interface Agent {
  id: number;
  agent_id: string;
  name: string;
  role: string;
  status: AgentStatus;
  total_tasks: number;
  completed_tasks: number;
  failed_tasks: number;
  created_at: string;
}

export enum AgentStatus {
  IDLE = 'idle',
  BUSY = 'busy',
  ERROR = 'error',
  OFFLINE = 'offline',
}

export interface APIKey {
  id: number;
  provider: string;
  api_key_masked: string;
  base_url?: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
  last_used?: string;
}

export interface SystemConfig {
  app_name: string;
  version: string;
  default_llm_provider: string;
  default_model: string;
  max_agents: number;
  max_concurrent_projects: number;
  memory_backend: string;
  ollama_available: boolean;
}

export interface HealthStatus {
  status: string;
  service: string;
  version: string;
  services?: {
    [key: string]: string;
  };
}
