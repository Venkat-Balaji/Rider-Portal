import React from 'react'
import { useDocuments, useDeleteDocument } from '@/api/documents'
import FileUploader from '@/components/FileUploader'
import toast from 'react-hot-toast'

export default function DocumentsPage() {
  const { data: docs = [], isLoading } = useDocuments()
  const del = useDeleteDocument()

  const remove = async (uuid: string) => {
    await del.mutateAsync(uuid)
    toast.success('Deleted')
  }

  return (
    <div>
      <h1 className="text-2xl font-semibold mb-4">Documents</h1>
      <div className="mb-4">
        <FileUploader onUploaded={() => {}} />
      </div>
      <div className="bg-white rounded shadow p-4">
        {isLoading ? (
          <div>Loading...</div>
        ) : (
          <ul>
            {docs.map((d: any) => (
              <li key={d.uuid} className="py-2 flex justify-between items-center border-b">
                <div className="flex items-center gap-4">
                  {d.thumbnail_path ? <img src={d.thumbnail_path} className="w-12 h-12 object-cover rounded" /> : <div className="w-12 h-12 bg-slate-100 flex items-center justify-center rounded">DOC</div>}
                  <div>
                    <div className="font-medium">{d.name}</div>
                    <div className="text-sm text-slate-500">{new Date(d.created_at).toLocaleString()}</div>
                  </div>
                </div>
                <div>
                  <button onClick={() => remove(d.uuid)} className="text-red-600">Delete</button>
                </div>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  )
}
