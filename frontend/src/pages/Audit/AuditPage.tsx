import React from 'react'
import { useAudit } from '@/api/audit'

export default function AuditPage() {
  const { data = [], isLoading } = useAudit()
  return (
    <div>
      <h1 className="text-2xl font-semibold mb-4">Audit Logs</h1>
      <div className="bg-white p-4 rounded shadow overflow-x-auto">
        <table className="w-full text-left">
          <thead>
            <tr>
              <th className="py-2">Action</th>
              <th className="py-2">Timestamp</th>
              <th className="py-2">Device</th>
              <th className="py-2">Metadata</th>
            </tr>
          </thead>
          <tbody>
            {isLoading ? (
              <tr><td>Loading...</td></tr>
            ) : data.map((a: any) => (
              <tr key={a.id} className="border-t">
                <td className="py-2">{a.action}</td>
                <td className="py-2">{new Date(a.timestamp).toLocaleString()}</td>
                <td className="py-2">{a.device_info}</td>
                <td className="py-2"><pre className="text-xs">{JSON.stringify(a.meta || {}, null, 2)}</pre></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
