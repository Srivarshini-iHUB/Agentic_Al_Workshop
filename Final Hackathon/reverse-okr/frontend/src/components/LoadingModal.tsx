interface LoadingModalProps {
  isOpen: boolean;
  message: string;
}

export default function LoadingModal({ isOpen, message }: LoadingModalProps) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center">
      <div className="glass-card rounded-xl p-8 max-w-sm mx-4 border border-gray-600/30">
        <div className="text-center">
          <div className="loading-spinner mx-auto mb-4"></div>
          <h3 className="text-gray-100 font-semibold text-lg mb-2">Processing...</h3>
          <p className="text-gray-300">{message}</p>
        </div>
      </div>
    </div>
  );
}
