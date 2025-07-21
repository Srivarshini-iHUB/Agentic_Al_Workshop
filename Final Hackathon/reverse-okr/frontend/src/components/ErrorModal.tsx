import { X, AlertTriangle } from "lucide-react";

interface ErrorModalProps {
  isOpen: boolean;
  message: string;
  onClose: () => void;
  onRetry: () => void;
}

export default function ErrorModal({ isOpen, message, onClose, onRetry }: ErrorModalProps) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center">
      <div className="glass-card rounded-xl p-8 max-w-md mx-4 border border-gray-600/30">
        <div className="text-center">
          <AlertTriangle className="text-red-400 mx-auto mb-4" size={48} />
          <h3 className="text-gray-100 font-semibold text-lg mb-2">Error Occurred</h3>
          <p className="text-gray-300 mb-6">{message}</p>
          <div className="flex space-x-3 justify-center">
            <button
              onClick={onClose}
              className="px-4 py-2 bg-gray-800/60 hover:bg-gray-700/80 text-gray-200 rounded-lg transition-all duration-200 border border-gray-600/30"
            >
              Close
            </button>
            <button
              onClick={onRetry}
              className="px-4 py-2 bg-primary-500 hover:bg-primary-600 text-white rounded-lg transition-all duration-200"
            >
              Retry
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
