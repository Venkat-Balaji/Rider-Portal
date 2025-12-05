import React, { useState } from 'react'
import { useMyQR, useRegenerateQR } from '@/api/qr'
import Modal from '@/components/ui/Modal'
import toast from 'react-hot-toast'
import QRCode from 'react-qr-code'

export default function QRPage() {
  const { data, isLoading } = useMyQR()
  const regen = useRegenerateQR()
  const [confirmOpen, setConfirmOpen] = useState(false)

  const onRegenerate = async () => {
    try {
      await regen.mutateAsync()
      toast.success('QR regenerated')
      setConfirmOpen(false)
    } catch {
      toast.error('Failed')
    }
  }

  return (
    <div>
      <h1 className="text-2xl font-semibold mb-4">My QR</h1>
      <div className="bg-white p-6 rounded shadow inline-block">
        {isLoading ? (
          <div>Loading...</div>
        ) : (
          <>
            {data?.image_url ? (
              <img src={data.image_url} alt="qr" className="w-56 h-56 object-contain" />
            ) : (
              <QRCode value={data?.token || 'no-token'} size={220} />
            )}
            <div className="mt-3 break-all">{data?.token}</div>
            <div className="mt-3">
              <button onClick={() => setConfirmOpen(true)} className="px-3 py-2 bg-yellow-500 rounded">Regenerate QR</button>
            </div>
          </>
        )}
      </div>

      <Modal open={confirmOpen} onClose={() => setConfirmOpen(false)} title="Regenerate QR?">
        <div className="space-y-3">
          <div>This will invalidate the current QR token. Are you sure?</div>
          <div className="flex gap-2">
            <button className="px-4 py-2 bg-red-600 text-white rounded" onClick={onRegenerate}>Yes, regenerate</button>
            <button className="px-4 py-2 border rounded" onClick={() => setConfirmOpen(false)}>Cancel</button>
          </div>
        </div>
      </Modal>
    </div>
  )
}
