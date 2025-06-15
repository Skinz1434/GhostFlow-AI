/* GlowCard.tsx - Fully enhanced GlowCard component */

export default function GlowCard({ title, children }) {
  return (
    <div className="p-6 rounded-xl relative overflow-hidden glow shadow-lg">
      <h3 className="text-2xl mb-4 font-semibold">{title}</h3>
      {children}
      <style jsx>{`
        .glow::before {
          content: '';
          position: absolute;
          inset: -60%;
          background: conic-gradient(
            from 180deg,
            var(--qbit-purple),
            var(--qbit-blue),
            var(--qbit-purple)
          );
          animation: spin 10s linear infinite;
          filter: blur(80px);
          opacity: 0.5;
        }

        @keyframes spin {
          to {
            transform: rotate(1turn);
          }
        }
      `}</style>
    </div>
  );
}
