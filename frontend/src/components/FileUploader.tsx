import React, { useState, useRef } from 'react'
import { useSignedUploadUrl, useCreateDocumentMeta } from '@/api/documents'
import toast from 'react-hot-toast'

type Props = { onUploaded?: () => void }

export default function FileUploader({ onUploaded }: Props) {
  const inputRef = useRef<HTMLInputElement | null>(null)
  const signedMut = useSignedUploadUrl()
  const metaMut = useCreateDocumentMeta()
  const [loading, setLoading] = useState(false)

  const handleFile = async (file: File) => {
    setLoading(true)
    try {
      const { data } = await signedMut.mutateAsync({ filename: file.name, content_type: file.type })
      const uploadUrl = data.upload_url || data.uploadUrl || data.upload_url
      const storage_path = data.storage_path || data.storagePath || data.storage_path
      await fetch(uploadUrl, {
        method: 'PUT',
        headers: { 'Content-Type': file.type },
        body: file
      })
      await metaMut.mutateAsync({ name: file.name, mime_type: file.type, storage_path })
      toast.success('Uploaded')
      onUploaded?.()
    } catch (e) {
      toast.error('Upload failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <input ref={inputRef} type="file" hidden onChange={(e) => e.target.files && handleFile(e.target.files[0])} />
      <button onClick={() => inputRef.current?.click()} className="px-3 py-2 border rounded">
        Upload document
        {loading && '...'}
      </button>
    </div>
  )
}
