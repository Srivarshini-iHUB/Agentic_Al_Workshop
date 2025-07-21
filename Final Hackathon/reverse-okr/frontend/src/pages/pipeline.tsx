import { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { 
  Network, 
  RefreshCw, 
  FileText, 
  Brain, 
  Target, 
  Trophy, 
  Download, 
  Play,
  ArrowLeft,
  Lightbulb,
  Map,
  Goal
} from 'lucide-react';
import { api, WorkflowData } from '../lib/api';
import LoadingModal from '../components/LoadingModal';
import ErrorModal from '../components/ErrorModal';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Card, CardContent } from '@/components/ui/card';

const STEPS = [
  { id: 1, title: 'Log Aggregation', description: 'Parse raw logs', icon: FileText },
  { id: 2, title: 'Intent Inference', description: 'Identify themes', icon: Brain },
  { id: 3, title: 'Knowledge Graph', description: 'Map relationships', icon: Map },
  { id: 4, title: 'Outcome Generation', description: 'Create outcomes', icon: Target },
  { id: 5, title: 'OKR Generation', description: 'Generate OKRs', icon: Trophy },
];

export default function Pipeline() {
  const [currentStep, setCurrentStep] = useState(1);
  const [workflowData, setWorkflowData] = useState<WorkflowData>({
    logs: null,
    activities: null,
    themes: null,
    knowledgeGraph: null,
    outcomes: null,
    okrs: null,
  });
  const [logsInput, setLogsInput] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [currentRetryAction, setCurrentRetryAction] = useState<(() => void) | null>(null);

  const step1Mutation = useMutation({
    mutationFn: api.aggregateLogs,
    onSuccess: (data) => {
      setWorkflowData(prev => ({ ...prev, activities: data }));
      setCurrentStep(Math.max(currentStep, 2));
    },
    onError: (err: any) => {
      setError(`Failed to aggregate logs: ${err.message}`);
      setCurrentRetryAction(() => () => processStep1());
    }
  });

  const step2Mutation = useMutation({
    mutationFn: api.inferIntent,
    onSuccess: (data) => {
      setWorkflowData(prev => ({ ...prev, themes: data }));
      setCurrentStep(Math.max(currentStep, 3));
    },
    onError: (err: any) => {
      setError(`Failed to infer intent: ${err.message}`);
      setCurrentRetryAction(() => () => processStep2());
    }
  });

  const step3Mutation = useMutation({
    mutationFn: api.mapGraph,
    onSuccess: (data) => {
      setWorkflowData(prev => ({ ...prev, knowledgeGraph: data }));
      setCurrentStep(Math.max(currentStep, 4));
    },
    onError: (err: any) => {
      setError(`Failed to map knowledge graph: ${err.message}`);
      setCurrentRetryAction(() => () => processStep3());
    }
  });

  const step4Mutation = useMutation({
    mutationFn: ({ knowledge_graph, themes }: any) => api.generateOutcomes(knowledge_graph, themes),
    onSuccess: (data) => {
      setWorkflowData(prev => ({ ...prev, outcomes: data }));
      setCurrentStep(Math.max(currentStep, 5));
    },
    onError: (err: any) => {
      setError(`Failed to generate outcomes: ${err.message}`);
      setCurrentRetryAction(() => () => processStep4());
    }
  });

  const step5Mutation = useMutation({
    mutationFn: ({ outcomes, graph }: any) => api.generateOKR(outcomes, graph),
    onSuccess: (data) => {
      setWorkflowData(prev => ({ ...prev, okrs: data }));
    },
    onError: (err: any) => {
      setError(`Failed to generate OKRs: ${err.message}`);
      setCurrentRetryAction(() => () => processStep5());
    }
  });

  const processStep1 = () => {
    const logs = logsInput.trim().split('\n').filter(line => line.trim());
    if (!logs.length) {
      setError('Please enter some learning logs');
      return;
    }
    step1Mutation.mutate(logs);
  };

  const processStep2 = () => {
    if (!workflowData.activities) {
      setError('No activities data available. Complete Step 1 first.');
      return;
    }
    step2Mutation.mutate(workflowData.activities);
  };

  const processStep3 = () => {
    if (!workflowData.themes) {
      setError('No themes data available. Complete Step 2 first.');
      return;
    }
    const themes = workflowData.themes.themes?.output || workflowData.themes;
    step3Mutation.mutate(themes);
  };

  const processStep4 = () => {
    if (!workflowData.knowledgeGraph) {
      setError('No knowledge graph data available. Complete Step 3 first.');
      return;
    }
    step4Mutation.mutate({
      knowledge_graph: workflowData.knowledgeGraph,
      themes: workflowData.themes
    });
  };

  const processStep5 = () => {
    if (!workflowData.outcomes) {
      setError('No outcomes data available. Complete Step 4 first.');
      return;
    }
    step5Mutation.mutate({
      outcomes: workflowData.outcomes,
      graph: workflowData.knowledgeGraph
    });
  };

  const loadSampleData = () => {
    const sampleLogs = `https://www.youtube.com/watch?v=dD2EISBDjWM - React Tutorial
https://github.com/streamlit/streamlit - Data viz library
https://www.figma.com/file/abcd1234/UI-Mockups - UI Design
Read 'Clean Code' chapters 1-3
Completed Python pandas course`;
    setLogsInput(sampleLogs);
  };

  const resetWorkflow = () => {
    setCurrentStep(1);
    setWorkflowData({
      logs: null,
      activities: null,
      themes: null,
      knowledgeGraph: null,
      outcomes: null,
      okrs: null,
    });
    setLogsInput('');
    setError(null);
  };

  const exportResults = () => {
    const results = {
      workflow_completion_date: new Date().toISOString(),
      pipeline_results: workflowData
    };
    
    const dataStr = JSON.stringify(results, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `learning_analytics_results_${new Date().toISOString().split('T')[0]}.json`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  const selectStep = (step: number) => {
    if (step <= currentStep) {
      // Allow navigation to completed steps
    }
  };

  const createJSONDisplay = (data: any) => {
    if (!data) return null;
    return (
      <pre className="text-green-400 text-sm overflow-auto whitespace-pre-wrap">
        {JSON.stringify(data, null, 2)}
      </pre>
    );
  };

  const EmptyState = ({ icon: Icon, message }: { icon: any; message: string }) => (
    <div className="text-white/60 text-center py-16">
      <Icon className="mx-auto mb-4" size={48} />
      <p>{message}</p>
    </div>
  );

  const isLoading = step1Mutation.isPending || step2Mutation.isPending || 
                   step3Mutation.isPending || step4Mutation.isPending || step5Mutation.isPending;

  const loadingMessage = step1Mutation.isPending ? 'Aggregating exploration logs...' :
                        step2Mutation.isPending ? 'Inferring themes and intent...' :
                        step3Mutation.isPending ? 'Mapping knowledge graph...' :
                        step4Mutation.isPending ? 'Generating learning outcomes...' :
                        step5Mutation.isPending ? 'Generating retrospective OKRs...' : 'Processing...';

  return (
    <div className="min-h-screen gradient-bg">
      {/* Header */}
      <header className="bg-gray-900/80 backdrop-blur-md border-b border-gray-700/50 sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-4">
              <div className="flex items-center justify-center w-10 h-10 rounded-lg bg-gray-800/60 backdrop-blur-sm border border-gray-600/30">
                <Network className="text-gray-200" size={20} />
              </div>
              <h1 className="text-xl font-bold text-white">Learning Analytics Pipeline</h1>
            </div>
            
            <div className="step-indicator rounded-full px-4 py-2">
              <span className="text-white text-sm font-medium">
                Step {currentStep} of 5
              </span>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Left Sidebar */}
          <div className="lg:col-span-1">
            <div className="glass-card rounded-xl p-6 sticky top-24">
              <h2 className="text-white font-semibold text-lg mb-4">Workflow Steps</h2>
              <nav className="space-y-3">
                {STEPS.map((step) => {
                  const Icon = step.icon;
                  const isActive = step.id === currentStep;
                  const isCompleted = step.id < currentStep;
                  const isAccessible = step.id <= currentStep;
                  
                  return (
                    <div
                      key={step.id}
                      className={`cursor-pointer p-3 rounded-lg transition-all duration-200 ${
                        isAccessible ? 'hover:bg-white/10' : 'opacity-50 cursor-not-allowed'
                      }`}
                      onClick={() => isAccessible && selectStep(step.id)}
                    >
                      <div className="flex items-center space-x-3">
                        <div className={`w-8 h-8 rounded-full text-sm font-bold flex items-center justify-center ${
                          isCompleted || isActive ? 'bg-primary-500 text-white' : 'bg-white/20 text-white'
                        }`}>
                          {step.id}
                        </div>
                        <div>
                          <div className="text-white font-medium">{step.title}</div>
                          <div className="text-white/70 text-sm">{step.description}</div>
                        </div>
                      </div>
                    </div>
                  );
                })}
              </nav>

              <div className="mt-8 pt-6 border-t border-gray-600/30">
                <Button
                  onClick={resetWorkflow}
                  className="w-full bg-gray-800/60 hover:bg-gray-700/80 text-gray-200 backdrop-blur-sm border border-gray-600/30"
                  variant="ghost"
                >
                  <RefreshCw className="mr-2" size={16} />
                  Reset Workflow
                </Button>
              </div>
            </div>
          </div>

          {/* Main Content */}
          <div className="lg:col-span-3">
            <Card className="glass-card border-gray-700/30 min-h-[600px]">
              <CardContent className="p-8">
                {/* Step 1: Log Aggregation */}
                {currentStep >= 1 && (
                  <div className={currentStep === 1 ? 'block' : 'hidden'}>
                    <div className="mb-6">
                      <h2 className="text-2xl font-bold text-white mb-2">Step 1: Log Aggregation</h2>
                      <p className="text-white/80">Enter your learning exploration logs to begin the analysis pipeline.</p>
                    </div>

                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                      <div>
                        <label className="block text-white font-medium mb-3">Learning Logs</label>
                        <Textarea
                          value={logsInput}
                          onChange={(e) => setLogsInput(e.target.value)}
                          className="h-64 bg-gray-900/60 border-gray-600/30 text-gray-100 placeholder-gray-400 backdrop-blur-sm resize-none"
                          placeholder="Enter your learning logs here...

Examples:
https://www.youtube.com/watch?v=dD2EISBDjWM - React Tutorial
https://github.com/streamlit/streamlit - Data viz library
https://www.figma.com/file/abcd1234/UI-Mockups - UI Design"
                        />
                        
                        <div className="mt-4 flex space-x-3">
                          <Button
                            onClick={loadSampleData}
                            variant="ghost"
                            className="bg-gray-800/60 hover:bg-gray-700/80 text-gray-200 backdrop-blur-sm border border-gray-600/30"
                          >
                            <FileText className="mr-2" size={16} />
                            Load Sample
                          </Button>
                          <Button
                            onClick={processStep1}
                            className="bg-primary-500 hover:bg-primary-600 text-white"
                            disabled={step1Mutation.isPending}
                          >
                            <Play className="mr-2" size={16} />
                            Process Logs
                          </Button>
                        </div>
                      </div>

                      <div>
                        <label className="block text-white font-medium mb-3">Processing Results</label>
                        <div className="json-viewer rounded-lg p-4 h-64 overflow-auto">
                          {workflowData.activities ? 
                            createJSONDisplay(workflowData.activities) : 
                            <EmptyState icon={Play} message="Click 'Process Logs' to see aggregated activities" />
                          }
                        </div>
                      </div>
                    </div>
                  </div>
                )}

                {/* Step 2: Intent Inference */}
                {currentStep >= 2 && (
                  <div className={currentStep === 2 ? 'block' : 'hidden'}>
                    <div className="mb-6">
                      <h2 className="text-2xl font-bold text-white mb-2">Step 2: Intent & Theme Inference</h2>
                      <p className="text-white/80">Analyzing your activities to identify learning themes and intentions.</p>
                    </div>

                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                      <div>
                        <label className="block text-white font-medium mb-3">Input Activities</label>
                        <div className="json-viewer rounded-lg p-4 h-64 overflow-auto">
                          {workflowData.activities ? 
                            createJSONDisplay(workflowData.activities) : 
                            <EmptyState icon={ArrowLeft} message="Complete Step 1 first" />
                          }
                        </div>
                        
                        <div className="mt-4">
                          <Button
                            onClick={processStep2}
                            className="bg-primary-500 hover:bg-primary-600 text-white"
                            disabled={!workflowData.activities || step2Mutation.isPending}
                          >
                            <Brain className="mr-2" size={16} />
                            Infer Intent
                          </Button>
                        </div>
                      </div>

                      <div>
                        <label className="block text-white font-medium mb-3">Inferred Themes</label>
                        <div className="json-viewer rounded-lg p-4 h-64 overflow-auto">
                          {workflowData.themes ? 
                            createJSONDisplay(workflowData.themes) : 
                            <EmptyState icon={Lightbulb} message="Themes and intentions will appear here" />
                          }
                        </div>
                      </div>
                    </div>
                  </div>
                )}

                {/* Step 3: Knowledge Graph */}
                {currentStep >= 3 && (
                  <div className={currentStep === 3 ? 'block' : 'hidden'}>
                    <div className="mb-6">
                      <h2 className="text-2xl font-bold text-white mb-2">Step 3: Knowledge Graph Mapping</h2>
                      <p className="text-white/80">Building a knowledge graph to map concepts and their relationships.</p>
                    </div>

                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                      <div>
                        <label className="block text-white font-medium mb-3">Input Themes</label>
                        <div className="json-viewer rounded-lg p-4 h-64 overflow-auto">
                          {workflowData.themes ? 
                            createJSONDisplay(workflowData.themes) : 
                            <EmptyState icon={ArrowLeft} message="Complete Step 2 first" />
                          }
                        </div>
                        
                        <div className="mt-4">
                          <Button
                            onClick={processStep3}
                            className="bg-primary-500 hover:bg-primary-600 text-white"
                            disabled={!workflowData.themes || step3Mutation.isPending}
                          >
                            <Map className="mr-2" size={16} />
                            Map Graph
                          </Button>
                        </div>
                      </div>

                      <div>
                        <label className="block text-white font-medium mb-3">Knowledge Graph</label>
                        <div className="json-viewer rounded-lg p-4 h-64 overflow-auto">
                          {workflowData.knowledgeGraph ? 
                            createJSONDisplay(workflowData.knowledgeGraph) : 
                            <EmptyState icon={Map} message="Knowledge graph will be mapped here" />
                          }
                        </div>
                      </div>
                    </div>
                  </div>
                )}

                {/* Step 4: Outcome Generation */}
                {currentStep >= 4 && (
                  <div className={currentStep === 4 ? 'block' : 'hidden'}>
                    <div className="mb-6">
                      <h2 className="text-2xl font-bold text-white mb-2">Step 4: Outcome Generation</h2>
                      <p className="text-white/80">Generating actionable learning outcomes based on your knowledge graph.</p>
                    </div>

                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                      <div>
                        <label className="block text-white font-medium mb-3">Knowledge Graph Input</label>
                        <div className="json-viewer rounded-lg p-4 h-64 overflow-auto">
                          {workflowData.knowledgeGraph ? 
                            createJSONDisplay(workflowData.knowledgeGraph) : 
                            <EmptyState icon={ArrowLeft} message="Complete Step 3 first" />
                          }
                        </div>
                        
                        <div className="mt-4">
                          <Button
                            onClick={processStep4}
                            className="bg-primary-500 hover:bg-primary-600 text-white"
                            disabled={!workflowData.knowledgeGraph || step4Mutation.isPending}
                          >
                            <Target className="mr-2" size={16} />
                            Generate Outcomes
                          </Button>
                        </div>
                      </div>

                      <div>
                        <label className="block text-white font-medium mb-3">Learning Outcomes</label>
                        <div className="json-viewer rounded-lg p-4 h-64 overflow-auto">
                          {workflowData.outcomes ? 
                            createJSONDisplay(workflowData.outcomes) : 
                            <EmptyState icon={Goal} message="Actionable outcomes will appear here" />
                          }
                        </div>
                      </div>
                    </div>
                  </div>
                )}

                {/* Step 5: OKR Generation */}
                {currentStep >= 5 && (
                  <div className={currentStep === 5 ? 'block' : 'hidden'}>
                    <div className="mb-6">
                      <h2 className="text-2xl font-bold text-white mb-2">Step 5: OKR Generation</h2>
                      <p className="text-white/80">Creating retrospective OKRs based on your learning outcomes.</p>
                    </div>

                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                      <div>
                        <label className="block text-white font-medium mb-3">Outcomes Input</label>
                        <div className="json-viewer rounded-lg p-4 h-64 overflow-auto">
                          {workflowData.outcomes ? 
                            createJSONDisplay(workflowData.outcomes) : 
                            <EmptyState icon={ArrowLeft} message="Complete Step 4 first" />
                          }
                        </div>
                        
                        <div className="mt-4">
                          <Button
                            onClick={processStep5}
                            className="bg-primary-500 hover:bg-primary-600 text-white"
                            disabled={!workflowData.outcomes || step5Mutation.isPending}
                          >
                            <Trophy className="mr-2" size={16} />
                            Generate OKRs
                          </Button>
                        </div>
                      </div>

                      <div>
                        <label className="block text-white font-medium mb-3">Retrospective OKRs</label>
                        <div className="json-viewer rounded-lg p-4 h-64 overflow-auto">
                          {workflowData.okrs ? 
                            createJSONDisplay(workflowData.okrs) : 
                            <EmptyState icon={Trophy} message="Your OKRs will be generated here" />
                          }
                        </div>
                        
                        {workflowData.okrs && (
                          <div className="mt-4">
                            <Button
                              onClick={exportResults}
                              className="bg-green-500 hover:bg-green-600 text-white"
                            >
                              <Download className="mr-2" size={16} />
                              Export Results
                            </Button>
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
        </div>
      </div>

      <LoadingModal isOpen={isLoading} message={loadingMessage} />
      <ErrorModal
        isOpen={!!error}
        message={error || ''}
        onClose={() => setError(null)}
        onRetry={() => {
          setError(null);
          if (currentRetryAction) {
            currentRetryAction();
          }
        }}
      />
    </div>
  );
}
