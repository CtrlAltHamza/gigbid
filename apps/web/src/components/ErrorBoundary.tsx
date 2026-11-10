import React, { Component, ErrorInfo, ReactNode } from 'react';
import { AlertTriangle, RefreshCw } from 'lucide-react';

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

export class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false,
    error: null,
  };

  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error("Uncaught error caught by ErrorBoundary:", error, errorInfo);
  }

  public componentDidUpdate(prevProps: Props) {
    // Automatically reset error state when switching to another view
    if (this.state.hasError && prevProps.children !== this.props.children) {
      this.setState({ hasError: false, error: null });
    }
  }

  public render() {
    if (this.state.hasError) {
      return (
        <div className="py-12 px-6 flex flex-col items-center justify-center text-center font-sans">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-8 max-w-lg space-y-4 shadow-2xl">
            <div className="w-12 h-12 rounded-xl bg-amber-500/20 text-amber-400 flex items-center justify-center mx-auto border border-amber-500/30">
              <AlertTriangle className="w-6 h-6" />
            </div>
            <h2 className="text-xl font-bold text-white">Temporary Rendering Hiccup</h2>
            <p className="text-xs text-slate-400 leading-relaxed">
              An unexpected data formatting mismatch occurred during render:
            </p>
            <pre className="bg-slate-950 p-3 rounded-lg text-xs font-mono text-rose-300 overflow-x-auto text-left">
              {this.state.error?.message || "Unknown error"}
            </pre>
            <div className="flex items-center justify-center space-x-3 pt-2">
              <button
                onClick={() => this.setState({ hasError: false, error: null })}
                className="bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold px-4 py-2.5 rounded-xl transition flex items-center space-x-2"
              >
                <RefreshCw className="w-3.5 h-3.5" />
                <span>Retry View</span>
              </button>
            </div>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}
