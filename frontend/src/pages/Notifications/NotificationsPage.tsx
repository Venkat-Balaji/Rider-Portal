import React from 'react'
import { useNotifications, useMarkAsRead } from '@/api/notifications'
import toast from 'react-hot-toast'

export default function NotificationsPage() {
  const { data: notes = [] } = useNotifications()
  const mark = useMarkAsRead()

  const handleMark = async (id: string) => {
    try {
      await mark.mutateAsync(id)
      toast.success('Marked read')
    } catch {
      toast.error('Error')
    }
  }

  return (
    <div>
      <h1 className="text-2xl font-semibold mb-4">Notifications</h1>
      <div className="bg-white p-4 rounded shadow">
        {notes.length === 0 ? <div>No notifications</div> : notes.map((n: any) => (
          <div key={n.id} className={`p-3 border-b ${n.read ? 'opacity-60' : ''}`}>
            <div className="flex justify-between items-start">
              <div>
                <div className="font-medium">{n.title}</div>
                <div className="text-sm text-slate-600">{n.body}</div>
              </div>
              <div>
                {!n.read && <button onClick={() => handleMark(n.id)} className="text-blue-600">Mark read</button>}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
