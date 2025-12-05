import React from 'react'
type Props = { open: boolean; onClose: () => void; title?: string; children?: React.ReactNode }
export default function Modal({ open, onClose, title, children }: Props) {
  if (!open) return null
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
      <div className="bg-white rounded shadow p-6 w-full max-w-lg">
        <div className="flex justify-between items-center mb-4">
          <h3 className="font-semibold">{title}</h3>
          <button onClick={onClose} className="text-slate-600">Close</button>
        </div>
        <div>{children}</div>
      </div>
    </div>
  )
}
