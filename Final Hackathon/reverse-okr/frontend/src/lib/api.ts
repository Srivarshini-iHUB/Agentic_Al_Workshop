import { apiRequest } from './queryClient';

export interface WorkflowData {
  logs: string[] | null;
  activities: any | null;
  themes: any | null;
  knowledgeGraph: any | null;
  outcomes: any | null;
  okrs: any | null;
}

export interface ApiResponse<T = any> {
  [key: string]: T;
}

export const api = {
  async aggregateLogs(logs: string[]): Promise<ApiResponse> {
    const response = await apiRequest('POST', '/api/aggregate', { logs });
    return response.json();
  },

  async inferIntent(activities: any): Promise<ApiResponse> {
    const response = await apiRequest('POST', '/api/infer-intent', {input: activities });
    return response.json();
  },

  async mapGraph(themes: any): Promise<ApiResponse> {
    const response = await apiRequest('POST', '/api/map-graph', {  input: themes  });
    return response.json();
  },

  async generateOutcomes(knowledge_graph: any, themes?: any): Promise<ApiResponse> {
    const response = await apiRequest('POST', '/api/generate-outcomes', { 
      input: {
        knowledge_graph,
        themes 
      }
    });
    return response.json();
  },

  async generateOKR(outcomes: any, graph?: any): Promise<ApiResponse> {
    const response = await apiRequest('POST', '/api/generate-okr', { 
     input: {
        outcomes,
        graph 
      } 
    });
    return response.json();
  }
};
